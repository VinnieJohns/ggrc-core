# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Utility functions for string operations"""

import random
import string


def random_string(size=5, chars=string.letters + string.digits):
  """Return string with corresponding size that filled by values from selected
  chars.
  """
  return ''.join(random.choice(chars) for position in range(size))


def random_list_of_strings(
    list_len=3, item_size=5, chars=string.letters + string.digits):
  """Return list of random strings separated by comma"""
  return ','.join(random_string(item_size, chars) for item in range(list_len))


def get_bool_from_string(str_to_bool):
  """Return True for 'Yes' and False for 'No'."""
  if str_to_bool.title() == 'Yes':
    return True
  elif str_to_bool.title() == 'No':
    return False
  else:
    raise ValueError("'{}' can't be converted to boolean".format(str_to_bool))
