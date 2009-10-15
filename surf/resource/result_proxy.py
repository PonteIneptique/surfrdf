from surf.util import attr2rdf
# hello

class ResultProxy(object):
    def __init__(self, params = {}, store = None, instancemaker = None):
        self.__params = params
        self.__data_cache = None
        
        if store:
            self.__params["store"] = store

        if instancemaker:
            self.__params["instancemaker"] = instancemaker

    def instancemaker(self, value):
        params = self.__params.copy()
        params["instancemaker"] = value
        return ResultProxy(params)

    def limit(self, value):
        params = self.__params.copy()
        params["limit"] = value
        return ResultProxy(params)

    def offset(self, value):
        params = self.__params.copy()
        params["offset"] = value
        return ResultProxy(params)
    
    def full(self, only_direct = False):
        params = self.__params.copy()
        params["full"] = True
        params["only_direct"] = only_direct
        return ResultProxy(params)
    
    def order(self, value = True):
        params = self.__params.copy()
        params["order"] = value
        return ResultProxy(params)
    
    def desc(self):
        params = self.__params.copy()
        params["desc"] = True
        return ResultProxy(params)
    
    def get_by(self, **kwargs):
        params = self.__params.copy()
        params["get_by"] = []
        for name, value in kwargs.items():
            attr, direct = attr2rdf(name)
            params["get_by"].append((attr, value, direct))
        return ResultProxy(params)

    def context(self, context):
        params = self.__params.copy()
        params["context"] = context
        return ResultProxy(params)
    
    def __get_data_cache(self):
        if self.__data_cache is None:
            self.__execute()
        
        return self.__data_cache
    
    def __execute(self):
        store = self.__params["store"]
        
        get_by_args = {}
        for key in ["limit", "offset", "full", "order", "desc", "get_by", 
                    "only_direct", "context"]:
            if key in self.__params:
                get_by_args[key] = self.__params[key]
        
        instancemaker = self.__params["instancemaker"]
        if self.__data_cache is None:
            self.__data_cache = store.get_by(get_by_args)

        for instance_data in self.__get_data_cache():
            yield instancemaker(get_by_args, instance_data)

        
    def __iter__(self):
        return self.__execute()
