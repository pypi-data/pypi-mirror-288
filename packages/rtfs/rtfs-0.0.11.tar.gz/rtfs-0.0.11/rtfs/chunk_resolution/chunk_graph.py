from networkx import DiGraph, node_link_graph, node_link_data
from pathlib import Path
from llama_index.core.schema import BaseNode
from typing import List, Tuple, Dict
import os
from collections import deque

from rtfs.scope_resolution.capture_refs import capture_refs
from rtfs.scope_resolution.graph_types import ScopeID
from rtfs.repo_resolution.repo_graph import RepoGraph, RepoNodeID, repo_node_id
from rtfs.fs import RepoFs
from rtfs.utils import TextRange
from rtfs.graph import Node

from rtfs.models import OpenAIModel, BaseModel

from .graph import (
    ChunkMetadata,
    ClusterNode,
    ChunkNode,
    EdgeKind,
    ImportEdge,
    ClusterEdge,
    NodeKind,
    ChunkNodeID,
)
from .cluster import (
    cluster_infomap,
    summarize_chunk_text,
    LLMException,
    SummarizedChunk,
)

import logging
from collections import defaultdict


logger = logging.getLogger(__name__)


class ChunkGraph:
    def __init__(
        self,
        repo_path: Path,
        g: DiGraph,
        cluster_roots=[],
        cluster_depth=None,
    ):
        self.fs = RepoFs(repo_path)
        self._graph = g
        self._repo_graph = RepoGraph(repo_path)
        self._file2scope = defaultdict(set)
        self._chunkmap: Dict[Path, List[ChunkNode]] = defaultdict(list)
        self._lm: BaseModel = OpenAIModel()

        self._cluster_roots = cluster_roots
        self._cluster_depth = cluster_depth

    # TODO: design decisions
    # turn import => export mapping into a function
    # implement tqdm for chunk by chunk processing
    @classmethod
    def from_chunks(cls, repo_path: Path, chunks: List[BaseNode]):
        """
        Build chunk (import) to chunk (export) mapping by associating a chunk with
        the list of scopes, and then using the scope -> scope mapping provided in RepoGraph
        to resolve the exports
        """
        g = DiGraph()
        cg: ChunkGraph = cls(repo_path, g)
        cg._file2scope = defaultdict(set)

        # used to map range to chunks
        chunk_names = set()

        for i, chunk in enumerate(chunks, start=1):
            metadata = ChunkMetadata(**chunk.metadata)

            short_name = cg._chunk_short_name(chunk, i)
            chunk_names.add(short_name)
            chunk_node = ChunkNode(
                id=short_name,
                og_id=chunk.node_id,
                metadata=metadata,
                content=chunk.get_content(),
            )
            cg.add_node(chunk_node)
            cg._chunkmap[Path(metadata.file_path)].append(chunk_node)

        # shouldnt really happen but ...
        if len(chunk_names) != len(chunks):
            raise ValueError("Collision has occurred in chunk names")

        # main loop to build graph
        for chunk_node in cg.get_all_nodes():
            # chunk -> range -> scope
            cg.build_import_exports(chunk_node)

        for f, scopes in cg._file2scope.items():
            all_scopes = cg._repo_graph.scopes_map[f].scopes()
            all_scopes = set(all_scopes)

            unresolved = all_scopes - scopes

        return cg

    @classmethod
    def from_json(cls, repo_path: Path, json_data: Dict):
        cg = node_link_graph(json_data["link_data"])

        return cls(repo_path, cg, cluster_roots=json_data["cluster_roots"])

    def to_json(self):
        graph_dict = {}
        graph_dict["cluster_roots"] = self._cluster_roots
        graph_dict["link_data"] = node_link_data(self._graph)

        return graph_dict

    def get_node(self, node_id: str) -> ChunkNode:
        data = self._graph._node.get(node_id, None)
        if not data:
            return None

        # BUG: hacky fix but for some reason node_link_data stores
        # the data wihtout id
        if data.get("id", None):
            del data["id"]

        if data["kind"] == NodeKind.Cluster:
            node = ClusterNode(id=node_id, **data)
        elif data["kind"] == NodeKind.Chunk:
            node = ChunkNode(id=node_id, **data)

        return node

    def remove_node(self, node_id: str):
        """
        Remove a node from the graph by its ID.

        Parameters:
        node_id (str): The ID of the node to be removed.
        """
        if node_id in self._graph:
            self._graph.remove_node(node_id)
        else:
            raise ValueError(f"Node with ID {node_id} does not exist in the graph.")

    def get_all_nodes(self) -> List[ChunkNode]:
        return [self.get_node(n) for n in self._graph.nodes]

    def add_edge(self, n1, n2, edge: ImportEdge):
        self._graph.add_edge(n1, n2, **edge.dict())

    def add_node(self, node: Node):
        id = node.id
        self._graph.add_node(id, **node.dict())

    def update_node(self, chunk_node: ChunkNode):
        self.add_node(chunk_node)

    def build_import_exports(self, chunk_node: ChunkNode):
        """
        Build the import to export mapping for a chunk
        need to do: import (chunk -> range -> scope) -> export (scope -> range -> chunk)
        """
        src_path = Path(chunk_node.metadata.file_path)
        scope_graph = self._repo_graph.scopes_map[src_path]
        chunk_refs = capture_refs(chunk_node.content.encode())

        for ref in chunk_refs:
            ref.range.add_line_offset(chunk_node.metadata.start_line)
            # range -> scope
            ref_scope = scope_graph.scope_by_range(ref.range)
            # scope (import) -> scope (export)
            export_scopes = self._repo_graph.import_to_export_scope(
                repo_node_id(src_path, ref_scope), ref.name
            )
            # scope -> range -> chunk
            # decision:
            # 1. can resolve range here using the scope
            # 2. can resolve range when RepoNode is constructed
            # Favor 1. since we can use repo_graph for both scope->range and range->scope
            for export_file, export_scope, export_sg in [
                (
                    node.file_path,
                    node.scope,
                    self._repo_graph.scopes_map[Path(node.file_path)],
                )
                for node in export_scopes
            ]:
                export_range = export_sg.range_by_scope(export_scope)
                dst_chunk = self.find_chunk(Path(export_file), export_range)

                if dst_chunk:
                    # print("Found chunk: ", dst_chunk.id, "with ref: ", ref.name)

                    edge = ImportEdge(ref=ref.name, kind=EdgeKind.ImportToExport)
                    self.add_edge(chunk_node.id, dst_chunk.id, edge)

    # TODO: should really use IntervalGraph here but chunks are small enough
    def find_chunk(self, file_path: Path, range: TextRange):
        """
        Find a chunk given a range
        """
        chunks = self._chunkmap[file_path]
        for chunk in chunks:
            if chunk.range.contains_line(range, overlap=True):
                return chunk

        return None

    def children(self, node_id: str):
        return [child for child, _ in self._graph.in_edges(node_id)]

    # TODO: this only works for cluster nodes
    def parent(self, node_id: str):
        parents = [parent for _, parent in self._graph.out_edges(node_id)]
        if parents:
            return parents[0]
        return None

    def get_clusters_at_depth(self, roots: List[ClusterNode], level):
        queue = deque([(root, 0) for root in roots])
        visited = set(roots)
        clusters_at_level = []

        while queue:
            node, depth = queue.popleft()

            if depth == level:
                clusters_at_level.append(node)
            elif depth > level:
                break

            for neighbor in self.children(node):
                if neighbor not in visited:
                    if self._graph.nodes[neighbor]["kind"] == NodeKind.Cluster:
                        visited.add(neighbor)
                        queue.append((neighbor, depth + 1))

        return clusters_at_level

    def _get_cluster_roots(self):
        """
        Gets the multiple root cluster nodes generated from Infomap
        """
        roots = []
        for node in self._graph.nodes:
            if isinstance(self.get_node(node), ClusterNode):
                if not self.parent(node):
                    roots.append(node)

        return roots

    def cluster(self, alg: str = "infomap") -> Dict[ChunkNodeID, Tuple]:
        """
        Entry method for cluster construction on ChunkGraph
        """
        if alg == "infomap":
            cluster_dict = cluster_infomap(self._graph)
        else:
            raise Exception(f"{alg} not supported")

        # NOTE: this max depth number seems sketchy...
        max_cluster_depth = 0
        for chunk_node, clusters in cluster_dict.items():
            for i in range(len(clusters) - 1):
                # TODO: i lazy, not handle case where clusters[i: i+2] is len 1
                parent, child = clusters[i : i + 2]

                parent_id = f"{i}:{parent}"
                child_id = f"{i+1}:{child}"

                parent_node = self.get_node(parent_id)
                if not parent_node:
                    parent_node = ClusterNode(id=parent_id)
                    self.add_node(parent_node)
                child_node = self.get_node(child_id)
                if not child_node:
                    child_node = ClusterNode(id=child_id)
                    self.add_node(child_node)

                self.add_edge(
                    child_id, parent_id, ClusterEdge(kind=EdgeKind.ClusterToCluster)
                )

                if i > max_cluster_depth:
                    max_cluster_depth = i

            # last child_id is the cluster of chunk_node
            self.add_edge(
                chunk_node, child_id, ClusterEdge(kind=EdgeKind.NodeToCluster)
            )

        self._cluster_depth = max_cluster_depth
        self._cluster_roots = self._get_cluster_roots()
        print("Cluster root: ", self._cluster_roots)

        for depth in range(max_cluster_depth + 1, -1, -1):
            clusters = self.get_clusters_at_depth(self._cluster_roots, depth)

            # Get rid of all intermediary clusters that have only one children
            for cluster in clusters:
                children = self.children(cluster)
                if len(children) < 2:
                    parent = self.parent(cluster)
                    if parent:
                        self.remove_node(cluster)
                        for child in children:
                            child_node = self.get_node(child)

                            self.add_edge(
                                child,
                                parent,
                                ClusterEdge(
                                    kind=(
                                        EdgeKind.ClusterToCluster
                                        if child_node.kind == NodeKind.Cluster
                                        else EdgeKind.NodeToCluster
                                    )
                                ),
                            )

                    else:
                        if not children:
                            self.remove_node(cluster)
                        else:
                            child = children[0]
                            grand_children = self.children(child)
                            self.remove_node(child)
                            for grand_child in grand_children:
                                self.add_edge(
                                    grand_child,
                                    cluster,
                                    ClusterEdge(
                                        kind=(
                                            EdgeKind.ClusterToCluster
                                            if self.get_node(grand_child).kind
                                            == NodeKind.Cluster
                                            else EdgeKind.NodeToCluster
                                        )
                                    ),
                                )
                    continue

        return cluster_dict

    # TODO: we need to fix the depth of the node
    async def summarize(self, user_confirm: bool = False):
        if self._cluster_depth is None:
            raise ValueError("Must cluster before summarizing")

        if user_confirm:
            agg_chunks = ""
            for depth in range(self._cluster_depth + 1, -1, -1):
                clusters = self.get_clusters_at_depth(self._cluster_roots, depth)
                for cluster in clusters:
                    # only count Chunk tokens
                    chunk_text = "\n".join(
                        [
                            self.get_node(c).get_content()
                            for c in self.children(cluster)
                            if self.get_node(c).kind == NodeKind.Chunk
                        ]
                    )
                    agg_chunks += chunk_text

            tokens, cost = self._lm.calc_input_cost(agg_chunks)
            user_input = input(
                f"The summarization will cost ${cost} and use {tokens} tokens. Do you want to proceed? (yes/no): "
            )
            if user_input.lower() != "yes":
                print("Aborted.")
                exit()

        for depth in range(self._cluster_depth + 1, -1, -1):
            clusters = self.get_clusters_at_depth(self._cluster_roots, depth)
            for cluster in clusters:
                chunk_text = "\n".join(
                    [self.get_node(c).get_content() for c in self.children(cluster)]
                )
                try:
                    summary_data = await summarize_chunk_text(chunk_text, self._lm)
                except LLMException:
                    continue

                cluster_node = ClusterNode(id=cluster, summary_data=summary_data)
                self.update_node(cluster_node)

    def get_chunks_attached_to_clusters(self):
        chunks_attached_to_clusters = {}
        clusters = defaultdict(int)

        total_chunks = len(
            [
                node
                for node, attrs in self._graph.nodes(data=True)
                if attrs["kind"] == "Chunk"
            ]
        )
        total_leaves = 0
        for u, v, attrs in self._graph.edges(data=True):
            if attrs.get("kind") == EdgeKind.NodeToCluster:
                chunk_node = self.get_node(u)
                cluster_node = self.get_node(v)

                if cluster_node.id not in chunks_attached_to_clusters:
                    chunks_attached_to_clusters[cluster_node.id] = []

                chunks_attached_to_clusters[cluster_node.id].append(chunk_node)
                clusters[cluster_node.id] += 1
                total_leaves += 1

        # for cluster, chunks in chunks_attached_to_clusters.items():
        #     print(f"---------------------{cluster}------------------")
        #     for chunk in chunks:
        #         print(chunk.id)
        #         print(chunk.content)
        #         print("--------------------------------------------------")

        print(f"Total chunks: {total_chunks}")
        print(f"Total leaves: {total_leaves}")

        return chunks_attached_to_clusters

    def _chunk_short_name(self, chunk_node: BaseNode, i: int) -> str:
        # class_func = self._get_classes_and_funcs(
        #     Path(chunk_node.metadata["file_path"]), head_scope
        # )[0]

        filename = "/".join(chunk_node.metadata["file_path"].split(os.sep)[-2:])
        size = chunk_node.metadata["end_line"] - chunk_node.metadata["start_line"]
        # return f"{filename}.{class_func}.{size}"

        return f"{filename}#{i}.{size}"

    def _get_classes_and_funcs(
        self, file_path: Path, scope_id: ScopeID
    ) -> List[RepoNodeID]:
        def_nodes = self._repo_graph.scopes_map[file_path].definitions(scope_id)

        return list(
            filter(lambda d: d.data["def_type"] in ["class", "function"], def_nodes)
        )

    ##### FOR testing prompt #####
    def get_chunk_imports(self):
        shared_refs = {}
        for cluster_id, node_data in self._graph.nodes(data=True):
            if node_data["kind"] == "Cluster":
                ref_edges = defaultdict(int)
                for child in self.children(cluster_id):
                    child_node = self.get_node(child)
                    if child_node.kind == NodeKind.Chunk:
                        try:
                            for _, _, attrs in self._graph.edges(child, data=True):
                                if attrs["kind"] == EdgeKind.ImportToExport:
                                    ref = attrs["ref"]
                                    ref_edges[ref] += 1
                        except Exception:
                            continue
                shared_refs[cluster_id] = ref_edges

        return shared_refs

    def get_chunks(self):
        cluster_dict = {}
        for cluster_id, node_data in self._graph.nodes(data=True):
            if node_data["kind"] == "Cluster":
                concatenated_content = []
                for child in self.children(cluster_id):
                    child_node = self.get_node(child)
                    if child_node.kind == NodeKind.Chunk:
                        # print("CHunk: ", child_node.id)
                        try:
                            chunk_node = self.get_node(child)
                            concatenated_content.append(chunk_node.get_content())
                        except Exception:
                            continue
                cluster_dict[cluster_id] = concatenated_content

        return cluster_dict

    ##### For debugging ####!SECTION
    def nodes(self):
        return self._graph.nodes(data=True)

    def to_str(self):
        repr = ""
        for u, v, attrs in self._graph.edges(data=True):
            ref = attrs["ref"]
            u_node = self.get_node(u)
            v_node = self.get_node(v)
            repr += (
                f"{u_node.metadata.file_name} --{ref}--> {v_node.metadata.file_name}\n"
            )
        return

    def to_str_cluster(self):
        repr = ""
        for node_id, node_data in self._graph.nodes(data=True):
            # print(node_data)
            if node_data["kind"] == "Cluster":
                repr += f"ClusterNode: {node_id}\n"
                for child, _, edge_data in self._graph.in_edges(node_id, data=True):
                    if edge_data["kind"] == EdgeKind.NodeToCluster:
                        chunk_node = self.get_node(child)
                        repr += f"  ChunkNode: {chunk_node.id}\n"
                    elif edge_data["kind"] == EdgeKind.ClusterToCluster:
                        cluster_node = self.get_node(child)
                        repr += f"  ClusterNode: {cluster_node.id}\n"
        return repr

    def to_str_dfs(self):
        INDENT_SYM = lambda d: "-" * d + " " if d > 0 else ""

        def dfs_cluster(cluster_id, depth=0):
            node_data = self._graph.nodes[cluster_id]
            sum_data = node_data.get("summary_data", {})

            if sum_data:
                title = sum_data["title"]
                keywords = ", ".join(sum_data.get("key_variables", [])[:2])
                summary = sum_data.get("summary", "")
            else:
                title = "<MISSING>"
                keywords = "<MISSING>"
                summary = "<MISSING>"

            cluster_reprs = []
            indent = "  " * depth

            repr = f"{INDENT_SYM(depth)}{title} {cluster_id}\n{indent}Keywords: {keywords}\n{indent}Summary: {summary}\n"

            for child, _, edge_data in self._graph.in_edges(cluster_id, data=True):
                if edge_data["kind"] == EdgeKind.NodeToCluster:
                    chunk_node = self.get_node(child)
                    repr += f"{indent}  ChunkNode: {chunk_node.id}\n"
                elif edge_data["kind"] == EdgeKind.ClusterToCluster:
                    cluster_reprs.append(dfs_cluster(child, depth + 1))

            repr += "\n".join(cluster_reprs)
            return repr

        repr = ""
        for node_id, node_data in self._graph.nodes(data=True):
            if node_data["kind"] == "Cluster" and not self.parent(node_id):
                repr += dfs_cluster(node_id)
        return repr

    # def get_import_refs(
    #     self, unresolved_refs: set[str], file_path: Path, scopes: List[ScopeID]
    # ):
    #     # get refs from the local scope that is a file-level import
    #     imported_refs = []
    #     file_imports = self._repo_graph.imports[file_path]

    #     for ref in unresolved_refs:
    #         if ref in [imp.namespace.child for imp in file_imports]:
    #             imported_refs.append(ref)

    #     return imported_refs

    # def unresolved_refs(
    #     self, file_path: Path, chunk_scopes: List[ScopeID]
    # ) -> Tuple[set, set]:
    #     """
    #     Find refs that
    #     """
    #     scope_graph = self.scopes_map[file_path]

    #     resolved = set()
    #     unresolved = set()

    #     # TODO: we also have the check definitions in the parent scope
    #     # TODO: also overlapped scopes/chunk ranges
    #     for scope in chunk_scopes:
    #         refs = [
    #             scope_graph.get_node(r).name
    #             for r in scope_graph.references_by_origin(scope)
    #         ]
    #         local_defs = [
    #             scope_graph.get_node(d).name for d in scope_graph.definitions(scope)
    #         ]

    #         # try to resolve refs with local defs
    #         for ref in refs:
    #             if ref in local_defs:
    #                 resolved.add(ref)
    #             else:
    #                 unresolved.add(ref)

    #     return resolved, unresolved

    # def get_modified_chunks(self):
    #     return self.chunks
