#
# Copyright (c) 2022-present Didier Malenfant <didier@malenfant.net>
#
# This file is part of TraktorBuddy.
#
# TraktorBuddy is free software: you can redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TraktorBuddy is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
# License for more details.
#
# You should have received a copy of the GNU General Public License along with TraktorBuddy. If not,
# see <https://www.gnu.org/licenses/>.
#

from datetime import datetime
from PIL import Image

from .Key import OpenNotation
from .Rating import Rating
from .Color import Color


# -- Class
class FakeTrack:
    """Interface for a Fake Traktor track used by the Listener."""

    def __init__(self, title: str, artist: str):
        """Constructor from a title and an artist."""

        self._title = title
        self._artist = artist

    def updateModificationDateIfModified(self, date: datetime) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def isASample(self) -> bool:
        return False

    def location(self) -> str:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def modificationDate(self) -> datetime:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def title(self) -> str:
        return self._title

    def setTitle(self, value) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def artist(self) -> str:
        return self._artist

    def setArtist(self, value) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def beatgridLocked(self) -> bool:
        return False

    def setBeatGridLocked(self, value: bool) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def beatgridLockModifiedDate(self) -> datetime:
        return None

    def bitrate(self) -> int:
        return None

    def setBitrate(self, value: int) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def genre(self) -> str:
        return None

    def setGenre(self, value: str) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def label(self) -> str:
        return None

    def setLabel(self, value: str) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def producer(self) -> str:
        return self.getValueFromInfoElement('PRODUCER')

    def setProducer(self, value: str) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def mix(self) -> str:
        return None

    def setMix(self, value: str) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def release(self) -> str:
        return None

    def setRelease(self, value: str) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def trackNumber(self) -> int:
        return None

    def setTrackNumber(self, value: int) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def comments(self) -> str:
        return None

    def setComments(self, value: str) -> None:
        self.setValueInInfoElement('COMMENT', value)

    def comments2(self) -> str:
        return None

    def setComments2(self, value: str) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def remixer(self) -> str:
        return None

    def setRemixer(self, value: str) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def key(self) -> str:
        return None

    def setKey(self, value: str) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def playCount(self) -> int:
        return None

    def setPlayCount(self, value: int) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def length(self) -> float:
        return None

    def setLength(self, value: float) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def rating(self) -> Rating:
        return None

    def setRating(self, value: Rating) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def importDate(self) -> datetime:
        return None

    def setImportDate(self, value: datetime) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def lastPlayedDate(self) -> datetime:
        return None

    def setLastPlayedDate(self, value: datetime) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def releaseDate(self) -> datetime:
        return None

    def setReleaseDate(self, value: datetime) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def fileSize(self) -> int:
        return None

    def setFileSize(self, value: int) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def bpm(self) -> float:
        return None

    def setBpm(self, value: float) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def traktorKey(self) -> OpenNotation:
        return None

    def setTraktorKey(self, value: OpenNotation) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def color(self) -> Color:
        return None

    def setColor(self, value: Color) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def coverArtImageFromFile(self) -> Image:
        return None

    def coverArtCacheFile(self, collection_folder_path: str) -> str:
        return None

    def coverArtImageFromCache(self, collection_folder_path: str) -> Image:
        return None
