from typing import *
from enum import Enum

from .party import Party
from .problem import Problem

class HackType(Enum):
    (HACK_SUCCESSFUL, HACK_UNSUCCESSFUL, INVALID_INPUT, GENERATOR_INCOMPILABLE, GENERATOR_CRASHED, IGNORED, TESTING, OTHER) = range(1, 9)

class JudgeProtocol:

    manual: bool
    protocol: str
    verdict: HackType

class Hack:

    id: int
    creationTimeSeconds: int
    hacker: Party
    defender: Party
    verdict: Optional[HackType]
    problem: Problem
    test: Optional[str]
    judgeProtocol: Optional[JudgeProtocol]

    def __init__(self, kwargs: dict):
        self.id: int = kwargs['id']
        self.creationTimeSeconds: int = kwargs['creationTimeSeconds']
        self.hacker: Party = Party(kwargs['hacker'])
        self.defender: Party = Party(kwargs['defender'])
        self.verdict: Optional[HackType] = HackType(kwargs['verdict']) if kwargs.get('verdict') else None
        self.problem: Problem = Problem(kwargs['problem'])
        self.test: Optional[str] = kwargs.get('test')
        self.judgeProtocol: Optional[JudgeProtocol] = JudgeProtocol(kwargs['judgeProtocol']) if kwargs.get('judegProtocol') else None