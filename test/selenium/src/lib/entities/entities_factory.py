# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Module for business entities."""
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments
# pylint: disable=no-self-use
import random

from lib.constants import objects
from lib.constants.element import AttributesTypes
from lib.entities import entity
from lib.utils.string_utils import random_list_of_strings, random_string
from lib.utils.test_utils import append_random_string


class CAFactory(object):
  """Factory class for Custom Attribute entity."""

  def create(self, title=None, ca_type=None, definition_type=None,
             helptext="", placeholder=None, multi_choice_options=None,
             is_mandatory=False, ca_global=True):
    """"
    Method for basic CustomAttribute object creation.
    None type or definition will be filled randomly.
    """
    ca_entity = self._create_random_ca()
    ca_entity = self._fill_ca_entity_fields(
        title, ca_type, definition_type, helptext,
        placeholder, multi_choice_options,
        is_mandatory, ca_global, ca_entity
    )
    ca_entity = self._normalize_ca_definition_type(ca_entity)
    return ca_entity

  def _create_random_ca(self):
    """Create random CustomAttribute entity."""
    random_ca = entity.CustomAttribute()
    random_ca.ca_type = random.choice(AttributesTypes.ALL_TYPES)
    random_ca.title = self._generate_title(random_ca.ca_type)
    random_ca.definition_type = random.choice(objects.all_objects)
    return random_ca

  def _generate_title(self, ca_type):
    """Generate title according to CustomAttribute type."""
    return append_random_string("{}_{}_".format(ca_type, random_string()))

  def _fill_ca_entity_fields(self, title,
                             ca_type, definition_type,
                             helptext, placeholder,
                             multi_choice_options, mandatory,
                             ca_global, ca_object):
    """Set the CustomAttributes object's attributes."""
    if ca_type:
      ca_object.ca_type = ca_type
      ca_object.title = self._generate_title(ca_type)
    if definition_type:
      ca_object.definition_type = definition_type
    if title:
      ca_object.title = title

    # "Placeholder" field exists only for Text and Rich Text.
    if placeholder and ca_object.ca_type in (AttributesTypes.TEXT,
                                             AttributesTypes.RICH_TEXT):
      ca_object.placeholder = placeholder

    ca_object.helptext = helptext
    ca_object.mandatory = mandatory
    ca_object.ca_global = ca_global

    # "Possible Values" - is a mandatory field for Dropdown CustomAttribute.
    if ca_object.ca_type == AttributesTypes.DROPDOWN:
      if ca_object.multi_choice_options is None:
        ca_object.multi_choice_options = random_list_of_strings(list_len=3)
      else:
        ca_object.multi_choice_options = multi_choice_options

    return ca_object

  def _normalize_ca_definition_type(self, ca_object):
    """
    Get ca_group title from the selected object for further using in UI.
    For manipulations with object via REST, definition type should be
    interpreted as objects.get_singular().get_object_name_form().
    """
    ca_object.definition_type = objects.get_normal_form(
        ca_object.definition_type
    )
    return ca_object
