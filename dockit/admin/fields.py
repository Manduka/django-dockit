from django.forms import fields, widgets, ValidationError
from django.core.urlresolvers import reverse

from django.utils.encoding import force_unicode
from django.forms.util import flatatt
from django.utils.safestring import mark_safe

from dockit.models import TemporarySchemaStorage

class LinkedJSONWidget(widgets.Input):
    input_type = 'hidden'
    
    def __init__(self, uri):
        self.uri = uri
        super(LinkedJSONWidget, self).__init__()
    
    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            #TODO store fragment, fragment id is part of the url
            final_attrs['value'] = force_unicode(self._format_value(value))
        #TODO how do we configure the display?
        return mark_safe(u'<input%s /><a href="%s?_popup=1"/>Edit</a>' % (flatatt(final_attrs), reverse(self.uri)))

class EmbededSchemaField(fields.CharField):
    widget = LinkedJSONWidget
    
    def __init__(self, *args, **kwargs):
        self.view = kwargs.pop('view')
        if 'widget' not in kwargs:
            kwargs['widget'] = self.widget(self.view.uri)
        super(EmbededSchemaField, self).__init__(*args, **kwargs)
    
    def to_python(self, value):
        storage = TemporarySchemaStorage.objects.get(value)
        if storage.identifier != self.view.get_identifier():
            raise ValidationError('This object does not match the field type.')
        return storage.data
        

