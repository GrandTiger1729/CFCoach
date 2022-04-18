from typing import *
from enum import Enum

class ProblemType(Enum):
    PROGRAMMING = 'PROGRAMMING'
    QUESTION = 'QUESTION'

class Problem:

    contestId: int
    problemsetName: Optional[str]
    index: str
    name: str
    type: ProblemType
    points: float
    rating: int
    tags: List[str]

    url: str

    def __init__(self, kwargs: dict):
        self.contestId: int = kwargs['contestId']
        self.problemsetName: Optional[str] = kwargs.get('problemsetName')
        self.index: str = kwargs['index']
        self.name: str = kwargs['name']
        self.type: ProblemType = ProblemType(kwargs['type'])
        self.points: float = kwargs.get('points')
        self.rating: int = kwargs.get('rating')
        self.tags: List[str] = kwargs['tags']

        self.url: str = f'https://codeforces.com/contest/{self.contestId}/problem/{self.index}'

class ProblemStatistics:
    
    contestId: Optional[int]
    index: str
    solvedCount: int

    def __init__(self, kwargs):
        self.contestId: Optional[int] = kwargs['contestId']
        self.index: str = kwargs['index']
        self.solvedCount: int = kwargs['solvedCount']

class ProblemResultType(Enum):
    (PRELIMINARY, FINAL) = range(1, 3)

class ProblemResult:

    points: float
    penalty: Optional[int]
    rejectedAttemptCount: int
    type: ProblemResultType
    bestSubmissionTimeSeconds: Optional[int]

    def __init__(self, **kwargs):
        self.points: float = kwargs['points']
        self.penalty: Optional[int] = kwargs.get('penalty')
        self.rejectedAttemptCount: int = kwargs['rejectedAttemptCount']
        self.type: ProblemResultType = ProblemResultType(kwargs['type'])
        self.bestSubmissionTimeSeconds: Optional[int] = kwargs['bestSubmissionTimeSeconds']