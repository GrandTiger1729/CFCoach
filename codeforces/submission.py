from typing import *
from enum import Enum

from .problem import Problem
from .party import Party

class SubmissionType(Enum):
    FAILED = 'FAILED'
    OK = 'OK'
    PARTIAL = 'PARTIAL'
    COMPILATION_ERROR = 'COMPILATION_ERROR'
    RUNTIME_ERROR = 'RUNTIME_ERROR'
    WRONG_ANSWER = 'WRONG_ANSWER'
    PRESENTATION_ERROR = 'PERSENTATION_ERROR'
    TIME_LIMIT_EXCEEDED = 'TIME_LIMIT_EXCEEDED'
    MEMORY_LIMIT_EXCEEDED = 'MEMORY_LIMIT_EXCEEDED'
    IDLENESS_LIMIT_EXCEEDED = 'IDLENESS_LIMIT_EXCEEDED'
    SECURITY_VIOLATED = 'SECURITY_VIOLATED'
    CRASHED = 'CRASHED'
    INPUT_PREPARATION_CRASHED = 'INPUT_PREPARATION_CRASHED'
    CHALLENGED = 'CHALLENGED'
    SKIPPED = 'SKIPPED'
    TESTING = 'TESTING'
    REJECTED = 'REJECTED'

class TestsetType(Enum):
    SAMPLES = 'SAMPLES'
    PRETESTS = 'PRETESTS'
    TESTS = 'TESTS'
    CHALLENGES = 'CHALLENGES'

class Submission:

    id: int
    contestId: Optional[int]
    creationTimeSeconds: int
    relativeTimeSeconds: int
    problem: Problem
    author: Party
    programmingLanguage: str
    verdict: Optional[SubmissionType]
    testset: TestsetType
    passedTestCount: int
    timeConsumedMillis: int
    memoryConsumedBytes: int
    points: float

    def __init__(self, kwargs: dict):
        self.id: int = kwargs['id']
        self.contestId: Optional[int] = kwargs.get('contestId')
        self.creationTimeSeconds: int = kwargs['creationTimeSeconds']
        self.relativeTimeSeconds: int = kwargs['relativeTimeSeconds']
        self.problem: Problem = Problem(kwargs['problem'])
        self.author: Party = Party(kwargs['author'])
        self.programmingLanguage: str = kwargs['programmingLanguage']
        self.verdict: Optional[SubmissionType] = SubmissionType(kwargs['verdict']) if kwargs.get('verdict') else None
        self.testset: TestsetType = TestsetType(kwargs['testset'])
        self.passedTestCount: int = kwargs['passedTestCount']
        self.timeConsumedMillis: int = kwargs['timeConsumedMillis']
        self.memoryConsumedBytes: int = kwargs['memoryConsumedBytes']
        self.points: float = kwargs.get('points')
