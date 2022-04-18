from typing import *
import requests

class RatingChange:
    
    contestId: int
    contestName: str
    handle: str
    rank: int
    ratingUpdateTimeSeconds: int
    oldRating: int
    newRating: int

    def __init__(self, kwargs):
        self.contestId: int = kwargs['contestId']
        self.contestName: str = kwargs['contestName']
        self.handle: str = kwargs['handle']
        self.rank: int = kwargs['rank']
        self.ratingUpdateTimeSeconds: int = kwargs['ratingUpdateTimeSeconds']
        self.oldRating: int = kwargs['oldRating']
        self.newRating: int = kwargs['newRating']