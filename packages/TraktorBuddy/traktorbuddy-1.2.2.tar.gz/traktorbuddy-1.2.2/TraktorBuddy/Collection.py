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

import os

import xml.etree.ElementTree as ET

from typing import List
from semver import VersionInfo
from time import sleep
from pathlib import Path

from .Utility import Utility
from .Track import Track
from .TrackList import TrackList
from .Folder import Folder
from .Exceptions import ArgumentError


# -- Classes
class Collection:
    """Interface for Traktor collection."""

    def __init__(self, collection_path: str = None, _mock_element: ET.Element = None):
        """Constructor from a collection path, or it will just use the latest collection if no path is provided."""

        self._nml_element = None

        if _mock_element is None:
            if collection_path is None:
                self._collection_path = Collection.traktorCollectionFilePath()

                if self._collection_path is None:
                    raise RuntimeError('Error: Could not find any Traktor folder in \'' + Collection.nativeInstrumentsFolderPath() + '\'.')
            else:
                self._collection_path = collection_path

            self._collection_folder_path = Path(self._collection_path).parent

            print('Parsing Traktor collection in \'' + self._collection_path + '\'.')

            self._nml_element = ET.ElementTree(file=self._collection_path).getroot()
        else:
            self._nml_element = _mock_element

        self._track_list = TrackList(self._nml_element.find('COLLECTION'))

    def folderPath(self) -> str:
        return self._collection_folder_path

    def makeBackup(self):
        # -- Backups filename have a timestamp so we make sure to wait so that names cannot clash.
        sleep(1)

        backup_folder = Collection.traktorCollectionBackupFolderPath()
        os.makedirs(backup_folder, exist_ok=True)

        arguments: List[str] = ['zip', '-j', Utility.utcTimeNow().strftime('%Y-%m-%d-%H-%M-%S.zip'), self._collection_path]
        Utility.shellCommand(arguments, backup_folder)

    def save(self):
        self.makeBackup()

        date = Utility.utcTimeNow()

        for track in self.tracks():
            track.updateModificationDateIfModified(date)

        with open(self._collection_path, 'w') as out_file:
            out_file.write(Utility.xmlElementToString(self._nml_element, xml_declaration=True))

        print('Saved Traktor collection in \'' + self._collection_path + '\'.')

    def findAllTracksAtPath(self, path: str) -> List[Track]:
        crate = self.rootFolder().find(path.split('/'))
        if crate is None:
            raise RuntimeError('Could not find any folder or playlist at \'' + path + '\'.')
        else:
            return crate.tracks()

    def tracks(self) -> List[Track]:
        return self._track_list.tracks()

    def numberOfTracks(self) -> int:
        return len(self._track_list.tracks())

    def trackAtIndex(self, index: int) -> Track:
        if index >= self.numberOfTracks():
            raise ArgumentError("Out of bound access to a track.")

        return self._track_list.tracks()[index]

    def rootFolder(self) -> Folder:
        playlists_element: ET.Element = self._nml_element.find('PLAYLISTS')
        if playlists_element is None:
            return None

        root_node: ET.Element = playlists_element.find('NODE')
        if root_node is None:
            return None

        return Folder(self._track_list, root_node)

    def trackWithPlaylistKey(self, key) -> Track:
        return self._track_list.trackWithPlaylistKey(key)

    @classmethod
    def purgeBackups(cls, test_mode: bool = False):
        backup_folder: str = Collection.traktorCollectionBackupFolderPath()
        backup_list: List[str] = os.listdir(backup_folder)

        nb_of_backups: int = len(backup_list)
        if nb_of_backups < 2:
            print('No backups to purge.')
            return

        if test_mode is False:
            backup_list.sort()

            for file in backup_list[:-1]:
                os.remove(os.path.join(backup_folder, file))

        print('Purged ' + str(nb_of_backups - 1) + ' backup(s).')

    @classmethod
    def traktorCollectionBackupFolderPath(cls) -> str:
        return os.path.join(Collection.latestTraktorFolderPath(), 'Backup', 'TraktorBuddy')

    @classmethod
    def nativeInstrumentsFolderPath(cls) -> str:
        return os.path.join(os.path.expanduser('~'), 'Documents', 'Native Instruments')

    @classmethod
    def latestTraktorFolderPath(cls) -> str:
        base_folder = Collection.nativeInstrumentsFolderPath()

        lastest_version = None

        for path in os.listdir(base_folder):
            if not path.startswith('Traktor '):
                continue

            try:
                version = VersionInfo.parse(path[8:])

                if lastest_version is None or version > lastest_version:
                    lastest_version = version
            except ValueError:
                continue

        if lastest_version is None:
            return None

        return os.path.join(base_folder, 'Traktor ' + str(lastest_version))

    @classmethod
    def traktorCollectionFilePath(cls) -> str:
        return os.path.join(Collection.latestTraktorFolderPath(), 'collection.nml')
