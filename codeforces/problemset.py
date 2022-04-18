from typing import *
from enum import Enum

import requests

from .error import CodeForcesException
from .problem import Problem, ProblemStatistics
from .submission import Submission

class Problemset:
    @classmethod
    def problems(cls, tags: Optional[List[str]] = None, problemsetName: Optional[str] = None) -> Tuple[List[Problem], List[ProblemStatistics]]:
        options: dict = {}
        if tags is not None:
            if tags[0] == '*combine tags by OR':
                options['tags'] = '&tags='.join(tags[1:])
            else:
                options['tags'] = ';'.join(tags)
        if problemsetName is not None:
            options.update('problemsetName', problemsetName)
        
        response = requests.get('https://codeforces.com/api/problemset.problems?', params='&'.join(f'{k}={v}' for k, v in options.items()))
        response.raise_for_status()

        result = response.json()
        if result['status'] == 'FAILED':
            raise CodeForcesException(result['comment'])

        result = result['result']
        problems = list(map(Problem, result['problems']))
        problem_statistics = list(map(ProblemStatistics, result['problemStatistics']))

        return (problems, problem_statistics)

    @classmethod
    def recentStatus(cls, count: int, *, problemsetName: Optional[str] = None) -> List[Submission]:
        options: dict = {'count': count}
        if problemsetName == None:
            options.update('problemsetName', problemsetName)
        
        response = requests.get('https://codeforces.com/api/problemset.recentStatus?', params=options)
        response.raise_for_status()

        result = response.json()
        if result['status'] == 'FAILED':
            raise CodeForcesException(result['comment'])
        
        result = result['result']
        return list(map(Submission, result))