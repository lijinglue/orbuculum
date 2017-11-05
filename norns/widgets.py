from django import forms


class JsEditor(forms.Textarea):
    def __init__(self, *args, **kwargs):
        super(JsEditor, self).__init__(*args, **kwargs)
        self.attrs['class'] = 'js-editor'

    class Media:
        css = {
            'all': (
                'codemirror/lib/codemirror.css',
            )
        }
        js = (
            'codemirror/lib/codemirror.js',
            'codemirror/mode/javascript/javascript.js',
            'codemirror/keymap/vim.js',
            'codemirror/django/init.js'
        )