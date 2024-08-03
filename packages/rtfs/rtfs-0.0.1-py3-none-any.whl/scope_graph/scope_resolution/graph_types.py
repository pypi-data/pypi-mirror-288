from typing import Dict, Optional, NewType
from enum import Enum
from pydantic import root_validator

from scope_graph.graph import Node
from scope_graph.utils import TextRange
import random
import string


class NodeKind(str, Enum):
    SCOPE = "LocalScope"
    DEFINITION = "LocalDef"
    IMPORT = "Import"
    REFERENCE = "Reference"


class EdgeKind(str, Enum):
    ScopeToScope = "ScopeToScope"
    DefToScope = "DefToScope"
    ImportToScope = "ImportToScope"
    RefToDef = "RefToDef"
    RefToOrigin = "RefToOrigin"
    RefToImport = "RefToImport"


class ScopeNode(Node):
    # jank..
    id: str = "".join(random.choices(string.ascii_letters, k=6))
    range: TextRange
    type: NodeKind
    name: Optional[str] = ""
    data: Optional[Dict] = {}


ScopeID = NewType("ScopeID", int)
