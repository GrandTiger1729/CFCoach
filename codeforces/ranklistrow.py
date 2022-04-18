from typing import *

from .party import Party
from .problem import ProblemResult

class RanklistRow:

    party: Party
    rank: int
    points: float
    penalty: int
    successfulHackCount: int
    unsuccessfulHackCount: int
    problemResults: List[ProblemResult]
    lastSubmissionTimeSeconds: Optional[int]

    def __init__(self, **kwargs):
        self.party: Party = Party(kwargs['party'])
        self.rank: int = kwargs['rank']
        self.points: float = kwargs['points']
        self.penalty: int = kwargs['penalty']
        self.successfulHackCount: int = kwargs['successfulHackCount']
        self.unsuccessfulHackCount: int = kwargs['unsuccessfulHackCount']
        self.problemResults: List[ProblemResult] = []
        for kw in kwargs['problemResult']:
            self.problemResults.append(ProblemResult(kw))
        self.lastSubmissionTimeSeconds: Optional[int] = kwargs.get('lastSubmissionTimeSeconds')