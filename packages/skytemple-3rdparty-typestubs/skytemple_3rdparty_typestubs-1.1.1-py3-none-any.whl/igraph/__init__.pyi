from numbers import Number
from typing import (
    Sequence,
    Iterable,
    Any,
    Literal,
    Iterator,
    overload,
    TYPE_CHECKING,
    Self,
)

from typing_extensions import deprecated

ADJ_DIRECTED: int
ADJ_LOWER: int
ADJ_MAX: int
ADJ_MIN: int
ADJ_PLUS: int
ADJ_UNDIRECTED: int
ADJ_UPPER: int
ALL: int
BLISS_F: int
BLISS_FL: int
BLISS_FLM: int
BLISS_FM: int
BLISS_FS: int
BLISS_FSM: int
GET_ADJACENCY_BOTH: int
GET_ADJACENCY_LOWER: int
GET_ADJACENCY_UPPER: int
IN: int
INTEGER_SIZE: int
LOOPS_SW: int
MULTI_SW: int
OUT: int
REWIRING_SIMPLE: int
REWIRING_SIMPLE_LOOPS: int
SIMPLE_SW: int
STAR_IN: int
STAR_MUTUAL: int
STAR_OUT: int
STAR_UNDIRECTED: int
STRONG: int
TRANSITIVITY_NAN: int
TRANSITIVITY_ZERO: int
TREE_IN: int
TREE_OUT: int
TREE_UNDIRECTED: int
WEAK: int

if TYPE_CHECKING:
    _Mode = Literal["out"] | Literal["in"] | Literal["all"] | OUT | IN | ALL


class GraphBase:
    def add_edges(self, es: Iterable[Edge]): ...
    def add_vertices(self, n: int): ...
    def delete_edges(self, es: Iterable[int | Edge] | EdgeSeq | int | Edge): ...
    def delete_vertices(self, vs: Iterable[int | Vertex] | int | Vertex): ...
    def are_adjacent(self, v1: str | int, v2: str | int): ...
    def incident(self, vertex: str | int | Vertex, mode: _Mode) -> list[int]: ...
    @overload
    def bfsiter(
        self, vid: int | Vertex, mode: _Mode = ..., advanced: Literal[False] = ...
    ) -> Iterator[Vertex]: ...
    @overload
    def bfsiter(
        self, vid: int | Vertex, mode: _Mode = ..., advanced: Literal[True] = ...
    ) -> Iterator[tuple[Number, Vertex]]: ...
    def bfsiter(
        self, vid: int | Vertex, mode: _Mode = ..., advanced: bool = False
    ) -> Iterator[Vertex] | Iterator[tuple[Number, Vertex]]: ...
    def are_adjacent(self, v1: int | str, v2: int | str) -> bool: ...
    def get_eid(
        self, v1: int | str, v2: int | str, directed: bool = ..., error: bool = ...
    ) -> int: ...
    def copy(self) -> Self: ...
    def get_shortest_path(
        self,
        v: Vertex | int,
        to: Vertex | int,
        weights: list[int] | str | None = None,
        mode: _Mode = ...,
        output: str = ...,
        algorithm: str = ...,
    ) -> list[int]: ...
    def get_shortest_paths(
        self,
        v: Vertex | int,
        to: Vertex | int,
        weights: list[int] | str | None = None,
        mode: _Mode = ...,
        output: str = ...,
        algorithm: str = ...,
    ) -> list[list[int]]: ...


class Graph(GraphBase):
    vs: VertexSeq
    es: EdgeSeq

    def __init__(
        self,
        *,
        n: int = 0,
        edges: list[tuple[int, int]] | None = None,
        directed: bool = False,
        graph_attrs: dict[str, str] | None = None,
        vertex_attrs: dict[str, Iterable[str]] | None = None,
        edge_attrs: dict[str, Iterable[str]] | None = None,
    ): ...
    def add_edge(
        self, source: Vertex | str | int, target: Vertex | str | int, **attributes: Any
    ) -> Edge: ...
    def add_vertex(self, name: str | None = None, **attributes: Any) -> Vertex: ...
    @deprecated("use Graph.are_adjacent() instead")
    def are_connected(self, v1: int | str, v2: int | str) -> bool: ...
    def get_all_simple_paths(
        self,
        v: Vertex | int | str,
        to: Vertex
        | Sequence[Vertex]
        | int
        | Sequence[int]
        | str
        | Sequence[str]
        | VertexSeq
        | None = None,
        cutoff: int = ...,
        mode=_Mode,
    ) -> list[list[int]]: ...


class Edge:
    index: int
    graph: Graph
    source: int
    source_vertex: Vertex
    target: int
    target_vertex: Vertex

    def attributes(self) -> dict[str, Any]: ...
    def __getitem__(self, key: str) -> Any: ...
    def __setitem__(self, key: str, value: Any): ...


class Vertex:
    index: int
    graph: Graph

    def out_edges(self) -> list[Edge]: ...
    def in_edges(self) -> list[Edge]: ...
    def attributes(self) -> dict[str, Any]: ...
    def __getitem__(self, key: str) -> Any: ...
    def __setitem__(self, key: str, value: Any): ...


class VertexSeq:
    def __iter__(self) -> Iterator[Vertex]: ...
    def __len__(self) -> int: ...
    def __getitem__(self, index: int | Vertex) -> Vertex: ...
    def __contains__(self, index: int | Vertex): ...


class EdgeSeq:
    def __iter__(self) -> Iterator[Edge]: ...
    def __len__(self) -> int: ...
    def __getitem__(self, index: int | Edge) -> Edge: ...
    def __contains__(self, index: int | Edge): ...
