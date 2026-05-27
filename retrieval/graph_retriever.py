"""
Hybrid retriever: graph traversal for structured facts + vector search fallback.
"""
from __future__ import annotations
import anthropic
from graph.graph_store import PropertyGraph
from graph.traversal import get_graph_context


class GraphRAGRetriever:
    def __init__(self, graph: PropertyGraph, model: str = "claude-sonnet-4-20250514"):
        self.graph = graph
        self.client = anthropic.Anthropic()
        self.model = model

    def answer(self, question: str) -> dict:
        graph_ctx = get_graph_context(question, self.graph)
        source = "graph" if graph_ctx else "parametric"

        prompt = (
            f"Use the following knowledge graph context to answer the question.\n\n"
            f"Context:\n{graph_ctx}\n\n" if graph_ctx else ""
        ) + f"Question: {question}"

        resp = self.client.messages.create(
            model=self.model, max_tokens=512,
            messages=[{"role": "user", "content": prompt}]
        )
        return {
            "question": question,
            "answer": resp.content[0].text.strip(),
            "context_source": source,
            "graph_context": graph_ctx[:300] if graph_ctx else None,
        }
