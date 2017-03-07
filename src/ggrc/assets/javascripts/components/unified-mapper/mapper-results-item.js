/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC, CMS) {
  'use strict';

  GGRC.Components('mapperResultsItem', {
    tag: 'mapper-results-item',
    template: can.view(
      GGRC.mustache_path +
      '/components/unified-mapper/mapper-results-item.mustache'
    ),
    viewModel: {
      itemData: {},
      searchOnly: false,
      drawRelatedAssessments: false,
      selectedColumns: [],
      showDetails: false,
      title: function () {
        var displayItem = this.displayItem();
        return displayItem.title ||
          displayItem.description_inline ||
          displayItem.name ||
          displayItem.email;
      },
      displayItem: function () {
        var itemData = this.attr('itemData');
        return itemData.revision ?
          itemData.revision.content :
          itemData;
      },
      objectTypeIcon: function () {
        var objectType = this.objectType();
        var Model = CMS.Models[objectType];
        return 'fa-' + Model.table_singular;
      },
      toggleIconCls: function () {
        return this.attr('showDetails') ? 'fa-caret-down' : 'fa-caret-right';
      },
      toggleDetails: function () {
        this.attr('showDetails', !this.attr('showDetails'));
      },
      isSnapshot: function () {
        return this.attr('itemData.type') ===
          CMS.Models.Snapshot.model_singular;
      },
      objectType: function () {
        if (this.isSnapshot()) {
          return this.attr('itemData.child_type');
        }
        return this.attr('itemData.type');
      },
      showRelatedAssessments: function () {
        this.dispatch({
          type: 'showRelatedAssessments',
          instance: this.displayItem()
        });
      }
    }
  });
})(window.can, window.GGRC, window.CMS);
