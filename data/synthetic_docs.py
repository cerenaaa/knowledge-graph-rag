"""Synthetic corporate knowledge base for graph extraction testing."""

DOCUMENTS = [
    "Microsoft was founded by Bill Gates and Paul Allen in 1975. Satya Nadella became CEO in 2014. Microsoft acquired GitHub in 2018 and Activision Blizzard in 2023.",
    "OpenAI developed GPT-4 and ChatGPT. Microsoft invested $10 billion in OpenAI. Sam Altman is the CEO of OpenAI and was briefly fired and reinstated in 2023.",
    "Google DeepMind was formed when Google merged Google Brain and DeepMind in 2023. Demis Hassabis leads Google DeepMind. DeepMind developed AlphaFold which predicts protein structures.",
    "Anthropic was founded by Dario Amodei and Daniela Amodei after leaving OpenAI. Anthropic built Claude, a large language model focused on safety. Amazon invested $4 billion in Anthropic.",
    "The transformer architecture was introduced in the paper Attention Is All You Need by researchers at Google. BERT and GPT are both based on the transformer architecture.",
]

def get_documents() -> list[dict]:
    return [{"doc_id": f"doc_{i}", "text": t} for i, t in enumerate(DOCUMENTS)]
