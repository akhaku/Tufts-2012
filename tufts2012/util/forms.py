from django.forms import ModelForm
from django.forms.widgets import TextInput, Textarea
from django.forms.util import ErrorList

class UtilModelForm(ModelForm):
    # Setup placeholder text based on help_text
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
            initial=None, error_class=ErrorList, label_suffix=':',
            empty_permitted=False, instance=None):
                                 
        super(UtilModelForm, self).__init__(data, files, auto_id, prefix, 
                initial, error_class, label_suffix, 
                empty_permitted, instance)
                
        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                if type(field.widget) == TextInput or type(field.widget) == Textarea:
                    field.widget.attrs["placeholder"] = field.help_text
                    try:
                        field.widget.attrs["maxlength"] = field.max_length 
                    except AttributeError:
                        pass
