# Knowledge Graph RAG

[![CI](https://github.com/cerenaaa/knowledge-graph-rag/actions/workflows/ci.yml/badge.svg)](https://github.com/cerenaaa/knowledge-graph-rag/actions)

Extract entities and relations from text, build a property graph, and use it to augment LLM retrieval. Combines structured graph traversal with dense vector search for richer context grounding.

## Why GraphRAG over plain RAG?

| Scenario | Plain RAG | GraphRAG |
|---|---|---|
| "Who works with Alice?" | Misses if not in same chunk | Traverses `WORKS_WITH` edges |
| Multi-hop questions | Fails on 2+ hops | Graph traversal handles it |
| Entity disambiguation | Struggles | Nodes are deduplicated |
| Relationship queries | Unreliable | First-class graph query |

## Architecture

```
Documents → Entity/Relation Extraction → Property Graph
                                              ↓
Query → Entity Linking → Graph Traversal → Context Assembly → Claude → Answer
             +
         Vector Search (fallback)
```

## Structure
```
knowledge-graph-rag/
├── graph/
│   ├── extractor.py       # LLM-based entity + relation extraction
│   ├── graph_store.py     # In-memory property graph (nodes, edges, attributes)
│   └── traversal.py       # BFS/DFS graph traversal for context retrieval
├── retrieval/
│   └── graph_retriever.py # Hybrid: graph traversal + vector fallback
├── data/
│   └── synthetic_docs.py  # Synthetic knowledge corpus
└── run.py
```

## Quickstart
```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key
python run.py
```
