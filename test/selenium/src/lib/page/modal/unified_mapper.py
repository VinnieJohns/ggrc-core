# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Modals for map objects."""

from selenium.webdriver.common.by import By
from lib import base
from lib.constants import locator
from lib.utils import string_utils, selenium_utils


class CommonUnifiedMapperModal(base.Modal):
  """Common unified mapper modal."""
  _locators = locator.ModalMapObjects

  def __init__(self, driver, obj_name):
    super(CommonUnifiedMapperModal, self).__init__(driver)
    # labels
    self.title_modal = base.Label(driver, self._locators.MODAL_TITLE)
    self.obj_type = base.Label(driver, self._locators.OBJ_TYPE)
    self.filter_by_expression = base.Label(
        driver, self._locators.FILTER_BY_EXPRESSION)
    # user input elements
    self.filter_via_expression_text_box = base.TextInputField(
        driver, self._locators.FILTER_VIA_EXPRESSION_TEXT_BOX)
    self.filter_by_state_text_box = base.DropdownStatic(
        driver, self._locators.FILTER_BY_STATE_DROPDOWN,
        self._locators.FILTER_BY_STATE_DROPDOWN_OPTIONS)
    self.tree_view = TreeView(driver, obj_name)

  def select_dest_obj_type(self, obj_name, is_asmts_generation=False):
    """Open dropdown and select element according to destination object name.
    If is_asmts_generation then TextFilterDropdown, else DropdownStatic.
    """
    obj_type_dropdown = base.DropdownStatic(
        self._driver, self._locators.OBJ_TYPE_DROPDOWN,
        self._locators.OBJ_TYPE_DROPDOWN_OPTIONS)
    obj_type_dropdown.select(obj_name)
    if is_asmts_generation:
      asmt_tmpl_dropdown = base.TextFilterDropdown(
          self._driver, self._locators.OBJ_TYPE_DROPDOWN,
          self._locators.OBJ_TYPE_DROPDOWN_OPTIONS)
      asmt_tmpl_dropdown.find_and_select_el_by_text(obj_name)

  def filter_dest_objs_via_expression_by_titles(self, objs_titles):
    """Enter expression is like 'title=obj1_title or title=obj2_title' into
    filter via expression text box according to destination objects titles.
    """
    # pylint: disable=invalid-name
    expression = string_utils.get_exp_to_filter_by_titles(titles=objs_titles)
    self.filter_via_expression_text_box.enter_text(expression)

  def search_dest_objs(self):
    """Click Search button to search objects according set filters."""
    base.Button(self._driver, self._locators.BUTTON_SEARCH).click()

  def select_dest_objs_to_map(self, objs_titles):
    """Select checkboxes regarding to titles from list of checkboxes
    according to destinations objects titles.
    """
    dest_objs = base.ListCheckboxes(
        self._driver, self._locators.FOUND_OBJECTS_TITLES,
        self._locators.FOUND_OBJECTS_CHECKBOXES)
    dest_objs.select_by_titles(objs_titles)

  def confirm_map_selected(self):
    """Select Map Selected button to confirm map selected objects to
    source object.
    """
    base.Button(self._driver, self._locators.BUTTON_MAP_SELECTED).click()
    selenium_utils.get_when_invisible(
        self._driver, self._locators.BUTTON_MAP_SELECTED)
    selenium_utils.get_when_invisible(
        self._driver, locator.TreeView.NO_RESULTS_MESSAGE)

  def filter_and_search_dest_objs(self, dest_objs_type, dest_objs_titles,
                                     is_asmts_generation=False):
    """Filter and search destination objects according to them type and titles.
    If is_asmts_generation then TextFilterDropdown is using.
    """
    self.select_dest_obj_type(obj_name=dest_objs_type,
                              is_asmts_generation=is_asmts_generation)
    self.filter_dest_objs_via_expression_by_titles(
        objs_titles=dest_objs_titles)
    self.search_dest_objs()
    return self.tree_view.get_list_members_as_list_scopes()

  def get_list_of_objs_from_search_results(self, dest_objs_type, dest_objs_titles,
                                     is_asmts_generation=False):
    # filter and search
    # set fields
    # get list of objects
    # return list
    self.get_obj()
    self.get_is_checked()
    self.get_is_enabled()

  def filter_search_and_get_list_objs(self, dest_objs_type, dest_objs_titles,
                                         is_asmts_generation=False):
    """Filter and search destination objects according to them type and titles.
       If is_asmts_generation then TextFilterDropdown is using.
       Return list of objects found
    """
    self.filter_and_search_dest_objs(dest_objs_type, dest_objs_titles,
                                     is_asmts_generation=is_asmts_generation)
    objs_list = self.get_list_of_objs_from_search_results(dest_objs_type)

  def filter_search_and_map_dest_objs(self, dest_objs_type, dest_objs_titles,
                                      is_asmts_generation=False):
    """Filter, search destination objects according to them type and titles.
    Map found destination objects to source object.
    If is_asmts_generation then TextFilterDropdown is using.
    """
    self.filter_and_search_dest_objs(dest_objs_type, dest_objs_titles,
                                     is_asmts_generation=is_asmts_generation)
    self.select_dest_objs_to_map(objs_titles=dest_objs_titles)
    self.confirm_map_selected()


class TreeView(base.TreeView):
  _locators = locator.UnifiedMapperTreeView

  def __init__(self, driver, obj_name):
    super(TreeView, self).__init__(driver, obj_name)
    self.locator_set_visible_fields = (By.CSS_SELECTOR,
                                       self._locators.BUTTON_SHOW_FIELDS)
    self._tree_view_header_elements = []
    self._tree_view_items_elements = []
    self._tree_view_items = []

  def open_set_visible_fields(self):
    """Click to Set Visible Fields button on Tree View to open
    Set Visible Fields modal.
    Return: lib.page.modal.set_fields.SetVisibleFieldsModal
    """
    _locator_set_visible_fields = self.locator_set_visible_fields
    base.Button(self._driver, _locator_set_visible_fields).click()
    return SetVisibleFieldsModal(self._driver, self.fields_to_set)


class SetVisibleFieldsModal(base.SetVisibleFieldsModal):
  """Modal to select and set visible fields for objects to represent them on
  Tree View."""
  _locators = locator.ModalSetVisibleFieldsMapper


class MapObjectsModal(CommonUnifiedMapperModal):
  """Modal for map objects."""
  _locators = locator.ModalMapObjects

  def __init__(self, driver, obj_name):
    super(MapObjectsModal, self).__init__(driver, obj_name)


class SearchObjectsModal(CommonUnifiedMapperModal):
  """Modal for map objects."""
  _locators = locator.ModalMapObjects

  def __init__(self, driver):
    super(SearchObjectsModal, self).__init__(driver)


class GenerateAssessmentsModal(CommonUnifiedMapperModal):
  """Modal for map objects."""
  _locators = locator.ModalGenerateAssessments

  def __init__(self, driver):
    super(GenerateAssessmentsModal, self).__init__(driver)

  def filter_search_and_generate_asmts(self, asmt_tmpl_title,
                                       objs_under_asmt_titles):
    """Filter, search objects under Assessment according to them titles.
    Generate Assessments based on found objects under Assessment.
    """
    # pylint: disable=invalid-name
    self.filter_search_and_map_dest_objs(
        dest_objs_type=asmt_tmpl_title,
        dest_objs_titles=objs_under_asmt_titles, is_asmts_generation=True)
