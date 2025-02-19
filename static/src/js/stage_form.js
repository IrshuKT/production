odoo.define('stage_form_custom_js', function (require) {
    "use strict";

    var FormController = require('web.FormController');

    FormController.include({
        start: function() {
            this._super.apply(this, arguments);  // Call the parent start method
            this._bindTabClick();  // Attach event handler once
        },

        _bindTabClick: function() {
            var self = this;
            // Attach the event listener to the tab click only once
            this.$el.off('click', '.o_notebook_headers .nav-item a'); // Ensure no duplicate bindings
            this.$el.on('click', '.o_notebook_headers .nav-item a', function () {
                // Get the index of the clicked tab
                var tabIndex = $(this).parent().index();
                console.log("Notebook tab index clicked:", tabIndex); // Debug: Log the tab index

                // Map the tab index to the corresponding stage status
                var stageStatus = '';
                if (tabIndex === 0) {
                    stageStatus = 'stage_1'; // First tab corresponds to Stage 1
                } else if (tabIndex === 1) {
                    stageStatus = 'stage_2'; // Second tab corresponds to Stage 2
                }
                console.log("Stage status to be updated:", stageStatus); // Debug: Log the stage status

                // Get the record ID
                var recordId = self.renderer.state.res_id; // Use res_id to get the record ID
                console.log("Record ID from res_id:", recordId); // Debug: Log the record ID

                // If res_id is undefined, try extracting the ID from the URL
                if (!recordId) {
                    console.log("Window location hash:", window.location.hash); // Debug: Log the URL hash
                    var idParam = new URLSearchParams(window.location.hash.substring(1)).get('id');
                    if (idParam) {
                        recordId = parseInt(idParam, 10);
                    }
                    console.log("Record ID from URL:", recordId); // Debug: Log the record ID
                }

                // Update the stage_status field in the database
                if (stageStatus && recordId) {
                    self._rpc({
                        model: 'stage.main',
                        method: 'write',
                        args: [recordId, { stage_status: stageStatus }],
                    }).then(function () {
                        console.log("Stage status updated successfully"); // Debug: Log success

                        // Update the form state directly (force UI update)
                        self._updateStatusbar(stageStatus);

                    }).catch(function (error) {
                        console.error("Error updating stage status:", error); // Debug: Log errors
                    });
                } else if (!recordId) {
                    console.log("Skipping update: No record ID (creation mode)"); // Debug: Log creation mode
                } else {
                    console.error("Record ID or stage status is invalid"); // Debug: Log invalid state
                }
            });
        },

        // New method to update the statusbar widget
        _updateStatusbar: function(stageStatus) {
            // Triggering a refresh of the statusbar widget without reloading the page
            var statusBar = this.$el.find('[name="stage_status"]'); // The statusbar field
            if (statusBar.length) {
                statusBar.val(stageStatus); // Set the new status
                statusBar.trigger('change'); // Trigger change event to update the UI
            }
        },

        destroy: function () {
            // Clean up event listener when the form is destroyed
            this.$el.off('click', '.o_notebook_headers .nav-item a');
            this._super.apply(this, arguments);  // Call parent destroy method
        }
    });
});
