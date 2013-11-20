# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: silas@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

from .base import *
from ggrc.models import Directive, Policy, Regulation, Contract, Standard, Objective, ObjectObjective
from .base_row import *
from collections import OrderedDict

DIRECTIVE_CLASSES = [Directive, Policy, Regulation, Contract, Standard]

class ObjectiveRowConverter(BaseRowConverter):
  model_class = Objective

  def find_by_slug(self, slug):
    from sqlalchemy import orm
    return self.model_class.query.filter_by(slug=slug).options(
        orm.joinedload('object_objectives')).first()

  def setup_object(self):
    self.obj = self.setup_object_by_slug(self.attrs)
    if self.obj.id is not None:
      self.add_warning('slug', "Objective already exists and will be updated")

  def reify(self):
    self.handle('slug', SlugColumnHandler)
    self.handle_raw_attr('title', is_required=True)
    self.handle_text_or_html('description')
    self.handle_raw_attr('url')
    self.handle_text_or_html('notes')
    self.handle_date('created_at', no_import=True)
    self.handle_date('updated_at', no_import=True)

  def save_object(self, db_session, **options):
    db_session.add(self.obj)

  def after_save(self, db_session, **options):
    parent_type = options.get('parent_type')
    if options.get('parent_type') in DIRECTIVE_CLASSES:
      parent_id = options.get('parent_id')
      parent_obj = parent_type.query.get(parent_id)
      parent_string = unicode(parent_obj.__class__.__name__)
      # check if no such directive/object mapping exists; if none, add
      matching_relationship = ObjectObjective.query\
        .filter(ObjectObjective.objectiveable_id==parent_id)\
        .filter(ObjectObjective.objectiveable_type==parent_string)\
        .filter(ObjectObjective.objective_id==self.obj.id)\
        .count()
      if matching_relationship == 0:
        db_session.add(ObjectObjective(
            objectiveable_type=parent_string,
            objectiveable_id=parent_id,
            objective=self.obj
        ))


class ObjectivesConverter(BaseConverter):

  metadata_map = OrderedDict([
    ('Type', 'type'),
    ('Directive Code', 'slug')
  ])

  object_map = OrderedDict([
    ('Objective Code', 'slug'),
    ('Title', 'title'),
    ('Description', 'description'),
    ('URL', 'url'),
    ('Notes', 'notes'),
    ('Created', 'created_at'),
    ('Updated', 'updated_at'),
  ])

  row_converter = ObjectiveRowConverter

  def validate_code(self, attrs):
    if not attrs.get('slug'):
      self.errors.append('Missing {} Code heading'.format(self.parent_type_string()))
    elif attrs['slug'] != self.parent_object().slug:
      self.errors.append('{0} Code must be {1}'.format(
          self.parent_type_string(),
          self.parent_object().slug
      ))

  # Creates the correct metadata_map for the specific directive kind.
  def create_metadata_map(self):
    parent_type = self.options.get('parent_type')
    if parent_type in DIRECTIVE_CLASSES:
      self.metadata_map = OrderedDict( [(k.replace("Directive", self.directive_kind()), v) \
                          if 'Directive' in k else (k, v) for k, v in self.metadata_map.items()] )

  def validate_metadata(self, attrs):
    self.validate_metadata_type(attrs, "Objectives")
    self.validate_code(attrs)

  def parent_object(self):
    parent_type = self.options['parent_type']
    return parent_type.query.get(self.options['parent_id'])

  def parent_type_string(self):
    return self.options.get('parent_type').__name__

  def directive_kind(self):
    parent_object = self.parent_object()
    return parent_object.meta_kind

  def do_export_metadata(self):
    yield self.metadata_map.keys()
    yield ['Objectives', self.parent_object().slug]
    yield[]
    yield[]
    yield self.object_map.keys()

