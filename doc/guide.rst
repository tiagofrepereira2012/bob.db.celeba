.. vim: set fileencoding=utf-8 :
.. @author: Manuel Guenther <Manuel.Guenther@idiap.ch>
.. @date:   Thu Dec  6 12:28:25 CET 2012

==============
 User's Guide
==============

The CelebA database is a database of face images, which are labeled with several binary ``attributes``, such as "Big Nose", "Bushy Eyebrows", "Narrow Eyes" or "Smiling".
Additionally, five facial landmarks (``annotations``) are labeled for each image, namely, the two eyes, the nose and the left and right mouth corners.

The database is split up into three partitions, a training set, a validation set and a test set.

After launching the python interpreter (assuming that the environment is properly set up), you could get the training set as follows:

.. doctest::

  >>> import bob.db.celeba
  >>> db = bob.db.celeba.Database()
  >>> files = db.objects(purposes='training')
  >>> file_names = [db.original_file_name(f) for f in files]

The annotations can be used to align the face in the image, e.g., using the :py:class:`bob.ip.base.FaceEyesNorm`:

.. code-block:: py

  >>> import bob.io.base
  >>> import bob.io.image
  >>> import bob.ip.base
  >>> face_eyes_norm = bob.ip.base.FaceEyesNorm(image_size=(100,100), right_eye=(33,33), left_eye=(33,67))
  >>> image = bob.io.base.load(file_names[0])
  >>> annotations = db.annotations(files[0])
  >>> aligned_image = face_eyes_norm(image, right_eye = annotations['reye'], left_eye = annotations['leye'])

Different kinds of features can be extracted from the images, and a classifier can be trained to classify the attributes.
The attributes themselves are binary (the actual datatype is ``int``), where ``+1`` stands for the presence of the attribute, while ``-1`` indicates the absence of it:

.. doctest::

  >>> attributes = db.attributes(files[0])
  >>> for i in range(4):
  ...   print ("Attribute '%s' is %spresent" % (db.attribute_names()[i], "" if attributes[i] == 1 else "not "))
  Attribute '5_o_Clock_Shadow' is not present
  Attribute 'Arched_Eyebrows' is present
  Attribute 'Attractive' is present
  Attribute 'Bags_Under_Eyes' is not present
