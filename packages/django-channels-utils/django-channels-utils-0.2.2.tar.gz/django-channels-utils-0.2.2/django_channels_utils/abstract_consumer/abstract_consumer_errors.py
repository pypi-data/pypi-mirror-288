from ..utils.abstract_custom_error import CustomError

class HandlerMissingError(CustomError):
    """Exception raised when required consumer handler is not defined
    """
    
    def __init__(self, message_type, message="Consumer handler missing"):
        self.message_type = message_type
        self.message = message
        
        super().__init__(self.message)
        
    def __str__(self):
        return f'{self.message_type} -> {self.message}'
    
