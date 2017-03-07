# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Module for factories that create entities."""
# pylint: disable=too-many-arguments
# pylint: disable=invalid-name
# pylint: disable=redefined-builtin


import random

from lib.constants import element, objects, roles, url as const_url
from lib.constants.element import AdminWidgetCustomAttrs
from lib.entities import entity
from lib.utils import string_utils
from lib.utils.string_utils import (random_list_strings, random_string,
                                    random_uuid)


class EntitiesFactory(object):
  """Common factory class for entities."""
  # pylint: disable=too-few-public-methods
  _obj_person = objects.get_singular(objects.PEOPLE)
  _obj_program = objects.get_singular(objects.PROGRAMS)
  _obj_control = objects.get_singular(objects.CONTROLS)
  _obj_audit = objects.get_singular(objects.AUDITS)
  _obj_asmt_tmpl = objects.get_singular(objects.ASSESSMENT_TEMPLATES)
  _obj_asmt = objects.get_singular(objects.ASSESSMENTS)

  all_objs_attrs_names = tuple(entity.Entity().attrs_names_all_entities())

  @classmethod
  def update_obj_attrs_values(cls, obj, attrs_names=all_objs_attrs_names,
                              **arguments):
    """Update the object's (obj) attributes values according to the list of
    unique possible objects' names and dictionary of arguments (key = value).
    """
    # pylint: disable=expression-not-assigned
    [setattr(obj, attr_name, arguments[attr_name]) for
        attr_name in attrs_names if arguments.get(attr_name)]
    return obj

  @classmethod
  def _generate_title(cls, obj_type):
    """Generate title according object type and random data."""
    special_chars = string_utils.SPECIAL
    return "{obj_type}_{uuid}_{rand_str}".format(
        obj_type=obj_type, uuid=random_uuid(),
        rand_str=random_string(size=len(special_chars), chars=special_chars))

  @classmethod
  def _generate_code(cls):
    """Generate code according str part and random data."""
    return "{code}".format(code=random_uuid())

  @classmethod
  def _generate_email(cls, domain=const_url.DEFAULT_EMAIL_DOMAIN):
    """Generate email according domain."""
    return "{mail_name}@{domain}".format(
        mail_name=random_uuid(), domain=domain)


class PersonFactory(EntitiesFactory):
  """Factory class for Person entity."""

  @classmethod
  def default(cls):
    """Create default system Person object."""
    return cls.create(
        title=roles.DEFAULT_USER, id=1, href=const_url.DEFAULT_USER_HREF,
        email=const_url.DEFAULT_USER_EMAIL, authorizations=roles.SUPERUSER)

  @classmethod
  def create(cls, title=None, id=None, href=None, url=None, type=None,
             email=None, authorizations=None):
    """Create Person object.

    Random values will be used for title aka name.
    Predictable values will be used for mail and system_wide_role.
    """
    person_entity = cls._create_random_person()
    person_entity = cls.update_obj_attrs_values(
        obj=person_entity, title=title, id=id, href=href, url=url, type=type,
        email=email, authorizations=authorizations)
    return person_entity

  @classmethod
  def _create_random_person(cls):
    """Create Person entity with randomly filled fields."""
    random_person = entity.Person()
    random_person.title = cls._generate_title(cls._obj_person)
    random_person.type = cls._obj_person
    random_person.email = cls._generate_email()
    random_person.authorizations = roles.NO_ROLE
    return random_person


class CAFactory(EntitiesFactory):
  """Factory class for Custom Attribute entity."""

  @classmethod
  def create(cls, title=None, ca_type=None, definition_type=None, helptext="",
             placeholder=None, multi_choice_options=None, is_mandatory=False,
             ca_global=True):
    """Create CustomAttribute object.

    Random values will be used for title, ca_type, definition_type and
    multi_choice_options if they are None.
    """
    ca_entity = cls._create_random_ca()
    ca_entity = cls._fill_ca_entity_fields(
        ca_entity, title=title,
        ca_type=ca_type, definition_type=definition_type, helptext=helptext,
        placeholder=placeholder, multi_choice_options=multi_choice_options,
        is_mandatory=is_mandatory, ca_global=ca_global)
    ca_entity = cls._normalize_ca_definition_type(ca_entity)
    return ca_entity

  @classmethod
  def _create_random_ca(cls):
    """Create CustomAttribute entity with randomly filled fields."""
    random_ca = entity.CustomAttribute()
    random_ca.ca_type = random.choice(AdminWidgetCustomAttrs.ALL_ATTRS_TYPES)
    random_ca.title = cls._generate_title(random_ca.ca_type)
    random_ca.definition_type = random.choice(objects.ALL_CA_OBJECTS)
    return random_ca

  @classmethod
  def _fill_ca_entity_fields(cls, ca_object, **ca_object_fields):
    """Set the CustomAttributes object's attributes."""
    if ca_object_fields.get("ca_type"):
      ca_object.ca_type = ca_object_fields["ca_type"]
      ca_object.title = cls._generate_title(ca_object.ca_type)
    if ca_object_fields.get("definition_type"):
      ca_object.definition_type = ca_object_fields["definition_type"]
    if ca_object_fields.get("title"):
      ca_object.title = ca_object_fields["definition_type"]

    # "Placeholder" field exists only for Text and Rich Text.
    if (ca_object_fields.get("placeholder") and
        ca_object.ca_type in (AdminWidgetCustomAttrs.TEXT,
                              AdminWidgetCustomAttrs.RICH_TEXT)):
      ca_object.placeholder = ca_object_fields["placeholder"]

    if ca_object_fields.get("helptext"):
      ca_object.helptext = ca_object_fields["helptext"]
    if ca_object_fields.get("is_mandatory"):
      ca_object.is_mandatory = ca_object_fields["is_mandatory"]
    if ca_object_fields.get("ca_global"):
      ca_object.ca_global = ca_object_fields["ca_global"]

    # "Possible Values" - is a mandatory field for dropdown CustomAttribute.
    if ca_object.ca_type == AdminWidgetCustomAttrs.DROPDOWN:
      if (ca_object_fields.get("multi_choice_options") and
              ca_object_fields["multi_choice_options"] is not None):
        ca_object.multi_choice_options =\
            ca_object_fields["multi_choice_options"]
      else:
        ca_object.multi_choice_options = random_list_strings(list_len=3)
    return ca_object

  @classmethod
  def _normalize_ca_definition_type(cls, ca_object):
    """Transform definition type to title form.

    Title from used for UI operations.
    For REST operations definition type should be interpreted as
    objects.get_singular().get_object_name_form().
    """
    ca_object.definition_type = objects.get_normal_form(
        ca_object.definition_type
    )
    return ca_object


class ProgramFactory(EntitiesFactory):
  """Factory class for Program entity."""

  @classmethod
  def create(cls, title=None, id=None, href=None, url=None, type=None,
             manager=None, pr_contact=None, code=None, state=None,
             last_update=None):
    """Create Program object.

    Random values will be used for title and code.
    Predictable values will be used for type, manager, pr_contact, state.
    """
    program_entity = cls._create_random_program()
    program_entity = cls.update_obj_attrs_values(
        obj=program_entity, title=title, id=id, href=href, url=url, type=type,
        manager=manager, pr_contact=pr_contact, code=code, state=state,
        last_update=last_update)
    return program_entity

  @classmethod
  def _create_random_program(cls):
    """Create Program entity with randomly and predictably filled fields."""
    # pylint: disable=protected-access
    random_program = entity.Program()
    random_program.title = cls._generate_title(cls._obj_program)
    random_program.type = cls._obj_program
    random_program.code = cls._generate_code()
    random_program.manager = roles.DEFAULT_USER
    random_program.pr_contact = roles.DEFAULT_USER
    random_program.state = element.ObjectStates.DRAFT
    return random_program


class ControlFactory(EntitiesFactory):
  """Factory class for Control entity."""

  @classmethod
  def create(cls, title=None, id=None, href=None, url=None, type=None,
             owner=None, pr_contact=None, code=None, state=None,
             last_update=None):
    """Create Control object.

    Random values will be used for title and code.
    Predictable values will be used for type, owner, pr_contact, state.
    """
    control_entity = cls._create_random_control()
    control_entity = cls.update_obj_attrs_values(
        obj=control_entity, title=title, id=id, href=href, url=url, type=type,
        owner=owner, pr_contact=pr_contact, code=code, state=state,
        last_update=last_update)
    return control_entity

  @classmethod
  def _create_random_control(cls):
    """Create Control entity with randomly and predictably filled fields."""
    # pylint: disable=protected-access
    random_control = entity.Control()
    random_control.title = cls._generate_title(cls._obj_control)
    random_control.type = cls._obj_control
    random_control.code = cls._generate_code()
    random_control.owner = roles.DEFAULT_USER
    random_control.pr_contact = roles.DEFAULT_USER
    random_control.state = element.ObjectStates.DRAFT
    return random_control


class AuditFactory(EntitiesFactory):
  """Factory class for Audit entity."""

  @classmethod
  def create(cls, title=None, id=None, href=None, url=None, type=None,
             program=None, audit_lead=None, code=None, status=None,
             last_update=None):
    """Create Audit object.

    Random values will be used for title and code.
    Predictable values will be used for type, audit_lead, status.
    """
    audit_entity = cls._create_random_audit()
    audit_entity = cls.update_obj_attrs_values(
        obj=audit_entity, title=title, id=id, href=href, url=url, type=type,
        program=program, audit_lead=audit_lead, code=code, status=status,
        last_update=last_update)
    return audit_entity

  @classmethod
  def _create_random_audit(cls):
    """Create Audit entity with randomly and predictably filled fields."""
    # pylint: disable=protected-access
    random_audit = entity.Audit()
    random_audit.title = cls._generate_title(cls._obj_audit)
    random_audit.type = cls._obj_audit
    random_audit.code = cls._generate_code()
    random_audit.audit_lead = roles.DEFAULT_USER
    random_audit.status = element.AuditStates.PLANNED
    return random_audit


class AsmtTmplFactory(EntitiesFactory):
  """Factory class for Assessment Template entity."""

  @classmethod
  def create(cls, title=None, id=None, href=None, url=None, type=None,
             audit=None, asmt_objects=None, def_assessors=None,
             def_verifiers=None, code=None, last_update=None):
    """Create Assessment Template object.

    Random values will be used for title and code.
    Predictable values will be used for type, asmt_objects, def_assessors,
    def_verifiers.
    """
    asmt_tmpl_entity = cls._create_random_asmt_tmpl()
    asmt_tmpl_entity = cls.update_obj_attrs_values(
        obj=asmt_tmpl_entity, title=title, id=id, href=href, url=url,
        type=type, audit=audit, asmt_objects=asmt_objects,
        def_assessors=def_assessors, def_verifiers=def_verifiers, code=code,
        last_update=last_update)
    return asmt_tmpl_entity

  @classmethod
  def _create_random_asmt_tmpl(cls):
    """Create Assessment Template entity with randomly and predictably
    filled fields.
    """
    random_asmt_tmpl = entity.AsmtTmpl()
    random_asmt_tmpl.title = cls._generate_title(cls._obj_asmt_tmpl)
    random_asmt_tmpl.type = cls._obj_asmt_tmpl
    random_asmt_tmpl.code = cls._generate_code()
    random_asmt_tmpl.asmt_objects = objects.CONTROLS
    random_asmt_tmpl.def_assessors = roles.OBJECT_OWNERS
    random_asmt_tmpl.def_verifiers = roles.OBJECT_OWNERS
    return random_asmt_tmpl


class AsmtFactory(EntitiesFactory):
  """Factory class for Assessment entity."""

  @classmethod
  def generate(cls, objs_under_asmt_tmpl, audit):
    """Generate Assessment object according to:
    objects' under Assessment Template titles from list objects
    "objs_under_asmt_tmpl", audit's title from "audit", the total number of
    objects under Assessment Template.
    """
    # pylint: disable=too-many-locals
    from lib.service.rest_service import ObjectsInfoService
    actual_count_all_asmts = ObjectsInfoService().get_total_count(
        obj_name=objects.get_normal_form(cls._obj_asmt)
    )
    return [
        cls.create(
            title=obj_under_asmt_tmpl.title + " assessment for " + audit.title,
            code=(cls._obj_asmt.upper() + "-" + str(asmt_number)),
            audit=audit.title) for asmt_number, obj_under_asmt_tmpl in
        enumerate(objs_under_asmt_tmpl, start=actual_count_all_asmts + 1)]

  @classmethod
  def create(cls, title=None, id=None, href=None, url=None, type=None,
             object=None, audit=None, creators=None, assignees=None,
             pr_contact=None, is_verified=None, code=None, state=None,
             last_update=None):
    """Create Assessment object.

    Random values will be used for title and code.
    Predictable values will be used for type, object, creators, assignees,
    state, is_verified.
    """
    asmt_entity = cls._create_random_asmt()
    asmt_entity = cls.update_obj_attrs_values(
        obj=asmt_entity, title=title, id=id, href=href, url=url, type=type,
        object=object, audit=audit, creators=creators, assignees=assignees,
        pr_contact=pr_contact, is_verified=is_verified, code=code, state=state,
        last_update=last_update)
    return asmt_entity

  @classmethod
  def _create_random_asmt(cls):
    """Create Assessment entity with randomly and predictably filled fields."""
    random_asmt = entity.Asmt()
    random_asmt.title = cls._generate_title(cls._obj_asmt)
    random_asmt.type = cls._obj_asmt
    random_asmt.code = cls._generate_code()
    random_asmt.object = roles.DEFAULT_USER
    random_asmt.creators = roles.DEFAULT_USER
    random_asmt.assignees = roles.DEFAULT_USER
    random_asmt.state = element.AsmtStates.NOT_STARTED
    random_asmt.is_verified = element.Common.FALSE
    return random_asmt
