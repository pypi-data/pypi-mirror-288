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

from .TrackList import TrackList
from .Playlist import Playlist
from .Track import Track


# -- Class
class Folder:
    """Interface for Traktor folders."""

    def __init__(self, track_list: TrackList, node_element: ET.Element):
        """Constructor from an XML entry element."""

        self._node_element: ET.Element = node_element
        self._track_list: TrackList = track_list
        self._folders: List[Folder] = None
        self._playlists: List[Playlist] = None

    def name(self) -> str:
        return self._node_element.get('NAME')

    def find(self, names: List[str]):
        name: str = names[0]
        nb_of_names: int = len(names)

        for playlist in self.playlists():
            if playlist.name() == name:
                if nb_of_names == 1:
                    return playlist

        for folder in self.folders():
            if folder.name() == name:
                if nb_of_names == 1:
                    return folder
                else:
                    return folder.find(names[1:])

        return None

    def findFolder(self, names: List[str]):
        result = self.find(names)
        if type(result) != Folder:
            return None

        return result

    def findPlaylist(self, names: List[str]):
        result = self.find(names)
        if type(result) != Playlist:
            return None

        return result

    def folders(self) -> List['Folder']:
        if self._folders is not None:
            return self._folders

        self._folders = []

        subnodes: ET.Element = self._node_element.find('SUBNODES')
        if subnodes is None:
            return self._folders

        for node in subnodes.findall('NODE'):
            if node.get('TYPE') != 'FOLDER':
                continue

            self._folders.append(Folder(self._track_list, node))

        return self._folders

    def playlists(self) -> List[Playlist]:
        if self._playlists is not None:
            return self._playlists

        self._playlists = []

        subnodes: ET.Element = self._node_element.find('SUBNODES')
        if subnodes is None:
            return self._playlists

        for node in subnodes.findall('NODE'):
            if node.get('TYPE') != 'PLAYLIST':
                continue

            self._playlists.append(Playlist(self._track_list, node))

        return self._playlists

    def tracks(self) -> List[Track]:
        result: List[Track] = []

        for folder in self.folders():
            result = result + folder.tracks()

        for playlist in self.playlists():
            result = result + playlist.tracks()

        return result
