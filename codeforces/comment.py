from typing import *

class Comment:

    id: int
    creationTimeSeconds: int
    commentatorHandle: str
    locale: str
    text: str
    parentCommentId: Optional[int]
    rating: int

    def __init__(self, kwargs: dict):
        self.id: int = kwargs['id']
        self.creationTimeSeconds: int = kwargs['creationTimeSeconds']
        self.commentatorHandle: str = kwargs['commentatorHandle']
        self.locale: str = kwargs['locale']
        self.text: str = kwargs['text']
        self.parentCommentId: Optional[int] = kwargs.get('parentCommentId')
        self.rating: int = kwargs['rating']