import re
from typing import List, Tuple

def split_by_section_headers(text: str) -> List[Tuple[str, str]]:
    """
    Splits text into sections based on numbered headers (e.g., '1. Introduction', '2.1 Confidentiality').
    Returns a list of (header, section_text) tuples.
    """
    # Regex for headers like '1. Title', '2.1 Subtitle', '10.2.3 Subsection', etc.
    pattern = re.compile(r'(^|\n)(\d+(?:\.\d+)*\s+[^\n]+)', re.MULTILINE)
    matches = list(pattern.finditer(text))
    sections = []
    for i, match in enumerate(matches):
        start = match.start(2)
        end = matches[i+1].start(2) if i+1 < len(matches) else len(text)
        header = match.group(2).strip()
        section_text = text[start:end].strip()
        sections.append((header, section_text))
    return sections 