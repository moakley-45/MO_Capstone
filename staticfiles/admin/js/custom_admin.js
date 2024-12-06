$(document).ready(function() {
    var checkbox = function(context) {
        var ui = $.summernote.ui;
        var button = ui.button({
            contents: '<i class="fa fa-check-square-o"/>',
            tooltip: 'Checkbox',
            click: function() {
                context.invoke('editor.insertText', '☐ ');
            }
        });
        return button.render();
    }

    $('.summernote').summernote('addButton', 'checkbox', checkbox);
});
