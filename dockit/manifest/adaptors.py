from common import DataAdaptor, register_adaptor

import json
from django.core.serializers.json import DjangoJSONEncoder

class JSONAdaptor(DataAdaptor):
    def deserialize(self, file_obj):
        return json.loads(file_obj)
    
    def serialize(self, python_objects):
        return json.dumps(python_objects, cls=DjangoJSONEncoder)

register_adaptor('json', JSONAdaptor)

class XMLAdaptor(DataAdaptor):
    pass

register_adaptor('xml', XMLAdaptor)
