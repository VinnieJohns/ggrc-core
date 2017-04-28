/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (GGRC, can) {
  'use strict';

  var tag = 'assessment-urls-list';
  var template = can.view(GGRC.mustache_path +
    '/components/assessment/urls-list.mustache');

  /**
   * Wrapper Component for rendering and managing of url lists
   */
  GGRC.Components('assessmentUrlsListComponent', {
    tag: tag,
    template: template,
    viewModel: {
      define: {
        noItemsText: {
          type: 'string',
          value: ''
        }
      },
      mappedItems: []
    }
  });
})(window.GGRC, window.can);
