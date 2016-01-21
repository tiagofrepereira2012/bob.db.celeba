#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Manuel Gunther <mgunther@vast.uccs.edu>
# @date:   Fri Sep 11 14:53:52 MDT 2015
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

"""This script creates the CelebA database in a single pass.
"""

from __future__ import print_function

import os

import bob.core
logger = bob.core.log.setup("bob.db.celeba")

from .models import *

def _update(session, field):
  """Add, updates and returns the given field for in the current session"""
  session.add(field)
  session.flush()
  session.refresh(field)
  return field


def _file_id(name):
  return int(os.path.splitext(name)[0])

def add_annotations(session, directory):
  """Reads the "list_landmarks_celeba.txt" file and adds all annotations of the CelebA database"""

  list_file = os.path.join(directory, 'list_landmarks_celeba.txt')
  logger.info("Reading annotations from %s", list_file)
  with open(list_file) as f:
    # ignore the first two lines
    _ = f.readline()
    _ = f.readline()
    # read the rest of the lines
    for counter, line in enumerate(f,1):
      splits = line.rstrip().split()
      assert len(splits) == 11, splits

      # create annotation
      annotation = Annotation(_file_id(splits[0]), [int(s) for s in splits[1:]])
      session.add(annotation)

#      if counter == 1000: break

    logger.info("Created %d Annotation objects", counter)

def add_attributes(session, directory):
  """Reads the "list_attr_celeba.txt" file and adds all attributes of the CelebA database"""

  list_file = os.path.join(directory, 'list_attr_celeba.txt')
  logger.info("Reading attributes from %s", list_file)
  with open(list_file) as f:
    # ignore the first two lines
    _ = f.readline()
    _ = f.readline()
    # read the rest of the lines
    for counter, line in enumerate(f,1):
      splits = line.rstrip().split()
      assert len(splits) == 41, splits

      # create attributes
      attributes = Attributes(_file_id(splits[0]), [int(s) for s in splits[1:]])
      session.add(attributes)
      logger.debug("Added attribute %s", attributes)

#      if counter == 1000: break

    logger.info("Created %d Attribute objects", counter)


def add_files_and_purposes(session, directory):
  """Reads the "list_eval_partition.txt" file and assigns each file a purpose"""

  # first, create the three purposes
  _purposes = {str(i) : p for i,p in enumerate(Purpose.purpose_names)}
  # and add them to the session
  for p in _purposes.values(): _update(session, Purpose(p))

  list_file = os.path.join(directory, 'list_eval_partition.txt')
  logger.info("Reading files and their purposes from %s", list_file)
  with open(list_file) as f:
    # ignore the first two lines
#    _ = f.readline()
#    _ = f.readline()
    # read the rest of the lines
    for counter, line in enumerate(f,1):
      splits = line.rstrip().split()
      assert len(splits) == 2, splits

      # add file
      # create file
      file = File(_file_id(splits[0]), _purposes[splits[1]])
      session.add(file)
      logger.debug("Added file %s", file)

#      if counter == 1000: break

    logger.info("Created %d File objects", counter)


def create_tables(args):
  """Creates all necessary tables (only to be used at the first time)"""

  from bob.db.base.utils import create_engine_try_nolock

  engine = create_engine_try_nolock(args.type, args.files[0], echo=(args.verbose > 2))
  Annotation.metadata.create_all(engine)
  Attributes.metadata.create_all(engine)
  File.metadata.create_all(engine)
  Purpose.metadata.create_all(engine)


# Driver API
# ==========

def create(args):
  """Creates or re-creates this database"""

  bob.core.log.set_verbosity_level(logger, args.verbose)

  from bob.db.base.utils import session_try_nolock

  dbfile = args.files[0]

  if args.recreate:
    if os.path.exists(dbfile):
      logger.info('unlinking %s...', dbfile)
      os.unlink(dbfile)

  if not os.path.exists(os.path.dirname(dbfile)):
    os.makedirs(os.path.dirname(dbfile))

  # the real work...
  create_tables(args)
  session = session_try_nolock(args.type, args.files[0], echo=(args.verbose > 2))

  add_files_and_purposes(session, args.directory)
  add_annotations(session, args.directory)
  add_attributes(session, args.directory)

  session.commit()
  session.close()


def add_command(subparsers):
  """Add specific subcommands that the action "create" can use"""

  parser = subparsers.add_parser('create', help=create.__doc__)

  parser.add_argument('-R', '--recreate', action='store_true', help='If set, I\'ll first erase the current database')
  parser.add_argument('-D', '--directory', metavar='DIR', default='/mgunther/databases/CelebA/', help='The path to the CelebA database')

  bob.core.log.add_command_line_option(parser)

  parser.set_defaults(func=create) #action
