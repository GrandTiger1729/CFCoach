from typing import *
from enum import Enum

class ParticipantType:
    CONTESTANT = 'CONTESTANT'
    PRACTICE = 'PRACTICE'
    VIRTUAL = 'VIRTUAL'
    MANAGER = 'MANAGER'
    OUT_OF_COMPETITION = 'OUT_OF_COMPETITION'

class Member:
    
    handle: str
    name: Optional[str]

    def __init__(self, kwargs):
        self.handle: str = kwargs['handle']
        self.name: Optional[str] = kwargs.get('name')

class Party:

    contestId: Optional[int]
    members: List[Member]
    participantType: ParticipantType
    teamId: int
    teamName: str
    ghost: bool
    room: int
    startTimeSeconds: int

    def __init__(self, kwargs: dict):
        self.contestId: int = kwargs['contestId']
        self.members: List[Member] = list(map(Member, kwargs['members']))
        # self.participantType: ParticipantType = ParticipantType(kwargs['participantType'])
        self.teamId: int = kwargs.get('teamId')
        self.teamName: str = kwargs.get('teamName')
        self.ghost: bool = kwargs['ghost']
        self.room: int = kwargs.get('room')
        self.startTimeSeconds: int = kwargs.get('startTimeSeconds')
