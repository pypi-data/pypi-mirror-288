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

from datetime import datetime
from PIL import Image
from mutagen import File as MutagenFile
from io import BytesIO

from .Utility import Utility
from .Key import OpenNotation
from .Rating import Rating
from .Color import Color


# -- Class
class Track:
    """Interface for Traktor tracks."""

    def __init__(self, entry_element: ET.Element):
        """Constructor from an XML entry element."""

        self._entry_element: ET.Element = entry_element
        self._info_element: ET.Element = self._entry_element.find('INFO')
        self._album_element: ET.Element = self._entry_element.find('ALBUM')
        self._modified: bool = False

    def _entryElement(self) -> ET.Element:
        return self._entry_element

    def _getInfoElement(self) -> ET.Element:
        if self._info_element is None:
            self._info_element = ET.SubElement(self._entry_element, 'INFO')

        return self._info_element

    def _getAlbumElement(self) -> ET.Element:
        if self._album_element is None:
            self._album_element = ET.SubElement(self._entry_element, 'ALBUM')

        return self._album_element

    def _getFromAlbumElement(self, key: str) -> str:
        if self._album_element is None:
            return None

        return self._album_element.get(key)

    def _markAsModified(self) -> None:
        self._modified = True

    def _playlistKey(self) -> str:
        location = self._entry_element.find('LOCATION')

        if location is None:
            return None

        webaddress = location.get('WEBADDRESS')
        if webaddress is not None:
            return webaddress

        volume = location.get('VOLUME')

        if volume is None:
            return None

        directory = location.get('DIR')

        if directory is None:
            return None

        file = location.get('FILE')

        if file is None:
            return None

        return volume + directory + file

    def updateModificationDateIfModified(self, date: datetime) -> None:
        if self._modified is False:
            return

        self._entry_element.set('MODIFIED_DATE', date.strftime('%Y/%m/%d'))
        self._entry_element.set('MODIFIED_TIME', str(date.second + (date.minute * 60) + (date.hour * 3600)))

        self._modified = False

    def getElement(self, name: str) -> ET.Element:
        return self._entry_element.find(name) is not None

    def removeElement(self, name: str):
        element = self._entry_element.find(name)
        if element is not None:
            self._entry_element.remove(element)
            self._markAsModified()

    def getValueFromInfoElement(self, name: str) -> str:
        if self._info_element is None:
            return None

        return self._info_element.get(name)

    def setValueInInfoElement(self, name: str, value: str):
        if self._info_element is None:
            if value is None:
                return

            self._info_element = ET.SubElement(self._entry_element, 'INFO')

        if value is None:
            self._info_element.attrib.pop(name)
        else:
            self._info_element.set(name, value)

        self._markAsModified()

    def isASample(self) -> bool:
        return self._entry_element.find('LOOPINFO') is not None

    def location(self) -> str:
        playlist_key = self._playlistKey()
        if playlist_key is None:
            return None

        if playlist_key.startswith('beatport:'):
            return playlist_key

        return '/Volumes/' + playlist_key.replace('/:', '/')

    def modificationDate(self) -> datetime:
        date = Utility.dateFromString(self._entry_element.get('MODIFIED_DATE'), '%Y/%m/%d')
        if date is None:
            return None

        seconds = Utility.stringToInt(self._entry_element.get('MODIFIED_TIME'))
        if seconds is None:
            return date

        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60

        # -- Traktor modification dates are stored in UTC time.
        return Utility.utcDatetime(date.year, date.month, date.day, hour, minutes, seconds)

    def title(self) -> str:
        return self._entry_element.get('TITLE')

    def setTitle(self, value) -> None:
        self._entry_element.set('TITLE', value)
        self._markAsModified()

    def artist(self) -> str:
        return self._entry_element.get('ARTIST')

    def setArtist(self, value) -> None:
        self._entry_element.set('ARTIST', value)
        self._markAsModified()

    def beatgridLocked(self) -> bool:
        return self._entry_element.get('LOCK') == '1'

    def setBeatGridLocked(self, value: bool) -> None:
        if value is True:
            string = '1'
        else:
            string = '0'

        self._entry_element.set('LOCK', string)
        self._markAsModified()

        date = Utility.utcTimeNow()
        self._entry_element.set('LOCK_MODIFICATION_TIME', date.strftime('%Y-%m-%dT%H:%M:%S'))

    def beatgridLockModifiedDate(self) -> datetime:
        string = self._entry_element.get('LOCK_MODIFICATION_TIME')
        if string is None:
            return None

        return Utility.dateFromString(string, '%Y-%m-%dT%H:%M:%S', utc=True)

    def bitrate(self) -> int:
        return Utility.stringToInt(self.getValueFromInfoElement('BITRATE'))

    def setBitrate(self, value: int) -> None:
        self.setValueInInfoElement('BITRATE', str(value))

    def genre(self) -> str:
        return self.getValueFromInfoElement('GENRE')

    def setGenre(self, value: str) -> None:
        self.setValueInInfoElement('GENRE', value)

    def label(self) -> str:
        return self.getValueFromInfoElement('LABEL')

    def setLabel(self, value: str) -> None:
        self.setValueInInfoElement('LABEL', value)

    def producer(self) -> str:
        return self.getValueFromInfoElement('PRODUCER')

    def setProducer(self, value: str) -> None:
        self.setValueInInfoElement('PRODUCER', value)

    def mix(self) -> str:
        return self.getValueFromInfoElement('MIX')

    def setMix(self, value: str) -> None:
        self.setValueInInfoElement('MIX', value)

    def release(self) -> str:
        return self._getFromAlbumElement('TITLE')

    def setRelease(self, value: str) -> None:
        self.setValueInInfoElement('TITLE', value)

    def trackNumber(self) -> int:
        return Utility.stringToInt(self._getFromAlbumElement('TRACK'))

    def setTrackNumber(self, value: int) -> None:
        self._getAlbumElement().set('TRACK', str(value))
        self._markAsModified()

    def comments(self) -> str:
        return self.getValueFromInfoElement('COMMENT')

    def setComments(self, value: str) -> None:
        self.setValueInInfoElement('COMMENT', value)

    def comments2(self) -> str:
        return self.getValueFromInfoElement('RATING')

    def setComments2(self, value: str) -> None:
        self.setValueInInfoElement('RATING', value)

    def remixer(self) -> str:
        return self.getValueFromInfoElement('REMIXER')

    def setRemixer(self, value: str) -> None:
        self.setValueInInfoElement('REMIXER', value)

    def key(self) -> str:
        return self.getValueFromInfoElement('KEY')

    def setKey(self, value: str) -> None:
        self.setValueInInfoElement('KEY', value)

    def playCount(self) -> int:
        return Utility.stringToInt(self.getValueFromInfoElement('PLAYCOUNT'))

    def setPlayCount(self, value: int) -> None:
        self.setValueInInfoElement('PLAYCOUNT', str(value))

    def length(self) -> float:
        return Utility.stringToFloat(self.getValueFromInfoElement('PLAYTIME_FLOAT'))

    def setLength(self, value: float) -> None:
        self.setValueInInfoElement('PLAYTIME', str(round(value)))
        self.setValueInInfoElement('PLAYTIME_FLOAT', '{:.06f}'.format(value))

    def rating(self) -> Rating:
        # -- The following works with rekordbox and Serato too:
        # --    Unrated -> 0, 1-51 -> 1, 52-102 -> 2, 103-153 -> 3, 154-204 -> 4, 205-anything -> 5
        value = Utility.stringToInt(self.getValueFromInfoElement('RANKING'))

        if value is None:
            return None

        if value == 0:
            return Rating.Unrated
        elif value < 52:
            return Rating.OneStar
        elif value < 103:
            return Rating.TwoStars
        elif value < 154:
            return Rating.ThreeStars
        elif value < 205:
            return Rating.FourStars
        elif value <= 255:
            return Rating.FiveStars

        return None

    def setRating(self, value: Rating) -> None:
        map = {
            Rating.Unrated: 0,
            Rating.OneStar: 51,
            Rating.TwoStars: 102,
            Rating.ThreeStars: 153,
            Rating.FourStars: 205,
            Rating.FiveStars: 255
        }

        self.setValueInInfoElement('RANKING', str(map[value]))

    def importDate(self) -> datetime:
        return Utility.dateFromString(self.getValueFromInfoElement('IMPORT_DATE'), '%Y/%m/%d')

    def setImportDate(self, value: datetime) -> None:
        self.setValueInInfoElement('IMPORT_DATE', value.strftime('%Y/%m/%d'))

    def lastPlayedDate(self) -> datetime:
        return Utility.dateFromString(self.getValueFromInfoElement('LAST_PLAYED'), '%Y/%m/%d')

    def setLastPlayedDate(self, value: datetime) -> None:
        self.setValueInInfoElement('LAST_PLAYED', value.strftime('%Y/%m/%d'))

    def releaseDate(self) -> datetime:
        return Utility.dateFromString(self.getValueFromInfoElement('RELEASE_DATE'), '%Y/%m/%d')

    def setReleaseDate(self, value: datetime) -> None:
        self.setValueInInfoElement('RELEASE_DATE', value.strftime('%Y/%m/%d'))

    def fileSize(self) -> int:
        return Utility.stringToInt(self.getValueFromInfoElement('FILESIZE'))

    def setFileSize(self, value: int) -> None:
        self.setValueInInfoElement('FILESIZE', str(value))

    def bpm(self) -> float:
        tempo_element = self._entry_element.find('TEMPO')
        if tempo_element is None:
            return None

        return Utility.stringToFloat(tempo_element.get('BPM'))

    def setBpm(self, value: float) -> None:
        tempo_element = self._entry_element.find('TEMPO')
        if tempo_element is None:
            tempo_element = ET.SubElement(self._entry_element, 'TEMPO')

        tempo_element.set('BPM', '{:.06f}'.format(value))
        tempo_element.set('BPM_QUALITY', '100.000000')
        self._markAsModified()

    def traktorKey(self) -> OpenNotation:
        key_element = self._entry_element.find('MUSICAL_KEY')
        if key_element is None:
            return None

        value = Utility.stringToInt(key_element.get('VALUE'))
        if value is None:
            return None

        try:
            result = OpenNotation(value)
        except ValueError:
            return None

        return result

    def setTraktorKey(self, value: OpenNotation) -> None:
        key_element = self._entry_element.find('MUSICAL_KEY')
        if key_element is None:
            key_element = ET.SubElement(self._entry_element, 'MUSICAL_KEY')

        key_element.set('VALUE', str(int(value)))
        self._markAsModified()

    def color(self) -> Color:
        value = Utility.stringToInt(self.getValueFromInfoElement('COLOR'))

        if value is None:
            return None

        try:
            result = Color(value)
        except ValueError:
            return None

        return result

    def setColor(self, value: Color) -> None:
        self.setValueInInfoElement('COLOR', str(int(value)))

    def coverArtImageFromFile(self) -> Image:
        track_file_path = self.location()
        if not os.path.exists(track_file_path):
            return None

        try:
            # -- Mutagen can automatically detect format and type of tags
            file = MutagenFile(track_file_path)

            # -- Access APIC frame and grab the image
            tag = file.tags.get('APIC:', None)

            artwork_data = None
            if tag is not None:
                artwork_data = BytesIO(tag.data)
            else:
                cover_list = file.get('covr', None)
                if cover_list is not None and len(cover_list) != 0:
                    # -- We only use the first cover from the list
                    artwork_data = BytesIO(cover_list[0])

            if artwork_data is None:
                return None

            return Image.open(artwork_data)
        except Exception:
            return None

        return None

    def coverArtCacheFile(self, collection_folder_path: str) -> str:
        cover_art_id = self.getValueFromInfoElement('COVERARTID')
        if cover_art_id is None:
            return None

        return os.path.join(collection_folder_path, 'CoverArt', cover_art_id) + '000'

    def coverArtImageFromCache(self, collection_folder_path: str) -> Image:
        database_image_path = self.coverArtCacheFile(collection_folder_path)
        if database_image_path is None or not os.path.exists(database_image_path):
            return None

        artwork_file = open(database_image_path, "rb")
        data = artwork_file.read()
        artwork_file.close()

        if data[0] != 8:
            return None

        width = ((data[4] << 24) | (data[3] << 16) | (data[2] << 8) | data[1])
        height = ((data[8] << 24) | (data[7] << 16) | (data[6] << 8) | data[5])

        rgba_data = bytearray()

        # -- Re-order the color components from little endian data.
        for pixel_index in range(0, width * height):
            data_index = 9 + (pixel_index * 4)

            rgba_data.append(data[data_index + 2])
            rgba_data.append(data[data_index + 1])
            rgba_data.append(data[data_index])
            rgba_data.append(data[data_index + 3])

        return Image.frombytes('RGBA', (width, height), bytes(rgba_data))
