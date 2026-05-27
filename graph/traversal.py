"""Graph traversal strategies for context retrieval."""
from __future__ import annotations
from graph.graph_store import PropertyGraph


def extract_entities_from_query(query: str, graph: PropertyGraph) -> list[str]:
    """Simple entity linking: find graph nodes mentioned in the query."""
    query_lower = query.lower()
    return [name for name in graph.nodes if name in query_lower]


def get_graph_context(query: str, graph: PropertyGraph, depth: int = 2, max_chars: int = 2000) -> str:
    """Build graph-derived context string for a query."""
    entities = extract_entities_from_query(query, graph)
    if not entities:
        return ""
    contexts = []
    for entity in entities[:3]:
        ctx = graph.subgraph_text(entity, depth=depth)
        contexts.append(f"[Graph context for '{entity}']\n{ctx}")
    combined = "\n\n".join(contexts)
    return combined[:max_chars]
