from .abstract_consumer_handler_errors import TypeMissingError, MethodMissingError
from .const import HANDLER_ABSTRACT_CLASS_NAME


class HandlerMeta(type):
    def __new__(cls, name, bases, class_dict):
        new_cls = super().__new__(cls, name, bases, class_dict)
        if not hasattr(new_cls, 'handlers'):
            new_cls.handlers = {}
        is_handler_class_name_in_bases = HANDLER_ABSTRACT_CLASS_NAME in [base.__name__ for base in bases]            
        if not is_handler_class_name_in_bases:
            return new_cls
        if not hasattr(new_cls, 'type'):
            raise TypeMissingError(name)
        if not hasattr(new_cls, 'handle'):
            raise MethodMissingError(name, 'handle')
        new_cls.handlers[new_cls.type]=new_cls                        
        return new_cls                
        

class AbstractConsumerHandler(metaclass=HandlerMeta):
    '''
    Abstract class for websocket host handlers to subclass from
    Subclassed handlers should have type attribute and handler method    
    '''
    def __init__(self):
        super().__init__()
        
        
