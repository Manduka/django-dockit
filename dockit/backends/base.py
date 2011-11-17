
class BaseDocumentStorage(object):
    def register_document(self, document):
        for key, field in document._meta.fields.iteritems():
            if getattr(field, 'db_index', False):
                self.generate_index(document.collection, field)
    
    def save(self, collection, data):
        raise NotImplementedError
    
    def get(self, collection, doc_id):
        raise NotImplementedError
    
    def delete(self, collection, doc_id):
        raise NotImplementedError
    
    def generate_index(self, collection, field):
        raise NotImplementedError
    
    def define_index(self, collection, name, index):
        raise NotImplementedError
    
    def call_index(self, doc_class, collection, name, **kwargs):
        raise NotImplementedError
    
    def all(self, doc_class, collection):
        raise NotImplementedError
    
    def filter(self, doc_class, collection, params):
        raise NotImplementedError
    
    def get_id(self, data):
        raise NotImplementedError

