.. vim: set fileencoding=utf-8 :
.. Manuel Gunther <siebenkopf@googlemail.com>
.. Fri Jan 22 09:08:25 MST 2016

.. image:: http://img.shields.io/badge/docs-stable-yellow.png
   :target: http://pythonhosted.org/bob.db.celeba/index.html
.. image:: http://img.shields.io/badge/docs-latest-orange.png
   :target: https://www.idiap.ch/software/bob/docs/latest/bioidiap/bob.db.celeba/master/index.html
.. image:: https://travis-ci.org/bioidiap/bob.db.celeba.svg?branch=master
   :target: https://travis-ci.org/bioidiap/bob.db.celeba
.. image:: https://coveralls.io/repos/bioidiap/bob.db.celeba/badge.png
   :target: https://coveralls.io/r/bioidiap/bob.db.celeba
.. image:: https://img.shields.io/badge/github-master-0000c0.png
   :target: https://github.com/bioidiap/bob.db.celeba/tree/master
.. image:: http://img.shields.io/pypi/v/bob.db.celeba.png
   :target: https://pypi.python.org/pypi/bob.db.celeba
.. image:: http://img.shields.io/pypi/dm/bob.db.celeba.png
   :target: https://pypi.python.org/pypi/bob.db.celeba
.. image:: https://img.shields.io/badge/original-data--files-a000a0.png
   :target: http://personal.ie.cuhk.edu.hk/~lz013/projects/CelebA.html

===================================
 CelebA Database Interface for Bob
===================================

The `CelebA database`_ consists of a collection of 202'599 facial images of celebrities that are labeled with binary attributes describing the face, such as wavy hair, oval face, mustache or smiling.
It is split into a training, a development (validation) and an evaluation (test) set, which can be used for the classification of the attributes.
Note that no information about the identity shown in the images is labeled, so this database cannot be used for face recognition purposes.

This package only contains the Bob_ accessor methods to use this database directly from Python.
It does not contain the original raw data files, which need to be obtained through the link above.

Installation
------------
To install this package -- alone or together with other `Packages of Bob <https://github.com/idiap/bob/wiki/Packages>`_ -- please read the `Installation Instructions <https://github.com/idiap/bob/wiki/Installation>`_.
For Bob_ to be able to work properly, some dependent packages are required to be installed.
Please make sure that you have read the `Dependencies <https://github.com/idiap/bob/wiki/Dependencies>`_ for your operating system.

Documentation
-------------
For further documentation on this package, please read the `Stable Version <http://pythonhosted.org/bob.db.celeba/index.html>`_ or the `Latest Version <https://www.idiap.ch/software/bob/docs/latest/bioidiap/bob.db.celeba/master/index.html>`_ of the documentation.
For a list of tutorials on this or the other packages ob Bob_, or information on submitting issues, asking questions and starting discussions, please visit its website.

.. _bob: https://www.idiap.ch/software/bob
.. _celeba database: http://personal.ie.cuhk.edu.hk/~lz013/projects/CelebA.html
