"""End-to-end Knowledge Graph RAG demo."""
import os
from data.synthetic_docs import get_documents
from graph.graph_store import PropertyGraph, Node, Edge
from graph.traversal import get_graph_context

# Minimal demo without API call — just show graph construction + traversal
def build_graph_manually() -> PropertyGraph:
    """Pre-built graph from DOCUMENTS to demo without API key."""
    g = PropertyGraph()
    nodes = [
        Node("Microsoft", "ORG", "Technology company"), Node("Bill Gates", "PERSON", "Co-founder of Microsoft"),
        Node("Satya Nadella", "PERSON", "CEO of Microsoft"), Node("GitHub", "ORG", "Code hosting platform"),
        Node("OpenAI", "ORG", "AI research company"), Node("Sam Altman", "PERSON", "CEO of OpenAI"),
        Node("Anthropic", "ORG", "AI safety company"), Node("Claude", "PRODUCT", "LLM by Anthropic"),
        Node("Dario Amodei", "PERSON", "CEO of Anthropic"), Node("Amazon", "ORG", "Technology company"),
        Node("GPT-4", "PRODUCT", "LLM by OpenAI"), Node("Transformer", "CONCEPT", "Neural architecture"),
    ]
    for n in nodes:
        g.add_node(n)
    edges = [
        Edge("Bill Gates", "FOUNDED", "Microsoft"),
        Edge("Satya Nadella", "IS_CEO_OF", "Microsoft"),
        Edge("Microsoft", "ACQUIRED", "GitHub"),
        Edge("Microsoft", "INVESTED_IN", "OpenAI"),
        Edge("Sam Altman", "IS_CEO_OF", "OpenAI"),
        Edge("OpenAI", "DEVELOPED", "GPT-4"),
        Edge("Dario Amodei", "FOUNDED", "Anthropic"),
        Edge("Anthropic", "DEVELOPED", "Claude"),
        Edge("Amazon", "INVESTED_IN", "Anthropic"),
        Edge("GPT-4", "BASED_ON", "Transformer"),
    ]
    for e in edges:
        g.add_edge(e)
    return g

def main():
    print("Building knowledge graph...")
    graph = build_graph_manually()
    print(f"Graph stats: {graph.stats}")

    queries = [
        "Who founded Microsoft?",
        "What has Anthropic built?",
        "What did Microsoft acquire?",
    ]
    for q in queries:
        ctx = get_graph_context(q, graph)
        print(f"\nQ: {q}")
        print(f"Context:\n{ctx[:300]}")

if __name__ == "__main__":
    main()
