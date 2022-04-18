from __future__ import annotations
from typing import *
import requests

from .blogentry import BlogEntry
from .comment import Comment
from .error import CodeForcesException

class RecentAction:
    
    timeSeconds: int
    blogEntry: Optional[BlogEntry]
    comment: Optional[Comment]

    def __init__(self, kwargs):
        self.timeSeconds: int = kwargs['timeSeconds']
        self.blogEntry: Optional[BlogEntry] = kwargs.get('blogEntry')
        self.comment: Optional[Comment] = kwargs.get('comment')
    
    @classmethod
    def recentActions(cls, maxCount) -> List[RecentAction]:
        response = requests.get('https://codeforces.com/api/problemset.recentStatus?', params={'maxCount': maxCount})
        response.raise_for_status()

        result = response.json()
        if result['status'] == 'FAILED':
            raise CodeForcesException(result['comment'])
        
        result = result['result']
        return list(map(cls, result))