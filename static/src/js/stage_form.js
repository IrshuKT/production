odoo.define('stage_form_custom_js', function (require) {
    "use strict";

    var FormController = require('web.FormController');

    FormController.include({
        renderButtons: function ($node) {
            this._super.apply(this, arguments);

            var self = this;
            var reloadInProgress = false;

            this.$el.off('click', '.o_notebook_headers .nav-item a');
            this.$el.on('click', '.o_notebook_headers .nav-item a', function () {
                var tabIndex = $(this).parent().index();
                var stageStatus = '';
                if (tabIndex === 0) {
                    stageStatus = 'stage_1';
                } else if (tabIndex === 1) {
                    stageStatus = 'stage_2';
                } else if (tabIndex === 2) {
                    stageStatus = 'stage_3';
                } else if (tabIndex === 3) {
                    stageStatus = 'stage_4';
                } else if (tabIndex === 4) {
                    stageStatus = 'stage_5';
                } else if (tabIndex === 5) {
                    stageStatus = 'stage_6';
                }

                var recordId = self.renderer.state.res_id;
                if (!recordId) {
                    var idParam = new URLSearchParams(window.location.hash.substring(1)).get('id');
                    if (idParam) {
                        recordId = parseInt(idParam, 10);
                    }
                }

                if (!recordId) {
                    console.log("Skipping update: No record ID (creation mode)");
                    return; // Exit the function if no record ID
                }

                if (stageStatus && recordId) {
                    var currentStageStatus = self.renderer.state.data.stage_status; // Get the current stage status
                    console.log("Current Stage Status: ", currentStageStatus);
                    console.log("New Stage Status: ", stageStatus);

                    if (currentStageStatus !== stageStatus) { // only write if stage status has changed.
                        self._rpc({
                            model: 'stage.main',
                            method: 'write',
                            args: [recordId, { stage_status: stageStatus }],
                        }).then(function () {
                            console.log("Stage status updated successfully");
                            if (!reloadInProgress) {
                                reloadInProgress = true;
                                self.reload().then(function() {
                                    reloadInProgress = false;
                                });
                            }
                        }).catch(function (error) {
                            console.error("Error updating stage status:", error);
                        });
                    } else {
                        console.log("Stage Status unchanged, skipping write and reload.");
                    }
                } else {
                    console.error("Stage status is empty or invalid record ID");
                }
            });
        }
    });
});