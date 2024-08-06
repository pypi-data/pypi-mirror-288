from ..utils.abstract_custom_error import CustomError

class TypeMissingError(CustomError):
    """Exception raised for errors in the subclass definition.

    Attributes:
        subclass_name -- name of the subclass which caused the error
        message -- explanation of the error
    """

    def __init__(self, subclass_name, message="Type attribute is missing in subclass"):
        self.subclass_name = subclass_name
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.subclass_name} -> {self.message}'
    
    
class MethodMissingError(CustomError):
    """Exception raised for missing required methods in subclass.

    Attributes:
        subclass_name -- name of the subclass which caused the error
        method_name -- name of the missing method
        message -- explanation of the error
    """

    def __init__(self, subclass_name, method_name, message=None):
        self.subclass_name = subclass_name
        self.method_name = method_name
        if message is None:
            message = f"'{method_name}' method is missing in subclass '{subclass_name}'"
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message    