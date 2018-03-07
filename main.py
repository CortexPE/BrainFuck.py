"""
   ____           _            ____  _____
  / ___|___  _ __| |_ _____  _|  _ \| ____|
 | |   / _ \| '__| __/ _ \ \/ / |_) |  _|
 | |__| (_) | |  | ||  __/>  <|  __/| |___
  \____\___/|_|   \__\___/_/\_\_|   |_____|

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import sys

MEMORY = [0] * 2048
WORKINGINDEX = 1024  # so we support negative indexes
CURRENT_LOOP_INDEX = 0
FILE_INDEX = 0


# PYTHON GETCH METHOD FROM:
# http://code.activestate.com/recipes/134892-getch-like-unbuffered-character-reading-from-stdin/
class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty

    def __call__(self):
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()

file = input("File to load: ")
file = open(str(file), 'r').read()
EOF = len(file)

while True:
    char = file[FILE_INDEX]
    if char == ">":
        WORKINGINDEX += 1
    elif char == "<":
        WORKINGINDEX -= 1
    elif char == "+":
        MEMORY[WORKINGINDEX] += 1
    elif char == "-":
        MEMORY[WORKINGINDEX] -= 1
    elif char == ".":
        sys.stdout.write(chr(MEMORY[WORKINGINDEX]))
        sys.stdout.flush()
    elif char == ",":
        MEMORY[WORKINGINDEX] = ord(getch())
    elif char == "[":
        CURRENT_LOOP_INDEX = FILE_INDEX
    elif char == "]":
        if MEMORY[WORKINGINDEX] != 0:
            INDEX = CURRENT_LOOP_INDEX
    FILE_INDEX += 1
    if FILE_INDEX == EOF:
        break
