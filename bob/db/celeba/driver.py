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

"""Commands the CelebA database can respond to.
"""

import os
import sys
from bob.db.base.driver import Interface as BaseInterface


def dumplist(args):
  """Dumps lists of files based on your criteria"""

  from .query import Database
  db = Database()

  r = db.objects(
      groups=args.group,
      protocol=args.protocol,
      purposes=args.purpose,
      model_ids=args.template_id
  )

  output = sys.stdout
  if args.selftest:
    from bob.db.base.utils import null
    output = null()

  for f in r:
    output.write('%s\n' % (f.make_path(args.directory, args.extension, args.add_sighting_id),))

  return 0


def checkfiles(args):
  """Checks existence of files based on your criteria"""

  from .query import Database
  db = Database()

  r = db.objects()

  # go through all files, check if they are available on the filesystem
  good = {}
  bad = {}
  for f in r:
    if os.path.exists(f.make_path(args.directory,args.extension,args.add_sighting_id)): good[f.id] = f
    else: bad[f.id] = f

  # report
  output = sys.stdout
  if args.selftest:
    from bob.db.base.utils import null
    output = null()

  if bad:
    for id, f in bad.items():
      output.write('Cannot find file "%s"\n' % f.make_path(args.directory,args.extension,args.add_sighting_id))
    output.write('%d files (out of %d) were not found at "%s"\n' % \
        (len(bad), len(r), args.directory))

  return 0


def reverse(args):
  """Returns a list of file database identifiers given the path stems"""

  from .query import Database
  db = Database()

  output = sys.stdout
  if args.selftest:
    from bob.db.base.utils import null
    output = null()

  r = db.reverse(args.path)
  for f in r: output.write('%s\n' % f.id)

  if not r: return 1

  return 0


def path(args):
  """Returns a list of fully formed paths or stems given some file id"""

  from .query import Database
  db = Database()

  output = sys.stdout
  if args.selftest:
    from bob.db.base.utils import null
    output = null()

  r = db.paths(args.id, prefix=args.directory, suffix=args.extension)
  for path in r: output.write('%s\n' % path)

  if not r: return 1

  return 0


class Interface(BaseInterface):

  def name(self):
    return 'celeba'

  def version(self):
    import pkg_resources  # part of setuptools
    return pkg_resources.require('bob.db.%s' % self.name())[0].version

  def files(self):
    from .models import protocol_file
    return [protocol_file]

  def type(self):
    return 'text'

  def add_commands(self, parser):

    import argparse
    from . import __doc__ as docs
    subparsers = self.setup_parser(parser, "CelebA database", docs)


    # example: get the "create" action from a submodule
    from .create import add_command as create_command
    create_command(subparsers)

    from .query import Database
    db = Database()

    #from .models import ProtocolPurpose

    # the "dumplist" action
    parser = subparsers.add_parser('dumplist', help=dumplist.__doc__)
    parser.add_argument('-d', '--directory', help="if given, this path will be prepended to every entry returned.")
    parser.add_argument('-e', '--extension', help="if given, this extension will be appended to every entry returned.")

    parser.add_argument('--self-test', dest="selftest", action='store_true', help=argparse.SUPPRESS)
    parser.set_defaults(func=dumplist) #action

    # the "checkfiles" action
    parser = subparsers.add_parser('checkfiles', help=checkfiles.__doc__)
    parser.add_argument('-d', '--directory', help="if given, this path will be prepended to every entry returned.")
    parser.add_argument('-e', '--extension', help="if given, this extension will be appended to every entry returned.")
    parser.add_argument('--self-test', dest="selftest", action='store_true', help=argparse.SUPPRESS)
    parser.set_defaults(func=checkfiles) #action

    # adds the "reverse" command
    parser = subparsers.add_parser('reverse', help=reverse.__doc__)
    parser.add_argument('path', nargs='+', help="one or more path stems to look up. If you provide more than one, files which cannot be reversed will be omitted from the output.")
    parser.add_argument('--self-test', dest="selftest", action='store_true', help=argparse.SUPPRESS)
    parser.set_defaults(func=reverse) #action

    # adds the "path" command
    parser = subparsers.add_parser('path', help=path.__doc__)
    parser.add_argument('-d', '--directory', help="if given, this path will be prepended to every entry returned.")
    parser.add_argument('-e', '--extension', help="if given, this extension will be appended to every entry returned.")
    parser.add_argument('id', type=int, nargs='+', help="one or more file ids to look up. If you provide more than one, files which cannot be found will be omitted from the output. If you provide a single id to lookup, an error message will be printed if the id does not exist in the database. The exit status will be non-zero in such case.")
    parser.add_argument('--self-test', dest="selftest", action='store_true', help=argparse.SUPPRESS)
    parser.set_defaults(func=path) #action
