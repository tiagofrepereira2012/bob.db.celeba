#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Laurent El Shafey <Laurent.El-Shafey@idiap.ch>
# @date: Wed May 8 19:42:39 CEST 2013
#
# Copyright (C) 2011-2013 Idiap Research Institute, Martigny, Switzerland
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

import shutil
import os

from .models import *
from .driver import Interface

class Database():
  """Wrapper class for the MNIST database of handwritten digits (http://yann.lecun.com/exdb/mnist/).
  """

  def __init__(self, original_directory = None, original_extension = '.jpg'):
    """Creates the database"""
    # initialize members
    self.m_sqlite_file = Interface().files()[0]
    if not os.path.exists(self.m_sqlite_file):
      self.m_session = None
    else:
      import bob.db.base.utils
      self.m_session = bob.db.base.utils.session_try_readonly('sqlite', self.m_sqlite_file)
    self.original_directory = original_directory
    self.original_extension = original_extension

  def __del__(self):
    """Closes the connection to the database when it is not needed any more."""
    if self.is_valid():
      # do some magic to close the connection to the database file
      try:
        # Since the dispose function re-creates a pool
        #   which might fail in some conditions, e.g., when this destructor is called during the exit of the python interpreter
        self.m_session.close()
        self.m_session.bind.dispose()
      except TypeError:
        # ... I can just ignore the according exception...
        pass
      except AttributeError:
        pass


  def is_valid(self):
    """Returns if a valid session has been opened for reading the database."""
    return self.m_session is not None


  def assert_validity(self):
    """Raise a RuntimeError if the database back-end is not available."""
    if not self.is_valid():
      raise IOError("Database of type 'sqlite' cannot be found at expected location '%s'." % self.m_sqlite_file)


  def query(self, *args):
    """Creates a query to the database using the given arguments."""
    self.assert_validity()
    return self.m_session.query(*args)


  def _check_parameters_for_validity(self, parameters, parameter_description, valid_parameters, default_parameters = None):
    """Checks the given parameters for validity, i.e., if they are contained in the set of valid parameters.
    It also assures that the parameters form a tuple or a list.
    If parameters is 'None' or empty, the default_parameters will be returned (if default_parameters is omitted, all valid_parameters are returned).

    This function will return a tuple or list of parameters, or raise a ValueError.

    Keyword parameters:

    parameters
      The parameters to be checked.
      Might be a string, a list/tuple of strings, or None.

    parameter_description
      A short description of the parameter.
      This will be used to raise an exception in case the parameter is not valid.

    valid_parameters
      A list/tuple of valid values for the parameters.

    default_parameters
      The list/tuple of default parameters that will be returned in case parameters is None or empty.
      If omitted, all valid_parameters are used.
    """
    if parameters is None:
      # parameters are not specified, i.e., 'None' or empty lists
      parameters = default_parameters if default_parameters is not None else valid_parameters

    if not isinstance(parameters, (list, tuple, set)):
      # parameter is just a single element, not a tuple or list -> transform it into a tuple
      parameters = (parameters,)

    # perform the checks
    for parameter in parameters:
      if parameter not in valid_parameters:
        raise ValueError("Invalid %s '%s'. Valid values are %s, or lists/tuples of those" % (parameter_description, parameter, valid_parameters))

    # check passed, now return the list/tuple of parameters
    return parameters


  def attribute_names(self):
    """Returns the vector of labels
    """
    return Attributes.attribute_names


  def objects(self, purposes = None):
    """objects(self, purposes=None) -> files

    Returns a list of :py:class:`File` objects for the given purposes.

    **Parameters:**

    ``purposes`` : str or [str] or ``None``

      A purpose or a list of purposes, which might be ``("training", "validation", "test")``.
      If ``None``, the full list of purposes will be used.

    **Returns:**

    ``files`` : [:py:class:`File`]
      A list of files for the given purpose(s).
    """
    purposes_ = self._check_parameters_for_validity(purposes, "purpose", Purpose.purpose_names)

    q = self.query(File).order_by(File.id)
    if purposes is not None:
      q = q.join(Purpose).filter(Purpose.name.in_(purposes_))
    return list(q)


  def original_file_name(self, file):
    """original_file_name(self, file) -> image_name

    Returns the full path of the original image name.
    This function requires that the ``original_directory`` was specified in the constructor of this class.

    **Parameters:**

    ``file`` : : :py:class:`File`
      The file object to get the original file name for.

    **Returns:**

    image_name : str
      The full path to the image belonging to the given :py:class:`File` object.
    """
    return file.make_path(self.original_directory, self.original_extension)


  def annotations(self, file):
    """annotations(self, file) -> annotations

    Returns the annotations for the given file.

    .. note::
       The annotations are returned in the default way comparable with other bob databases, i.e., in (y,x) order.
       Please also note that the name of the annotations have been changed to be in subject perspective (e.g., the x-coordinate of the left eye is larger than the x coordintae of the right eye),
       while the original database contains eye locations in observer perspective.

    **Parameters:**

    ``file`` : :py:class:`File`
      The file object to get the annotations for.

    **Returns:**

    ``annotations`` : {}
      The dictionary of annotations, which include the coordinated for 'reye', 'leye', 'nose', 'rmouth', 'lmouth'.
    """
    return file.annotation()


  def attributes(self, file, attribute_names=None):
    """attributes(self, file, attribute_names=None) -> attributes

    Returns the list of attributes for the given file.
    If ``attribute_names`` are specified, only the attributes for the given ``attribute_names`` are returned -- in exactly the same order.

    **Parameters:**

    ``file`` : :py:class:`File`
      The file object to get the attributes for.

    ``attribute_names`` : str or [str] or ``None``
      The list of attribute names (see :py:attr:`Attribute.attribute_names` for a list of valid names) which should be retrieved.
      If ``None``, all attributes are returned.

    **Returns:**

    ``attributes`` : [int]
      The list of attributes, which are either +1 (in case the attribute is present) or -1 (in case the attribute is absent).
    """
    attribute_names = self._check_parameters_for_validity(attribute_names, "attribute name", Attributes.attribute_names)

    return file.attributes(attribute_names)
