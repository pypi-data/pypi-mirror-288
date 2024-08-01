''' Fetch data from pretalx '''
from datetime import datetime
from typing import Any, Generator, List

import arrow
from pydantic import BaseModel, Field, parse_obj_as, validator
from requests import Session


def convert_datetime(value: Any) -> datetime:
    ''' convert `action_date` to date '''
    return arrow.get(value).datetime


class Speaker(BaseModel):
    ''' Speaker '''
    code: str = Field(default_factory=str)
    name: str = Field(default_factory=str)
    biography: str | None = Field(default_factory=str)
    avatar: str | None = Field(default_factory=str)
    submissions: list[str] | None = Field(default_factory=list)
    email: str | None = Field(default_factory=str)
    availabilities: list[dict[str, Any]] = Field(default_factory=list)


class Slot(BaseModel):
    ''' Slot in talk '''
    start: datetime = Field(default_factory=datetime.now,
                            description='Start time')
    end: datetime = Field(default_factory=datetime.now, description='End time')
    room: dict[str, str] = Field(default_factory=dict, description='Room name')
    room_id: int = Field(default=0, description='Room ID')

    _validate_convert_datetime = validator(
        'start', 'end',
        pre=True, allow_reuse=True, always=True)(convert_datetime)


class AnsQuestion(BaseModel):
    ''' Question in answers '''
    id: int = Field(default_factory=int)
    question: dict[str, str] = Field(default_factory=dict)


class Answer(BaseModel):
    ''' Answers in talk '''
    id: int = Field(default_factory=int)
    answer: str = Field(default_factory=str)
    submission: str = Field(default_factory=str)
    question: AnsQuestion = Field(default_factory=AnsQuestion)


class Talk(BaseModel):
    ''' Talk '''
    # pylint: disable=no-self-argument
    code: str = Field(default_factory=str,
                      description='A unique, alphanumeric identifier, also used in URLs')
    title: str = Field(default_factory=str,
                       description='The submission’s title')
    track: dict[str, str] = Field(description='The track this talk belongs to')
    track_id: int = Field(default_factory=int,
                          description='ID of the track this talk belongs to')
    submission_type: dict[str, str] | None = Field(
        description='The submission type')
    state: str = Field(default_factory=str,
                       description='The submission’s state, one of '
                                   '“submitted”, “accepted”, “rejected”, “confirmed”')
    abstract: str = Field(default_factory=str,
                          description='The abstract, a short note of the submission’s content')
    duration: int = Field(
        default_factory=int, description='The talk’s duration in minutes, or null')
    content_locale: str = Field(
        default_factory=str, description='The language the submission is in, e.g. “en” or “de”')
    slot: Slot = Field(default_factory=Slot,
                       description='The datetime in talk')
    speakers: list[Speaker] = Field(
        default_factory=list, description='A list of speaker objects')
    answers: list[Answer] | None = Field()

    @validator('track', pre=True)
    def verify_track(cls, value: Any) -> dict[str, str]:
        ''' verify track '''
        if value is None:
            return {'en': 'no track'}

        return dict(value)

    @validator('answers')
    def verify_answers(cls, value: Any, values: Any) -> None:
        ''' Verify answers '''
        if value is None:
            return None

        for ans in value:
            if ans.question.id != 216:
                continue

            if '中文' in ans.answer or 'Chinese' in ans.answer:
                values['content_locale'] = '中文 Chinese'
            elif '英文' in ans.answer or 'English' in ans.answer:
                values['content_locale'] = '英文 English'
            else:
                values['content_locale'] = '其他 Others'

            break

        return None


class Submission(BaseModel):
    ''' Submission '''
    # pylint: disable=no-self-argument
    code: str = Field(default_factory=str,
                      description='A unique, alphanumeric identifier, also used in URLs')
    speakers: list[Speaker] = Field(
        default_factory=list, description='A list of speaker objects')
    title: str = Field(default_factory=str,
                       description='The submission’s title')
    track: dict[str, str] = Field(
        description='The track this talk belongs to')
    track_id: int | None = Field(
        description='ID of the track this talk belongs to')
    submission_type: dict[str, str] | None = Field(
        description='The submission type')
    state: str = Field(
        description='The submission’s state, one of '
                    '“submitted”, “accepted”, “rejected”, “confirmed”')
    abstract: str = Field(
        description='The abstract, a short note of the submission’s content')
    duration: int = Field(
        default_factory=int, description='The talk’s duration in minutes, or null')
    content_locale: str = Field(
        default_factory=str, description='The language the submission is in, e.g. “en” or “de”')
    notes: str | None = Field(default='', description='note')
    internal_notes: str | None = Field(
        description='Notes the organisers left on the submission.'
                    'Available if the requesting user has organiser permissions.')

    @validator('track', pre=True)
    def verify_track(cls, value: Any) -> dict[str, str]:
        ''' verify track '''
        if value is None:
            return {'en': 'no track'}

        return dict(value)


class Room(BaseModel):
    ''' Room '''
    id: int = Field(default_factory=int,
                    description="The unique ID of the room object")
    name: str = Field(default_factory=str, description='The name of the room')
    description: str = Field(
        default_factory=str, description='The description of the room')
    capacity: int = Field(default_factory=int,
                          description='How many people fit in the room')
    position: int = Field(
        default_factory=int, description='A number indicating the ordering of '
                                         'the room relative to other rooms, '
                                         'e.g. in schedule visualisations')
    speaker_info: str = Field(default_factory=str)
    availabilities: list[dict[str, Any]] = Field(default_factory=list)


class PretalxResponse(BaseModel):
    ''' PretalxResponse '''
    count: int
    next: str | None
    previous: str | None
    results: List[dict[str, Any]]


class Pretalx(Session):
    ''' Pretalx '''

    def __init__(self, domain: str, event: str, token: str) -> None:
        super().__init__()
        self.url = f'https://{domain}/api/events/{event}'
        self.headers['Authorization'] = f'Token {token}'

    def fetch_all(self, path: str) -> Generator[PretalxResponse, None, None]:
        ''' Fetch all '''
        result = self.get(url=self.url+path, params={'limit': 50}).json()
        yield PretalxResponse.parse_obj(result)

        while 'next' in result and result['next']:
            result = self.get(result['next']).json()
            yield PretalxResponse.parse_obj(result)

    def talks(self) -> Generator[list[Talk], None, None]:
        ''' Fetch talks '''
        for resp in self.fetch_all(path='/talks'):
            yield parse_obj_as(list[Talk], resp.results)

    def submissions(self) -> Generator[list[Submission], None, None]:
        ''' Fetch submissions '''
        for resp in self.fetch_all(path='/submissions'):
            yield parse_obj_as(list[Submission], resp.results)

    def speakers(self) -> Generator[list[Speaker], None, None]:
        ''' Fetch speakers '''
        for resp in self.fetch_all(path='/speakers'):
            yield parse_obj_as(list[Speaker], resp.results)

    def rooms(self) -> Generator[list[Room], None, None]:
        ''' Fetch rooms '''
        for resp in self.fetch_all(path='/rooms'):
            yield parse_obj_as(list[Room], resp.results)
