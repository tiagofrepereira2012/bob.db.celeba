#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <laurent.el-shafey@idiap.ch>
#
# Copyright (C) 2011-2013 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""A few checks at the CelebA database.
"""

import bob.db.celeba
import random
import os

def test_query():
  db = bob.db.celeba.Database()

  train = db.objects("training")
  assert len(train) == 162770

  valid = db.objects("validation")
  assert len(valid) == 19867

  test = db.objects("test")
  assert len(test) == 19962

  all = db.objects()
  assert len(all) == 202599


def test_annotations():
  db = bob.db.celeba.Database()

  o = random.sample(db.objects(), 100)
  for f in o:
    a = db.annotations(f)
    assert set(a.keys()) == set(['leye', 'reye', 'nose', 'lmouth', 'rmouth'])


def test_attributes():
  db = bob.db.celeba.Database()

  o = random.sample(db.objects(), 1000)
  for f in o:
    a = db.attributes(f)
    assert len(a) == len(db.attribute_names())
    assert all(v == 1 or v == -1 for v in a)

    n = random.sample(bob.db.celeba.models.Attributes.attribute_names, 5)
    a2 = db.attributes(f, n)
    assert len(a2) == 5
    assert all(v == 1 or v == -1 for v in a2)


def test_attribute_values():
  db = bob.db.celeba.Database()
  f = db.objects()[0]
  assert f.id == 1
  first_attributes = [-1, 1, 1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, -1, 1, 1, -1, 1, -1, -1, 1, -1, -1, 1, -1, -1, -1, 1, 1, -1, 1, -1, 1, -1, -1, 1]
  assert f.attributes() == first_attributes, f.attributes()


def test_file_names():
  db = bob.db.celeba.Database("/path/to/files")

  o = random.sample(db.objects(), 10000)
  for f in o:
    n = db.original_file_name(f)
    assert n == os.path.join("/path/to/files", "%06d.jpg" % f.id)
