#
# Copyright (c) 2022-present Didier Malenfant <didier@malenfant.net>
#
# This file is part of
#
# TraktorBuddy is free software: you can redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TraktorBuddy is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
# License for more details.
#
# You should have received a copy of the GNU General Public License along with  If not,
# see <https://www.gnu.org/licenses/>.
#

import getopt
import sys
import os
import traceback
import time

from typing import List
from mutagen import File as MutagenFile
from pathlib import Path

from .__about__ import __version__
from .Exceptions import ArgumentError
from .Collection import Collection
from .Track import Track
from .Utility import Utility
from .Listener import Listener


_test_mode: bool = False
_verbose_mode: bool = False


def fix(_commands: List[str]) -> None:
    switch = {
        'labels': [fixLabels, 2, 3],
        'itunes': [fixItunes, 2, 3],
        'coverart': [fixCoverArt, 2, 3],
        'covercache': [fixCoverCache, 2, 2]
    }

    sub_command = _commands[1]
    method = switch.get(sub_command)
    if method is None:
        raise ArgumentError('Unknown argument \'' + sub_command + '\' to \'fix\' command.')

    nb_of_commands: int = len(_commands)
    if nb_of_commands < method[1]:
        raise ArgumentError('Expected an argument to \'fix\' command.')
    elif nb_of_commands > method[2]:
        raise ArgumentError('Too many arguments to \'fix\' command.')

    collection = Collection()
    tracks = collection.tracks() if nb_of_commands == method[1] else collection.findAllTracksAtPath(_commands[method[1]])
    method[0](collection, tracks)


def fixLabels(collection: Collection, tracks: List[Track]) -> None:
    global _test_mode
    global _verbose_mode

    nb_of_tracks_checked: int = 0
    nb_of_tracks_with_no_labels: int = 0
    nb_of_tracks_fixed: int = 0

    for track in tracks:
        if track.isASample():
            continue

        nb_of_tracks_checked += 1

        if track.label() is not None:
            continue

        nb_of_tracks_with_no_labels += 1

        file = MutagenFile(track.location())
        if file.tags is None:
            continue

        grouping = file.tags.get('©grp')
        if grouping is not None:
            if len(grouping) > 0:
                if _test_mode is False:
                    track.setLabel(grouping[0])

                nb_of_tracks_fixed += 1
        else:
            printed_location = False

            for tag in file.tags:
                if tag.startswith('APIC') or tag.startswith('PRIV:') or tag.startswith('GEOB:') or tag.startswith('POPM:') or tag.startswith('covr'):
                    continue
                if tag.startswith('©too'):
                    continue
                if tag.startswith('disk'):
                    continue
                if tag.startswith('©day'):
                    continue
                if tag.startswith('©nam'):
                    continue
                if tag.startswith('©alb'):
                    continue
                if tag.startswith('©ART'):
                    continue
                if tag.startswith('©gen'):
                    continue
                if tag.startswith('tmpo'):
                    continue
                if tag.startswith('----:com.apple.iTunes:initialkey'):
                    continue
                if tag.startswith('----:com.apple.iTunes:rating wmp'):
                    continue
                if tag.startswith('cpil'):
                    continue
                if tag.startswith('©cmt'):
                    continue
                if tag.startswith('TSSE'):
                    continue
                if tag.startswith('TPE1'):
                    continue
                if tag.startswith('TCMP'):
                    continue
                if tag.startswith('TIT2'):
                    continue
                if tag.startswith('TCON'):
                    continue
                if tag.startswith('TKEY'):
                    continue
                if tag.startswith('COMM::eng'):
                    continue
                if tag.startswith('TDRC'):
                    continue
                if tag.startswith('TBPM'):
                    continue
                if tag.startswith('TDOR'):
                    continue
                if tag.startswith('TDRL'):
                    continue
                if tag.startswith('TPE4'):
                    continue
                if tag.startswith('TENC'):
                    continue
                if tag.startswith('©wrt'):
                    continue
                if tag.startswith('trkn'):
                    continue
                if tag.startswith('TLEN'):
                    continue
                if tag.startswith('TXXX'):
                    continue
                if tag.startswith('TALB'):
                    continue
                if tag.startswith('TXXX'):
                    continue
                if tag.startswith('TRCK'):
                    continue
                if tag.startswith('aART'):
                    continue
                if tag.startswith('RVA2:SeratoGain'):
                    continue
                if tag.startswith('COMM:ID3v1 Comment'):
                    continue
                if tag.startswith('TSOT'):
                    continue
                if tag.startswith('TSOA'):
                    continue
                if tag.startswith('----:com.apple.iTunes:energylevel'):
                    continue
                if tag.startswith('----:com.apple.iTunes:iTunNORM'):
                    continue
                if tag.startswith('----:com.apple.iTunes:iTunSMPB'):
                    continue
                if tag.startswith('apID'):
                    continue
                if tag.startswith('cnID'):
                    continue
                if tag.startswith('ownr'):
                    continue
                if tag.startswith('plID'):
                    continue
                if tag.startswith('purd'):
                    continue
                if tag.startswith('stik'):
                    continue
                if tag.startswith('----:com.apple.iTunes:iTunMOVI'):
                    continue
                if tag.startswith('sonm'):
                    continue
                if tag.startswith('COMM:iTunSMPB:eng'):
                    continue
                if tag.startswith('COMM:iTunNORM:eng'):
                    continue
                if tag.startswith('TPOS'):
                    continue
                if tag.startswith('atID'):
                    continue
                if tag.startswith('geID'):
                    continue
                if tag.startswith('soal'):
                    continue
                if tag.startswith('soar'):
                    continue
                if tag.startswith('soco'):
                    continue
                if tag.startswith('----:com.apple.iTunes:Encoding Params'):
                    continue
                if tag.startswith('UFID:http://www.jhutveckling.se'):
                    continue
                if tag.startswith('GRP1'):
                    continue
                if tag.startswith('TIT1'):
                    continue
                if tag.startswith('rtng'):
                    continue
                if tag.startswith('cprt'):
                    continue
                if tag.startswith('sfID'):
                    continue
                if tag.startswith('xid '):
                    continue
                if tag.startswith('cmID'):
                    continue
                if tag.startswith('pgap'):
                    continue
                if tag.startswith('----:com.apple.iTunes:iTunes_CDDB_TrackNumber'):
                    continue

                if _verbose_mode is True:
                    if printed_location is False:
                        printed_location = True
                        print(track.location())

                    print("%s: %s" % (tag, file.tags[tag]))

    if _test_mode:
        print('Checked %d tracks. %d with no labels. %d of them can be fixed.' % (nb_of_tracks_checked, nb_of_tracks_with_no_labels, nb_of_tracks_fixed))
    else:
        print('Checked %d tracks. %d with no labels. Fixed %d of them.' % (nb_of_tracks_checked, nb_of_tracks_with_no_labels, nb_of_tracks_fixed))

    if _test_mode is False and nb_of_tracks_fixed > 0:
        collection.save()


def fixItunes(collection: Collection, tracks: List[Track]) -> None:
    global _test_mode
    global _verbose_mode

    nb_of_tracks_checked: int = 0
    nb_of_tracks_with_itunes_info: int = 0

    for track in tracks:
        if track.isASample():
            continue

        nb_of_tracks_checked += 1

        if track.getElement('ITUNES') is not None:
            continue

        nb_of_tracks_with_itunes_info += 1

        if _verbose_mode is True:
            print(track.location())

        if _test_mode is False:
            track.removeElement('ITUNES')

    if _test_mode:
        print('Checked %d tracks. %d with iTunes info tags.' % (nb_of_tracks_checked, nb_of_tracks_with_itunes_info))
    else:
        print('Checked %d tracks. Removed iTunes info tags from %d of them.' % (nb_of_tracks_checked, nb_of_tracks_with_itunes_info))

    if _test_mode is False and nb_of_tracks_with_itunes_info > 0:
        collection.save()


def fixCoverArt(collection: Collection, tracks: List[Track]) -> None:
    global _test_mode
    global _verbose_mode

    nb_of_tracks_checked: int = 0
    nb_of_tracks_with_missing_coverart_in_cache: int = 0
    track_filepaths_to_touch: List[str] = []

    for track in tracks:
        if track.isASample():
            continue

        nb_of_tracks_checked += 1

        cache_image_path = track.coverArtCacheFile(collection.folderPath())
        if cache_image_path is not None and os.path.exists(cache_image_path):
            continue

        if cache_image_path is None:
            file_coverart_image = track.coverArtImageFromFile()
            if file_coverart_image is None:
                continue

            file_coverart_image.close()

        nb_of_tracks_with_missing_coverart_in_cache += 1

        track_file_path = track.location()
        if _verbose_mode is True:
            print(track_file_path)

        if os.path.exists(track_file_path):
            track_filepaths_to_touch.append(track_file_path)

        if _test_mode is False:
            if cache_image_path is not None:
                track.setValueInInfoElement('COVERARTID', None)

    if _test_mode:
        print('Checked %d tracks. %d with missing or invalid cache coverart.' % (nb_of_tracks_checked, nb_of_tracks_with_missing_coverart_in_cache))
    else:
        print('Checked %d tracks. Removed invalid coverart ID from %d of them.' % (nb_of_tracks_checked, nb_of_tracks_with_missing_coverart_in_cache))

    if _test_mode is False and nb_of_tracks_with_missing_coverart_in_cache > 0:
        collection.save()

        # -- We need Traktor to spot that the track file is newer than the date in the collection
        time.sleep(5)

        for path in track_filepaths_to_touch:
            Path(path).touch()


def fixCoverCache(collection: Collection, tracks: List[Track]) -> None:
    global _test_mode
    global _verbose_mode

    cache_folder_path = os.path.join(collection.folderPath(), 'CoverArt')
    cache_files_found = {}

    nb_of_cache_entries: int = 0
    nb_of_orphan_cache_entries: int = 0

    for track in tracks:
        cache_file = track.coverArtCacheFile(collection.folderPath())
        if cache_file is None:
            continue

        cache_files_found[str(Path(cache_file).relative_to(cache_folder_path))[:-3]] = True

        nb_of_cache_entries += 1

    for p in Path(cache_folder_path).rglob('*'):
        if not os.path.isdir(p):
            continue

        for p in Path(p).rglob('*'):
            if os.path.isdir(p):
                continue

            cache_file = str(p.relative_to(cache_folder_path))[:-3]
            if cache_file in cache_files_found:
                continue

            nb_of_orphan_cache_entries += 1

            if _verbose_mode is True:
                print(str(p.relative_to(cache_folder_path)))

            if _test_mode is False:
                os.remove(p)

    if _test_mode:
        print('Checked %d cache entries. %d of wich are orphans.' % (nb_of_cache_entries, nb_of_orphan_cache_entries))
    else:
        print('Checked %d tracks. Deleted %d orphans.' % (nb_of_cache_entries, nb_of_orphan_cache_entries))


def tag(_commands: List[str]) -> None:
    if len(_commands) < 2:
        raise ArgumentError('Expected an argument to \'tag\' command.')

    switch = {
        'add': addTag,
        'remove': removeTag,
        'rename': renameTag,
        'years': addYearTag
    }

    sub_command = _commands[1]
    method = switch.get(sub_command)
    if method is None:
        raise ArgumentError('Unknown argument \'' + sub_command + '\' to \'tag\' command.')

    method(_commands)


def addTag(_commands: List[str]) -> None:
    global _test_mode
    global _verbose_mode

    nb_of_commands: int = len(_commands)
    if nb_of_commands > 4:
        raise ArgumentError('Too many arguments to \'add\' command.')
    elif nb_of_commands < 3:
        raise ArgumentError('Expected name argument to \'add\' command.')

    tag_name: str = _commands[2]
    if tag_name.__contains__(' '):
        raise ArgumentError('Tag names should not contain spaces.')

    collection = Collection()
    tracks = collection.tracks() if nb_of_commands == 3 else collection.findAllTracksAtPath(_commands[3])

    nb_of_tracks_tagged: int = 0
    for track in tracks:
        if track.isASample():
            continue

        existing_value: str = track.comments2()
        if existing_value is None:
            existing_value = tag_name
        elif tag_name in existing_value.split(' '):
            continue
        else:
            existing_value += ' ' + tag_name

        track.setComments2(existing_value)
        nb_of_tracks_tagged += 1

        if _verbose_mode is True:
            print(track.location())

    print('Tagged ' + str(nb_of_tracks_tagged) + ' tracks.')
    if _test_mode is False and nb_of_tracks_tagged > 0:
        collection.save()


def removeTag(_commands: List[str]) -> None:
    global _test_mode
    global _verbose_mode

    nb_of_commands: int = len(_commands)
    if nb_of_commands > 4:
        raise ArgumentError('Too many arguments to \'remove\' command.')
    elif nb_of_commands < 3:
        raise ArgumentError('Expected name argument to \'remove\' command.')

    tag_name: str = _commands[2]
    if tag_name.__contains__(' '):
        raise ArgumentError('Tag names should not contain spaces.')

    collection = Collection()
    tracks = collection.tracks() if nb_of_commands == 3 else collection.findAllTracksAtPath(_commands[3])

    nb_of_tracks_tagged: int = 0
    for track in tracks:
        if track.isASample():
            continue

        existing_value: str = track.comments2()
        if existing_value is None:
            continue

        names = existing_value.split(' ')
        if tag_name not in names:
            continue

        names.remove(tag_name)
        track.setComments2(" ".join(names))
        nb_of_tracks_tagged += 1

        if _verbose_mode is True:
            print(track.location())

    print('Removed tag from ' + str(nb_of_tracks_tagged) + ' tracks.')
    if _test_mode is False and nb_of_tracks_tagged > 0:
        collection.save()


def renameTag(_commands: List[str]) -> None:
    global _test_mode
    global _verbose_mode

    nb_of_commands: int = len(_commands)
    if nb_of_commands > 5:
        raise ArgumentError('Too many arguments to \'rename\' command.')
    elif nb_of_commands < 4:
        raise ArgumentError('Expected old and new name arguments to \'rename\' command.')

    old_tag_name: str = _commands[2]
    if old_tag_name.__contains__(' '):
        raise ArgumentError('Tag names should not contain spaces.')

    new_tag_name: str = _commands[3]
    if new_tag_name.__contains__(' '):
        raise ArgumentError('Tag names should not contain spaces.')

    collection = Collection()
    tracks = collection.tracks() if nb_of_commands == 4 else collection.findAllTracksAtPath(_commands[4])

    nb_of_tracks_tagged: int = 0
    for track in tracks:
        if track.isASample():
            continue

        existing_value: str = track.comments2()
        if existing_value is None:
            continue

        names = existing_value.split(' ')
        if old_tag_name not in names:
            continue

        names.remove(old_tag_name)
        track.setComments2(" ".join(names) + ' ' + new_tag_name)
        nb_of_tracks_tagged += 1

        if _verbose_mode is True:
            print(track.location())

    print('Renamed tag in ' + str(nb_of_tracks_tagged) + ' tracks.')
    if _test_mode is False and nb_of_tracks_tagged > 0:
        collection.save()


def addYearTag(_commands: List[str]) -> None:
    global _test_mode
    global _verbose_mode

    nb_of_commands: int = len(_commands)
    if nb_of_commands > 4:
        raise ArgumentError('Too many arguments to \'years\' command.')
    elif nb_of_commands < 3:
        raise ArgumentError('Expected old and new name arguments to \'rename\' command.')

    collection = Collection()
    tracks = collection.tracks() if nb_of_commands == 3 else collection.findAllTracksAtPath(_commands[3])

    nb_of_tracks_tagged: int = 0
    for track in tracks:
        if track.isASample():
            continue

        release_date = track.releaseDate()
        if release_date is None:
            continue

        year: int = track.releaseDate().year
        if year == 0:
            continue

        tag_name: str = 'Year:' + str(year)

        existing_value: str = track.comments2()
        if existing_value is None:
            existing_value = tag_name
        elif tag_name in existing_value.split(' '):
            continue
        else:
            existing_value += ' ' + tag_name

        if _test_mode is True:
            track.setComments2(existing_value)

        nb_of_tracks_tagged += 1

        if _verbose_mode is True:
            print(track.location())

    print('Tagged ' + str(nb_of_tracks_tagged) + ' tracks.')
    if _test_mode is False and nb_of_tracks_tagged > 0:
        collection.save()


def purgeBackups(_commands: List[str]) -> None:
    global _test_mode

    Collection.purgeBackups(test_mode=_test_mode)


def _new_track_posted(track: Track) -> None:
    label = track.label()
    if label is None:
        print(f'Playing "{track.title()}" by {track.artist()}.')
    else:
        print(f'Playing "{track.title()}" by {track.artist()} [{label}].')


def listen(_commands: List[str]) -> None:
    nb_of_commands: int = len(_commands)
    if nb_of_commands > 2:
        raise ArgumentError('Too many arguments to \'listen\' command.')

    collection: Collection = Collection()

    print('Listening to Traktor... (press CTRL-C to quit)')
    listener = Listener(collection, _new_track_posted)
    listener.start()


def printUsage(_commands: List[str]) -> None:
    method = None

    if len(_commands) > 1:
        switch = {
            'topics': printTopics,
            'tag': printTagUsage,
            'fix': printFixUsage,
            'license': printLicense
        }

        method = switch.get(_commands[1])
        if method is None:
            raise ArgumentError('Error: Unknown topic \'' + _commands[1] + '\'.')

        method()
        return

    printVersion()
    print('')
    print('usage: tktbud <options> <command> <arguments> <path>')
    print('')
    print('The following commands are supported:')
    print('')
    print('   help <topic>       - Show a help message. topic is optional (use \'help topics\' for a list).')
    print('   version            - Print the current version.')
    print('   tag <arguments>    - Add or remove tags (use \'help tag\' for a list of arguments).')
    print('   purge              - Purge all collection backups apart from the most recent one.')
    print('   listen             - Listen to tracks playing on Traktor and print info about them.')
    print('')
    print('The following options are supported:')
    print('')
    print('   --test/-t          - Run in test mode. Affected tracks are printed out. No changes are saved.')
    print('   --debug/-d         - Enable extra debugging information.')
    print('   --verbose/-v       - Enable verbose mode (prints information on the tracks affected).')
    print('')
    print('If path is provided then the action is only applied to the track contained in the Playlist/Folder at that path. Paths are / separated, i.e. \'/Folder1/Folder2/Playlist\'. Use \'\\ \' for spaces.')
    print('')
    print('If no path is provided the action is applied to ALL tracks in the collection.')
    print('')
    print('TraktorBuddy is free software, type "tktbud help license" for license information.')


def printVersion() -> None:
    print('🎧 Traktor Buddy v' + __version__ + ' 🎧')


def printTopics() -> None:
    printVersion()
    print('')
    print('Usage:')
    print('   tktbud help tag     - List arguments accepted by the tag command.')
    print('   tktbud help fix     - List arguments accepted by the fix command.')
    print('   tktbud help license - Show the license for the app.')
    print('')


def printTagUsage() -> None:
    printVersion()
    print('')
    print('Usage:')
    print('   tktbud tag add <name> <path>          - Add a tag named \'name\' to all tracks in \'path\'.')
    print('   tktbud tag delete <name> <path>       - Delete a tag named \'name\' for all tracks in \'path\'.')
    print('   tktbud tag rename <old> <new> <path>  - Rename tags named \'old\' to \'new\' for tracks in \'path\'.')
    print('   tktbud tag years <path>               - Add track\'s release year as a tag (i.e. Year:2022).')
    print('')


def printFixUsage() -> None:
    printVersion()
    print('')
    print('Usage:')
    print('   tktbud fix labels <path>   - Grab missing record labels from the track file\'s grouping field for all tracks in \'path\'.')
    print('   tktbud fix itunes <path>   - Delete iTunes info, if present, for all tracks in \'path\'.')
    print('   tktbud fix coverart <path> - Force Traktor to reload the coverart if the cached file is missing for all tracks in \'path\'.')
    print('   tktbud fix covercache      - Remove any files in the coverart cache that is not used by any tracks in the collection.')
    print('')


def printLicense() -> None:
    printVersion()
    print('')
    print('GPL License Version 3')
    print('')
    print('Copyright (c) 2024-present Didier Malenfant <didier@malenfant.net>')
    print('')
    print('TraktorBuddy is free software: you can redistribute it and/or modify it under the terms of the GNU General')
    print('Public License as published by the Free Software Foundation, either version 3 of the License, or')
    print('(at your option) any later version.')
    print('')
    print('TraktorBuddy is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the')
    print('implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public')
    print('License for more details.')
    print('')
    print('You should have received a copy of the GNU General Public License along with Main. If not,')
    print('see <https://www.gnu.org/licenses/>.')
    print('')


def main() -> None:
    global _test_mode
    global _verbose_mode

    _debug_on: bool = False

    try:
        # -- Gather the arguments, remove the first argument (which is the script filename)
        opts, _commands = getopt.getopt(sys.argv[1:], 'htdv', ['help', 'test', 'debug', 'verbose'])

        for o, a in opts:
            if o in ('-t', '--test'):
                print('Running in test mode.')
                _test_mode = True
            elif o in ('-d', '--debug'):
                print('Enabling debugging information.')
                _debug_on = True
            elif o in ('-v', '--verbose'):
                print('Enabling verbose mode.')
                _verbose_mode = True

        if len(_commands) == 0:
            raise ArgumentError('Expected a command! Maybe start with `tktbud help`?')

        switch = {
            'help': printUsage,
            'version': printVersion,
            'tag': tag,
            'purge': purgeBackups,
            'fix': fix,
            'listen': listen
        }

        if _commands is None:
            raise ArgumentError('Expected a command! Maybe start with `tktbud help`?')

        command = _commands[0]
        method = switch.get(command)
        if method is None:
            raise ArgumentError('Unknown commanwd \'' + command + '\'.')

        if _test_mode is not True and command != 'help' and command != 'version' and command != 'listen' and Utility.processIsRunning('Traktor'):
            raise RuntimeError('Traktor seems to be running. It\'s not a good idea to make changes to the collection at this time.')

        method(_commands)

    except getopt.GetoptError:
        printUsage([])
    except Exception as e:
        if _debug_on:
            print(traceback.format_exc())
        else:
            print(e)

        sys.exit(1)
    except KeyboardInterrupt:
        print('Execution interrupted by user.')
        pass


if __name__ == '__main__':
    main()
