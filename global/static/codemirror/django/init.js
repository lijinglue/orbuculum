(function () {
    var $ = django.jQuery;
    $(document).ready(function () {
        $('textarea.js-editor').each(function (idx, el) {
            CodeMirror.fromTextArea(el, {
                lineNumbers: true,
                mode: 'javascript',
                keyMap: 'vim'
            });
        });
    });
})();