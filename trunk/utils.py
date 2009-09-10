# Copyright 2009, Jeffrey Regier, jeff [at] stat [dot] berkeley [dot] edu

# This file is part of the Badger Author Disambiguation Toolkit (Badger).
#
# Badger is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Badger is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Badger.  If not, see <http://www.gnu.org/licenses/>.


import re
from collections import defaultdict


def compatible_name_part(w1, w2):
    w1 = re.sub(r'\W', '', w1)
    w2 = re.sub(r'\W', '', w2)
    l = min(len(w1), len(w2))
    if not l:
        return True
    return w1[:l] == w2[:l]


def compatible_names(e1, e2):
    """This function takes either PartitionParts or AuthorRefs as arguments
    """

    if e1.ln() != e2.ln():
        return False

    short, long = list(e1.mns()), e2.mns()
    if len(short) > len(long):
        return compatible_names(e2, e1)

    # the front first names must be compatible
    if not compatible_name_part(e1.fn(), e2.fn()):
        return False

    # try finding each middle name of long in short, and remove the
    # middle name from short if found
    for wl in long:
        if not short:
            break
        ws = short.pop(0)
        if not compatible_name_part(ws, wl):
            short.insert(0, ws)

    # true iff short is a compatible substring of long
    return short == []


def drop_fn_source_candidate(p):
    return len(p.mns()) == 1 and\
        len(p.mns()[0]) == 1 and\
        p.mns()[0][0] != p.fn()[0]

def drop_fn_target_candidate(p):
    return len(p.mns()) == 0


def drop_ln_source_candidate(p):
    return re.match(r'\w{4,}-\w{4,}', p.ln())


def shorter(s1, s2):
    return s1 if len(s1) < len(s2) else s2


def same_fl_initials(name1, name2):
    if name1[0] != name2[0]:
        return False
    li1 = re.sub(r'^.* (\S)\S*$', r'\1', name1)
    li2 = re.sub(r'^.* (\S)\S*$', r'\1', name2)
    return li1 == li2

