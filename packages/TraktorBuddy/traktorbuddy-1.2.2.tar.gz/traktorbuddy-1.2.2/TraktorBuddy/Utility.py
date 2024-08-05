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

import pytz
import subprocess
import os
import xml.etree.ElementTree as ET

from datetime import datetime
from typing import List


# -- Class
class Utility:
    """Helper methods."""

    # -- This is used in Unit tests to mock the time for 'now'.
    _mock_now_date = None

    @classmethod
    def stringToInt(cls, string: str) -> int:
        if string is None:
            return None

        return int(string)

    @classmethod
    def stringToFloat(cls, string: str) -> float:
        if string is None:
            return None

        return float(string)

    @classmethod
    def dateFromString(cls, string: str, format: str, utc: bool = False) -> datetime:
        if string is None:
            return None

        try:
            date = datetime.strptime(string, format)
            if utc:
                date = pytz.utc.localize(date)

            return date
        except ValueError:
            return None

    @classmethod
    def utcTimeNow(cls) -> datetime:
        if Utility._mock_now_date is not None:
            return Utility._mock_now_date

        return datetime.now().astimezone(pytz.utc)

    @classmethod
    def utcDatetime(cls, year: int, month: int, day: int, hour: int, minutes: int, seconds: int) -> datetime:
        return pytz.utc.localize(datetime(year, month, day, hour, minutes, seconds))

    @classmethod
    def xmlElementToString(cls, element: ET.Element, xml_declaration: bool = False) -> str:
        return ET.tostring(element, encoding='unicode', short_empty_elements=False, xml_declaration=xml_declaration)

    @classmethod
    def processIsRunning(cls, process_name: str) -> bool:
        return process_name in Utility.shellCommand(['ps', '-axc', '-o', 'comm'])

    @classmethod
    def shellCommand(cls, command_and_args: List[str], from_dir: str = None) -> str:
        try:
            if from_dir is None:
                from_dir = os.path.expanduser('~')

            process = subprocess.Popen(command_and_args, cwd=from_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                print(command_and_args)
                print(stdout)
                print(stderr)

                raise RuntimeError('Error running shell command.')

            return stdout.decode('UTF-8').split('\n')
        except RuntimeError:
            raise
        except SyntaxError:
            raise
        except Exception as e:
            raise RuntimeError('Error running shell command: ' + str(e))
