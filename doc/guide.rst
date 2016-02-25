.. vim: set fileencoding=utf-8 :
.. @author: Manuel Gunther <siebenkopf@googlemail.com>
.. @date:   Fri Jan 22 09:08:25 MST 2016

.. py:currentmodule:: bob.db.celeba

==============
 User's Guide
==============

The CelebA database is a database of face images, which are labeled with several binary :py:meth:`Database.attributes`, such as "Big Nose", "Bushy Eyebrows", "Narrow Eyes" or "Smiling".
Additionally, five facial landmarks (:py:meth:`Database.annotations`) are labeled for each image, namely, the two eyes, the nose and the left and right mouth corners.

The database is split up into three partitions, a training set, a validation set and a test set.

After launching the python interpreter (assuming that the environment is properly set up), you could get the training set as follows:

.. doctest::

   >>> import bob.db.celeba
   >>> db = bob.db.celeba.Database()
   >>> files = db.objects(purposes='training')
   >>> file_names = [db.original_file_name(f) for f in files]

.. note::
   You can also use the :py:meth:`Database.training_set` to obtain the list of training :py:class:`File` objects.
   Similarly, the validation and test set can be obtained with :py:meth:`Database.validation_set` and :py:meth:`Database.test_set`.

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

The :py:meth:`Database.objects` function can also be used to filter the results for some attributes.
For example, if you only want the attractive young women, you might want to call:

.. doctest::

   >>> attractive_young_women = db.objects(with_attributes=["Attractive", "Young"], without_attributes="Male")
