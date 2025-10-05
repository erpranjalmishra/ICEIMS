/* Track Admin JavaScript Enhancements */

(function($) {
    'use strict';
    
    $(document).ready(function() {
        // Add help text for description field
        var descField = $('#id_description');
        if (descField.length) {
            var helpText = $('<div class="track-admin-help">')
                .html('<strong>Tip:</strong> Add one topic per line. Each line will be displayed as a separate bullet point on the website.');
            descField.before(helpText);
            
            // Add line counter
            var lineCounter = $('<div class="help" style="margin-top: 5px;">')
                .text('Lines: 0');
            descField.after(lineCounter);
            
            function updateLineCount() {
                var lines = descField.val().split('\n').filter(function(line) {
                    return line.trim().length > 0;
                }).length;
                lineCounter.text('Topics: ' + lines);
            }
            
            descField.on('input', updateLineCount);
            updateLineCount();
        }
        
        // Color picker enhancement
        var colorField = $('#id_color');
        if (colorField.length) {
            var preview = $('<div>')
                .css({
                    'width': '100px',
                    'height': '40px',
                    'border': '1px solid #ccc',
                    'margin-top': '5px',
                    'background-color': colorField.val()
                });
            colorField.after(preview);
            
            colorField.on('change', function() {
                preview.css('background-color', $(this).val());
            });
        }
        
        // Track number validation
        var trackNumField = $('#id_track_number');
        if (trackNumField.length) {
            trackNumField.on('blur', function() {
                var val = parseInt($(this).val());
                if (val < 1) {
                    alert('Track number must be greater than 0');
                    $(this).val(1);
                }
            });
        }
    });
})(django.jQuery);
