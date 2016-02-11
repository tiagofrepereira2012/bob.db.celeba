#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Manuel Gunther <siebenkopf@googlemail.com>
# @date:   Fri Jan 22 09:08:25 MST 2016
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Table models and functionality for the CelebA database.
"""
import os

import pkg_resources
import tarfile

class Annotation:
  """Annotations of the CelebA database consists of the locations of the two eyes, the nose tip and the mouth corners.
  There is exactly one annotation for each :py:class:`File`, which after creation of the database can be obtained using ``self.file``.

  .. note::
     The eye and mouth locations given in the original annotation file are in observer perspective (i.e., the right eye is to the right of the left eye).
     To be consistent with other databases of Bob, here we change them to be in subject perspective (i.e., the right eye is to the left of the left eye).
     Also, as usual for Bob, coordinates are specified in ``(y,x)`` order, opposite to how they are written in the list file.
  """
  def __init__(self, file_id, labels):
    self.file_id = file_id

    assert len(labels) == 10
    self.re_x = labels[2] # left eye in the list file
    self.re_y = labels[3]
    self.le_x = labels[0] # right eye in the list file
    self.le_y = labels[1]
    self.n_x = labels[4]
    self.n_y = labels[5]
    self.rm_x = labels[8] # left mouth in the list file
    self.rm_y = labels[9]
    self.lm_x = labels[6] # right mouth in the list file
    self.lm_y = labels[7]

  def __call__(self):
    """Returns these annotations in a dictionary, which are: ``{'reye' : (re_y, re_x), 'leye' : (le_y, le_x), 'nose' : (n_y, n_x), 'rmouht' : (rm_y, rm_x), 'lmouth' : (lm_y, lm_x)}``.
    """
    return {
      'reye' : (self.re_y, self.re_x),
      'leye' : (self.le_y, self.le_x),
      'nose' : (self.n_y, self.n_x),
      'rmouth' : (self.rm_y, self.rm_x),
      'lmouth' : (self.lm_y, self.lm_x),
    }

  def __repr__(self):
    return "<Annotation('%d')>" % self.file_id


class Attributes:
  """Attributes of the CelebA database consist of a list of binary labels for the face, such as ``Smiling``, ``Wavy_Hair``, ``Young`` or ``Pointy_Nose``.
  Each attribute is binary, i.e., it either exists (``+1``) or it does not exist (``-1``).
  There is exactly one set of attributes for each :py:class:`File`, which after creation of the database can be obtained using ``self.file``.
  """

  attribute_names = (
    '5_o_Clock_Shadow',
    'Arched_Eyebrows',
    'Attractive',
    'Bags_Under_Eyes',
    'Bald',
    'Bangs',
    'Big_Lips',
    'Big_Nose',
    'Black_Hair',
    'Blond_Hair',
    'Blurry',
    'Brown_Hair',
    'Bushy_Eyebrows',
    'Chubby',
    'Double_Chin',
    'Eyeglasses',
    'Goatee',
    'Gray_Hair',
    'Heavy_Makeup',
    'High_Cheekbones',
    'Male',
    'Mouth_Slightly_Open',
    'Mustache',
    'Narrow_Eyes',
    'No_Beard',
    'Oval_Face',
    'Pale_Skin',
    'Pointy_Nose',
    'Receding_Hairline',
    'Rosy_Cheeks',
    'Sideburns',
    'Smiling',
    'Straight_Hair',
    'Wavy_Hair',
    'Wearing_Earrings',
    'Wearing_Hat',
    'Wearing_Lipstick',
    'Wearing_Necklace',
    'Wearing_Necktie',
    'Young'
  )

  attribute_indices = {a:i for i,a in enumerate(attribute_names)}

  def __init__(self, file_id, attributes):
    self.file_id = file_id

    assert len(attributes) == 40
    self.attributes = attributes

  def __call__(self, attribute_names = None):
    """Returns these attributes in a dictionary, with the attribute name as key and the binary value ``+1`` or ``-1`` for the presence or absence of the attribute.
    """
    if attribute_names is None:
      return self.attributes
    return [self.attributes[self.attribute_indices[a]] for a in attribute_names]

  def __repr__(self):
    return "<Attributes('%d')>" % self.file_id


class File:
  """Information about the files of the CelebA database.

  Each file includes only a numerical ID (which is identical to the file path).

  Additionally, some fields will be available, once the database is created:

  * ``annotation``: the :py:class:`Annotation`, which belongs to this file
  * ``attributes``: the :py:class:`Attributes`, which belongs to this file
  * ``purpose``: the :py:class:`Purpose`, for which this file is used

  """
  def __init__(self, file_id, purpose):
    self.id = file_id
    self.purpose_name = purpose

  def make_path(self, directory = None, extension = None):
    """Wraps the current path so that a complete path is formed.
    To get the original file name, please use the :py:meth:`Database.original_file_name` function instead, or set the ``add_sighting_id`` flag to ``False``.

    Keyword parameters:

    ``directory`` : str or ``None``
      An optional directory name that will be prefixed to the returned result.

    ``extension`` : str or ``None``
      An optional extension that will be suffixed to the returned filename.
      The extension normally includes the leading ``.`` character as in ``.jpg`` or ``.hdf5``.

    Returns a string containing the newly generated file path, which by default is unique.
    """

    # assure that directory and extension are actually strings
    if not directory: directory = ''
    if not extension: extension = ''
    # create the path
    return str(os.path.join(directory, "%06d%s" % (self.id, extension)))


# dictionary storing the loaded protocol information
protocol_file = pkg_resources.resource_filename("bob.db.celeba", "data/protocol.tar.bz2")
files_list = []
annotations_dict = {}
attributes_dict = {}
purpose_names = ("training", "validation", "test")

def _file_id(name):
  return int(os.path.splitext(name)[0])

def get_files():
  """Reads the 'list_eval_partition.txt' from the protocol file"""
  if not files_list:
    tar = tarfile.open(protocol_file, 'r')
    f = tar.extractfile('list_eval_partition.txt')
    # read the lines
    for line in f:
      splits = line.rstrip().split()
      assert len(splits) == 2, splits

      # create file
      file = File(_file_id(splits[0]), purpose_names[int(splits[1])])
      files_list.append(file)
  return files_list

def get_annotations():
  """Reads the 'list_landmarks_celeba.txt' from the protocol file"""
  if not annotations_dict:
    tar = tarfile.open(protocol_file, 'r')
    f = tar.extractfile('list_landmarks_celeba.txt')
    # ignore the first two lines
    _ = f.readline()
    _ = f.readline()
    # read the rest of the lines
    for line in f:
      splits = line.rstrip().split()
      assert len(splits) == 11, splits

      # create annotation
      annotation = Annotation(_file_id(splits[0]), [int(s) for s in splits[1:]])
      annotations_dict[annotation.file_id] = annotation
  return annotations_dict

def get_attributes():
  """Reads the 'list_attr_celeba.txt' from the protocol file"""
  if not attributes_dict:
    tar = tarfile.open(protocol_file, 'r')
    f = tar.extractfile('list_attr_celeba.txt')
    # ignore the first two lines
    _ = f.readline()
    _ = f.readline()
    # read the rest of the lines
    for line in f:
      splits = line.rstrip().split()
      assert len(splits) == 41, splits

      # create attributes
      attributes = Attributes(_file_id(splits[0]), [int(s) for s in splits[1:]])
      attributes_dict[attributes.file_id] = attributes
  return attributes_dict
