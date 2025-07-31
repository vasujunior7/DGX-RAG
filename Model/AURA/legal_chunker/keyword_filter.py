import re
from typing import List

LEGAL_KEYWORDS = [
    'confidentiality', 'liability', 'termination', 'indemnity', 'governing law',
    'dispute', 'arbitration', 'warranty', 'intellectual property', 'force majeure',
    'assignment', 'notices', 'severability', 'entire agreement', 'amendment',
]

def contains_legal_keyword(text: str) -> bool:
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in LEGAL_KEYWORDS)

def further_split(text: str, min_length: int = 200) -> List[str]:
    # Split by sentences if possible, else by paragraphs
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    chunk = ''
    for sentence in sentences:
        if len(chunk) + len(sentence) < min_length:
            chunk += ' ' + sentence
        else:
            if chunk:
                chunks.append(chunk.strip())
            chunk = sentence
    if chunk:
        chunks.append(chunk.strip())
    return [c for c in chunks if c] 