from __future__ import annotations
from typing import *

import requests

from .comment import Comment
from .error import CodeForcesException

class BlogEntry:
    
    id: int
    originalLocale: str
    creationTimeSeconds: int
    authorHandle: str
    title: str
    content: Optional[str]
    modificationTimeSeconds: int
    allowViewHistory: bool
    tags: List[str]
    rating: int

    def __init__(self, kwargs: dict):
        self.id: int = kwargs['id']
        self.originalLocale: str = kwargs['originalLocale']
        self.creationTimeSeconds: int = kwargs['creationTimeSeconds']
        self.authorHandle: str = kwargs['authorHandle']
        self.title: str = kwargs['title']
        self.content: Optional[str] = kwargs.get('content')
        self.modificationTimeSeconds: int = kwargs['modificationTimeSeconds']
        self.allowViewHistory: bool = kwargs['allowViewHistory']
        self.tags: List[str] = kwargs['tags']
        self.rating: int = kwargs['rating']

    @classmethod
    def comments(cls, blogEntryId: int) -> List[Comment]:
        response = requests.get('https://codeforces.com/api/blogEntry.comments?', params={'blogEntryId': blogEntryId})
        response.raise_for_status()

        result = response.json()
        if result['status'] == 'FAILED':
            raise CodeForcesException(result['comment'])

        result = result['result']
        return list(map(Comment, result))

    @classmethod
    def view(cls, id: int) -> BlogEntry:
        response = requests.get('https://codeforces.com/api/blogEntry.view?', params={'blogEntryId': id})
        response.raise_for_status()

        result = response.json()
        if result['status'] == 'FAILED':
            raise CodeForcesException(result['comment'])

        result = result['result']
        return cls(**result)