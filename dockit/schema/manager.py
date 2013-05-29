from copy import copy

from dockit.backends.queryindex import QueryIndex

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

class Manager(object):
    def contribute_to_class(self, cls, name):
        new = copy(self)
        new.schema = cls
        setattr(cls, name, new)
    
    @property
    def backend(self):
        return self.schema._meta.get_backend()
    
    @property
    def collection(self):
        return self.schema._meta.collection
    
    def filter(self, **kwargs):
        return self.all().filter(**kwargs)
    
    def index(self, *args):
        return self.all().index(*args)
    
    #def values(self):
    #    return self.index_manager.values
    
    def all(self):
        return QueryIndex(self.schema)
    
    def count(self):
        return self.all().count()
    
    def get(self, **kwargs):
        return self.all().get(**kwargs)
    
    def filter_by_natural_key(self, hashval=None, **kwargs):
        if isinstance(hashval, dict):
            kwargs = hashval
            hashval = None
        if kwargs:
            if len(kwargs) == 1 and '@natural_key_hash' in kwargs:
                hashval = kwargs['@natural_key_hash']
            else:
                vals = tuple(kwargs.items())
                hashval = str(hash(vals))
        assert isinstance(hashval, basestring)
        return self.filter(**{'@natural_key_hash':hashval})
    
    def get_by_natural_key(self, hashval=None, **kwargs):
        qs = self.filter_by_natural_key(hashval, **kwargs)
        try:
            return qs.get()
        except MultipleObjectsReturned, error:
            raise MultipleObjectsReturned('Duplicate natural keys found! Lookup parameters were %s' % (hashval or kwargs))
        except ObjectDoesNotExist, error:
            raise ObjectDoesNotExist('Natural key not found! Lookup parameters were %s' % (hashval or kwargs))


