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

import random
import string
import os


def random_str_func(k):
    def random_str():
        return "".join(random.choices(string.ascii_letters + string.digits, k=k))

    return random_str


def random_str_32():
    return random_str_func(32)()


def without_folder(path):
    return os.path.splitext(os.path.basename(path))[0]


def get_directory(path):
    return os.path.dirname(path)


def join(path1, path2):
    return os.path.join(path1, path2)


def generate_filename(ext="wav", bit=16, title=None):
    if title:
        return f"Matchering_{bit}bit_{title}_{random_str_func(4)()}.{ext}"
    else:
        return f"{random_str_func(16)()}.{ext}"
