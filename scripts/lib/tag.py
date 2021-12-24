from typing import Dict

SECTION_SPLITTER = "---\n"

def has_tags_section(doc: str) -> bool:
    return doc.startswith(SECTION_SPLITTER)

def get_tags(doc) -> Dict[str, str]:
    if not has_tags_section(doc): return {}
    lines = doc.split(SECTION_SPLITTER, 3)[1][:-1].split('\n')
    return { name: content for name, content in (line.split(': ') for line in lines) }

def get_tag(doc: str, name: str) -> str:
    return get_tags(doc)[name]

def get_body(doc: str) -> str:
    return doc.split(SECTION_SPLITTER, 3)[-1]

def to_tags_section(tags: Dict[str, str]) -> str:
    return SECTION_SPLITTER + ''.join([f'{name}: {content}\n' for name, content in tags]) + SECTION_SPLITTER

def set_tags(doc: str, tags: Dict[str, str]) -> str:
    tags = {**get_tags(doc), **tags}
    body = get_body(doc)
    return to_tags_section(tags) + body

def set_tag(doc: str, name: str, content: str) -> str:
    tags = get_tags(doc)
    tags[name] = content
    body = get_body(doc)
    return to_tags_section(tags) + body

