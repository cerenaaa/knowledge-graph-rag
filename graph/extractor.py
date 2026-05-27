"""
LLM-based entity and relation extraction.
Extracts (subject, predicate, object) triples from text using Claude.
"""
from __future__ import annotations
import json
import re
from dataclasses import dataclass
import anthropic


@dataclass
class Entity:
    name: str
    entity_type: str    # PERSON, ORG, PRODUCT, CONCEPT, LOCATION
    description: str = ""

@dataclass
class Relation:
    subject: str
    predicate: str
    obj: str
    source_text: str = ""


EXTRACTION_PROMPT = """Extract all entities and relations from this text.
Return ONLY valid JSON:
{
  "entities": [{"name": "string", "type": "PERSON|ORG|PRODUCT|CONCEPT|LOCATION", "description": "string"}],
  "relations": [{"subject": "entity name", "predicate": "VERB_PHRASE", "object": "entity name"}]
}
Rules:
- Normalize entity names (e.g. "Microsoft Corp" -> "Microsoft")
- Use UPPERCASE_SNAKE_CASE for predicates (e.g. WORKS_AT, ACQUIRED, COMPETES_WITH)
- Only extract clearly stated relations, no inference
Text: {text}"""


class KGExtractor:
    def __init__(self, model: str = "claude-sonnet-4-20250514"):
        self.client = anthropic.Anthropic()
        self.model = model

    def extract(self, text: str) -> tuple[list[Entity], list[Relation]]:
        resp = self.client.messages.create(
            model=self.model, max_tokens=1024,
            messages=[{"role": "user", "content": EXTRACTION_PROMPT.format(text=text)}]
        )
        raw = resp.content[0].text.strip()
        raw = re.sub(r"^```(?:json)?\n?", "", raw)
        raw = re.sub(r"\n?```$", "", raw)
        data = json.loads(raw)
        entities = [Entity(**e) for e in data.get("entities", [])]
        relations = [Relation(**r) for r in data.get("relations", [])]
        return entities, relations
