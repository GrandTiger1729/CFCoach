from __future__ import annotations
from typing import *

import requests

from .error import CodeForcesException
from .blogentry import BlogEntry
from .ratingchange import RatingChange
from .submission import Submission

class User:

    handle: str
    email: str
    vkId: str
    openId: str
    firstName: Optional[str]
    lastName: Optional[str]
    country: Optional[str]
    city: Optional[str]
    organization: Optional[str]
    contribution: int
    rank: str
    rating: int
    maxRank: str
    maxRating: int
    lastOnlineTimeSeconds: int
    registrationTimeSeconds: int
    friendOfCount: int
    avatar: str
    titlePhoto: str

    def __init__(self, kwargs: dict):
        self.handle: str = kwargs['handle']
        self.email: str = kwargs['email']
        self.vkId: str = kwargs['vkId']
        self.openId: str = kwargs['openId']
        self.firstName: Optional[str] = kwargs.get('firstName')
        self.lastName: Optional[str] = kwargs.get('lastName')
        self.country: Optional[str] = kwargs.get('country')
        self.city: Optional[str] = kwargs.get('city')
        self.organization: Optional[str] = kwargs.get('organization')
        self.contribution: int = kwargs['contribution']
        self.rank: str = kwargs['rank']
        self.rating: int = kwargs['rating']
        self.maxRank: str = kwargs['maxRank']
        self.maxRating: int = kwargs['maxRating']
        self.lastOnlineTimeSeconds: int = kwargs['lastOnlineTimeSeconds']
        self.registrationTimeSeconds: int = kwargs['registrationTimeSeconds']
        self.friendOfCount: int = kwargs['friendOfCount']
        self.avatar: str = kwargs['avatar']
        self.titlePhoto: str = kwargs['titlePhoto']

    @classmethod
    def blogEntries(cls, handle: str) -> List[BlogEntry]:
        response = requests.get('https://codeforces.com/api/user.blogEntries?', params={'handle': handle})
        response.raise_for_status()

        result = response.json()
        if result['status'] == 'FAILED':
            raise CodeForcesException(result['comment'])

        result = result['result']
        return list(map(BlogEntry, result))

    def friends(self, onlyOnline: bool):
        '''require api key, under development'''

    @classmethod
    def info(cls, handles: List[str]) -> List[User]:
        response = requests.get('https://codeforces.com/api/user.info?', params={'handles': ';'.join(handles)})
        response.raise_for_status()

        result = response.json()
        if result['status'] == 'FAILED':
            raise CodeForcesException(result['comment'])

        result = result['result']
        return list(map(cls, result))

    @classmethod
    def ratedList(cls, activeOnly: Optional[bool] = None, includeRetired: Optional[bool] = None, contestId: Optional[int] = None) -> List[User]:
        options: dict = {}
        if activeOnly is not None:
            options.update('activeOnly', activeOnly)
        if includeRetired is not None:
            options.update('includeRetired', includeRetired)
        if contestId is not None:
            options.update('contestId', contestId)
        
        response = requests.get('https://codeforces.com/api/user.ratedList?', params=options)
        response.raise_for_status()

        result = response.json()
        if result['status'] == 'FAILED':
            raise CodeForcesException(result['comment'])

        result = result['result']
        return list(map(User, result))

    @classmethod
    def Rating(cls, handle: str) -> List[RatingChange]:
        response = requests.get('https://codeforces.com/api/user.rating?', params={'handle': handle})
        response.raise_for_status()

        result = response.json()
        if result['status'] == 'FAILED':
            raise CodeForcesException(result['comment'])

        result = result['result']
        return list(map(RatingChange, result))

    @classmethod
    def status(cls, handle: str, _from: Optional[int] = None, _count: Optional[int] = None) -> List[Submission]:
        options: dict = {'handle': handle}
        if _from is not None:
            options['from'] = _from
        if _count is not None:
            options['count'] =  _count
        
        response = requests.get('https://codeforces.com/api/user.status?', params=options)
        response.raise_for_status()

        result = response.json()
        if result['status'] == 'FAILED':
            raise CodeForcesException(result['comment'])

        result = result['result']
        return list(map(Submission, result))
