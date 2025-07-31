from .section_splitter import split_by_section_headers
from .recursive_splitter import recursive_split
from .keyword_filter import contains_legal_keyword, further_split
from typing import List
from concurrent.futures import ProcessPoolExecutor

def smart_legal_chunk(text: str) -> List[str]:
    chunks = []
    sections = split_by_section_headers(text)
    if not sections:
        # No headers found, use recursive splitter
        for chunk in recursive_split(text):
            if contains_legal_keyword(chunk):
                chunks.append(chunk.strip())
            else:
                chunks.extend(further_split(chunk))
        return [c.strip() for c in chunks if c.strip()]
    for header, section_text in sections:
        if contains_legal_keyword(section_text):
            chunks.append(section_text.strip())
        else:
            for chunk in recursive_split(section_text):
                if contains_legal_keyword(chunk):
                    chunks.append(chunk.strip())
                else:
                    chunks.extend(further_split(chunk))
    return [c.strip() for c in chunks if c.strip()]

def process_section(section_tuple):
    from .recursive_splitter import recursive_split
    from .keyword_filter import contains_legal_keyword, further_split
    header, section_text = section_tuple
    if contains_legal_keyword(section_text):
        return [section_text.strip()]
    else:
        subchunks = recursive_split(section_text)
        filtered = [c.strip() for c in subchunks if contains_legal_keyword(c)]
        if filtered:
            return filtered
        else:
            further = []
            for chunk in subchunks:
                further.extend(further_split(chunk))
            return [c.strip() for c in further if c.strip()]

def parallel_smart_legal_chunk(text: str, max_workers: int = 4) -> List[str]:
    sections = split_by_section_headers(text)
    if not sections:
        # No headers found, use recursive splitter in parallel
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            chunks = list(executor.map(recursive_split, [text]))
        flat_chunks = [item for sublist in chunks for item in sublist]
        return [c.strip() for c in flat_chunks if contains_legal_keyword(c) and c.strip()]
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(process_section, sections))
    flat_chunks = [item for sublist in results for item in sublist]
    return [c for c in flat_chunks if c] 