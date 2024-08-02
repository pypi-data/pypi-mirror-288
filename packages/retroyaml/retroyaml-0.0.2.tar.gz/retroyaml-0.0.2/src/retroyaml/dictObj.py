
class dictObj(object):
    
    def __init__(self, inObj: dict = dict()):
        self.__load__(inObj)

    def __load__(self, inObj):
        if inObj:
            self.__clear__()
            for obj in inObj:
                if issubclass(type(inObj[obj]), (dictObj, dict)):
                    self.__setattr__(obj, dictObj(inObj[obj]))
                else:
                    self.__setattr__(obj, inObj[obj])
    
    def __getitem__(self, item):
        return self.__to_dict__()[item]

    def __clear__(self):
        default_attributes = type(self)().__dir__()
        for attribute in list(self.__dir__()):
            if attribute not in default_attributes:
                self.__delattr__(attribute)
    
    def __to_dict__(self):
        default_attributes = type(self)().__dir__()
        extra_attributes = list(filter(lambda x: x not in default_attributes, self.__dir__()))
        out = dict()
        for attribute in extra_attributes:
            if issubclass(type(self.__dict__[attribute]), dictObj):
                out[attribute] = self.__dict__[attribute].__to_dict__()
            else:
                out[attribute] = self.__getattribute__(attribute)
        return out
    
    def __str__(self):
        return str(self.__to_dict__().__str__())
