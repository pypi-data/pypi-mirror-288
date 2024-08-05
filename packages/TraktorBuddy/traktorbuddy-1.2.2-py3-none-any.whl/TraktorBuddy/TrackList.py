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

import xml.etree.ElementTree as ET

from typing import List

from .Track import Track


# -- Class
class TrackList:
    """Interface for Traktor track list inside a collection."""

    def __init__(self, collection_element: ET.Element):
        """Constructor from an XML collection element."""

        self._collection_element: ET.Element = collection_element
        self._tracks: List[Track] = None

    def tracks(self) -> List[Track]:
        if self._collection_element is None:
            return []

        if self._tracks is not None:
            return self._tracks

        self._tracks = []

        for entry in self._collection_element.findall('ENTRY'):
            track = Track(entry)
            if track.location() is not None:
                self._tracks.append(track)

        return self._tracks

    def trackWithPlaylistKey(self, key) -> Track:
        for track in self.tracks():
            if track._playlistKey() == key:
                return track

        return None
