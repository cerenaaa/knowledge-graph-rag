"""
In-memory property graph.
Nodes represent entities, edges represent relations.
Supports subgraph extraction and neighborhood queries.
"""
from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Node:
    name: str
    entity_type: str
    description: str = ""
    properties: dict = field(default_factory=dict)

@dataclass
class Edge:
    source: str
    predicate: str
    target: str
    weight: float = 1.0
    source_doc: str = ""


class PropertyGraph:
    def __init__(self):
        self.nodes: dict[str, Node] = {}
        self.edges: list[Edge] = []
        self._adj: dict[str, list[Edge]] = defaultdict(list)
        self._radj: dict[str, list[Edge]] = defaultdict(list)

    def add_node(self, node: Node):
        key = node.name.lower()
        if key not in self.nodes:
            self.nodes[key] = node
        elif not self.nodes[key].description and node.description:
            self.nodes[key].description = node.description

    def add_edge(self, edge: Edge):
        self.edges.append(edge)
        self._adj[edge.source.lower()].append(edge)
        self._radj[edge.target.lower()].append(edge)

    def neighbors(self, entity: str, depth: int = 1) -> list[Node]:
        """BFS to collect all nodes within `depth` hops."""
        visited, queue = set(), [(entity.lower(), 0)]
        result = []
        while queue:
            name, d = queue.pop(0)
            if name in visited or d > depth:
                continue
            visited.add(name)
            if name in self.nodes:
                result.append(self.nodes[name])
            for edge in self._adj.get(name, []) + self._radj.get(name, []):
                next_node = edge.target.lower() if edge.source.lower() == name else edge.source.lower()
                if next_node not in visited:
                    queue.append((next_node, d + 1))
        return result

    def subgraph_text(self, entity: str, depth: int = 2) -> str:
        """Render subgraph around an entity as readable text for LLM context."""
        nodes = self.neighbors(entity, depth)
        node_names = {n.name.lower() for n in nodes}
        relevant_edges = [e for e in self.edges
                          if e.source.lower() in node_names and e.target.lower() in node_names]
        lines = [f"Entities: {', '.join(n.name for n in nodes)}",
                 "Relations:"]
        for e in relevant_edges:
            lines.append(f"  {e.source} --[{e.predicate}]--> {e.target}")
        return "\n".join(lines)

    @property
    def stats(self) -> dict:
        return {"nodes": len(self.nodes), "edges": len(self.edges)}
