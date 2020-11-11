"""
Matchering WEB - Handy Matchering 2.0 Containerized Web Application
Copyright (C) 2016-2021 Sergree

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from django.utils.text import get_valid_filename
from django_rq import job
import matchering as mg

from matchering_web.settings import MEDIA_ROOT
from mgw_back.models import MGSession
from mgw_back.utilities import get_directory, join, generate_filename


def media(path):
    return join(MEDIA_ROOT, path)


class Paths:
    def __init__(self, target_path, target_title):
        self.title = get_valid_filename(target_title)
        self.folder = get_directory(target_path)
        self.result16 = join(self.folder, generate_filename("wav", 16, self.title))
        self.result24 = join(self.folder, generate_filename("wav", 24, self.title))
        self.preview_target = join(self.folder, generate_filename("flac"))
        self.preview_result = join(self.folder, generate_filename("flac"))


class SessionUpdater:
    def __init__(self, session: MGSession, paths: Paths):
        self.session = session
        self.paths = paths

    def __code(self, value):
        if len(value) >= 4:
            try:
                code = int(value[:4])
                if 2000 < code < 5000:
                    return code
            except ValueError:
                pass
        return 4201

    def info(self, value):
        code = self.__code(value)
        self.session.code = code
        if code == 2010:
            self.session.result16 = self.paths.result16
            self.session.result24 = self.paths.result24
            self.session.preview_target = self.paths.preview_target
            self.session.preview_result = self.paths.preview_result
        self.session.save()

    def warning(self, value):
        code = self.__code(value)
        self.session.warnings.create(code=code)


@job
def process(session: MGSession):
    if session.code != 2002:
        return

    paths = Paths(session.target.file.name, session.target.title)
    updater = SessionUpdater(session, paths)

    mg.log(info_handler=updater.info, warning_handler=updater.warning, show_codes=True)

    try:
        mg.process(
            target=media(session.target.file.name),
            reference=media(session.reference.file.name),
            results=[
                mg.pcm16(media(paths.result16)),
                mg.pcm24(media(paths.result24)),
            ],
            preview_target=mg.pcm16(media(paths.preview_target)),
            preview_result=mg.pcm16(media(paths.preview_result)),
        )
    except Exception as e:
        updater.info(str(e))
