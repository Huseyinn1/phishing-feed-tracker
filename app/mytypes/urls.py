from dataclasses import dataclass

@dataclass
class URL:
    url_id: str
    url: str
    url_author: str
    source: str