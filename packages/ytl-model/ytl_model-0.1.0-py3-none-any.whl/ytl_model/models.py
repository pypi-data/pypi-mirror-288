from __future__ import annotations

from typing import TypedDict

from pydantic import BaseModel

from .enums import MsgType


type JsonVal = bool | int | float | str | Json | list | None
type Json = dict[str, JsonVal]


class MessageJson(TypedDict):
  type: MsgType
  content: JsonVal


class WithJson(BaseModel):
  @property
  def json(self) -> Json:
    return self.model_dump()


class Message(WithJson):
  type: MsgType
  content: JsonVal = None


class PlaybackData(WithJson):
  state: int
  currentTime: float
  videoId: str
  duration: float

  @staticmethod
  def from_event(state: 'PlaybackState') -> PlaybackData:
    return PlaybackData(
      state=state.state,
      currentTime=state.currentTime,
      videoId=state.videoId,
      duration=state.duration
    )
