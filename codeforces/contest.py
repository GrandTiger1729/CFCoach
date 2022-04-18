from __future__ import annotations
from enum import Enum
from typing import *

import requests
from scipy.__config__ import show

from .error import CodeForcesException
from .hack import Hack
from .ratingchange import RatingChange
from .problem import Problem
from .ranklistrow import RanklistRow
from .submission import Submission

class ContestType(Enum):
    CF = 'CF'
    IOI = 'IOI'
    ICPC = 'ICPC'

class ContestPhase(Enum):
    BEFORE = 'BEFORE'
    CODING = 'CODING'
    PENDING_SYSTEM_TEST = 'PENDING_SYSTEM_TEST'
    SYSTEM_TEST = 'SYSTEM_TEST'
    FINISHED = 'FINISHED'

class Contest:

    id: int
    name: str
    type: ContestType
    frozen: bool
    durationSeconds: int
    startTimeSeconds: int
    relativeTimeSeconds: int
    preparedBy: str
    websiteUrl: str
    description: str
    difficulty: int
    kind: str
    icpcRegion: str
    conntry: str
    city: str
    season: str

    @classmethod
    def hacks(cls, contestId: int) -> List[Hack]:
        response = requests.get('https://codeforces.com/api/contest.hacks?', params={'contestId': contestId})
        response.raise_for_status()

        result = response.json()
        if result['status'] == 'FAILED':
            raise CodeForcesException(result['comment'])

        result = result['result']
        return list(map(Hack, result))

    @classmethod
    def list(cls, gym: bool) -> List[Contest]:
        response = requests.get('https://codeforces.com/api/contest.list?', params={'gym': gym})
        response.raise_for_status()

        result = response.json()
        if result['status'] == 'FAILED':
            raise CodeForcesException(result['comment'])

        return list(map(cls, result['result']))

    @classmethod
    def ratingChanges(cls, contestId: int) -> List[RatingChange]:
        response = requests.get('https://codeforces.com/api/contest.ratingChanges?', params={'contestId': contestId})
        response.raise_for_status()

        result = response.json()
        if result['status'] == 'FAILED':
            raise CodeForcesException(result['comment'])

        return list(map(RatingChange, result['result']))
    
    @classmethod
    def standings(cls,
        contestId: int, 
        _from: Optional[int] = None, 
        _to: Optional[int] = None, 
        handles: Optional[List[str]] = None,
        room: Optional[int] = None,
        showUnofficial: Optional[bool] = None
    ) -> Tuple[Contest, List[Problem], List[RanklistRow]]:
        options: dict = {'contestId': contestId}
        if _from is not None:
            options.update('from', _from)
        if _to is not None:
            options.update('from', _to)
        if handles is not None:
            options.update('from', ';'.join(handles))
        if room is not None:
            options.update('from', room)
        if showUnofficial is not None:
            options.update('from', showUnofficial)
        response = requests.get('https://codeforces.com/api/contest.standings?', params=options)
        response.raise_for_status()

        result = response.json()
        if result['status'] == 'FAILED':
            raise CodeForcesException(result['comment'])

        result = result['result']
        contest: Contest = cls(result['contest'])
        problems: List[Problem] = list(map(Problem, result['problems']))
        rows: List[RanklistRow] = list(map(Problem, result['rows']))
        
        return (contest, problems, rows)

    @classmethod   
    def status(self, contestId: int, _from: Optional[int] = None, _to: Optional[int] = None) -> List[Submission]:
        options: dict = {'contestId', contestId}
        if _from is not None:
            options.update('from', _from)
        if _to is not None:
            options.update('from', _to)
        response = requests.get('https://codeforces.com/api/contest.status?', params=options)
        response.raise_for_status()

        result = response.json()
        if result['status'] == 'FAILED':
            raise CodeForcesException(result['comment'])

        return list(map(Submission, result['result']))
