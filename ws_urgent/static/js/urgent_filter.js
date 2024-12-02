odoo.define('your_module_name.urgent_filter', function(require) {
    "use strict";

    var core = require('web.core');
    var Dropdown = require('web.Dropdown');

    // Add event listeners for the urgent filter dropdown
    $(document).ready(function() {
        // Show and hide filters on 'Urgent Filter' button click
        $('.urgent-filter-button').on('click', function() {
            $('.urgent-options').toggleClass('d-none');  // Toggle visibility of urgent options
        });
    });
});
