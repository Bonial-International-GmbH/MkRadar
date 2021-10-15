''' Module to hoald usefull dataclasses '''
from dataclasses import dataclass
from datetime import datetime


@dataclass(eq=True)
class MarkdownPage:
    ''' Class to hoald information of a markdown file '''
    pk: int
    url: str
    markdown_file_path: str
    file_content_hash: str
    category: str
    title: str
    latest_update: str
