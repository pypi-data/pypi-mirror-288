import unittest

from django_channels_utils.abstract_consumer_handler import AbstractConsumerHandler, MethodMissingError, TypeMissingError 

class TestAbstractConsumerHandler(unittest.TestCase):
    def test_subclass_missing_type(self):
        # Define a subclass without a type attribute
        with self.assertRaises(TypeMissingError):
            class MissingTypeHandler(AbstractConsumerHandler):
                def handle(self):
                    pass

    def test_subclass_missing_handle_method(self):
        # Define a subclass without a handle method
        with self.assertRaises(MethodMissingError):
            class MissingHandleMethodHandler(AbstractConsumerHandler):
                type = 'test'

    def test_subclass_with_all_requirements(self):
        # Define a valid subclass
        class ValidHandler(AbstractConsumerHandler):
            type = 'test'
            def handle(self):
                pass
        
        # Ensure that the handlers dictionary contains the new handler
        self.assertIn('test', AbstractConsumerHandler.handlers)
        self.assertEqual(AbstractConsumerHandler.handlers['test'], ValidHandler)

    def test_multiple_valid_subclasses(self):
        # Define multiple valid subclasses
        class FirstHandler(AbstractConsumerHandler):
            type = 'first'
            def handle(self):
                pass

        class SecondHandler(AbstractConsumerHandler):
            type = 'second'
            def handle(self):
                pass

        # Ensure that both handlers are registered correctly
        self.assertIn('first', AbstractConsumerHandler.handlers)
        self.assertEqual(AbstractConsumerHandler.handlers['first'], FirstHandler)

        self.assertIn('second', AbstractConsumerHandler.handlers)
        self.assertEqual(AbstractConsumerHandler.handlers['second'], SecondHandler)

    def test_handler_not_in_handlers_if_not_subclassed(self):
        # Define a class that is not a subclass of AbstractConsumerHandler
        class NonHandler:
            type = 'non_handler'
            def handle(self):
                pass

        # Ensure that the handlers dictionary does not contain this class
        self.assertNotIn('non_handler', AbstractConsumerHandler.handlers)
        
    def test_utils_import_are_correct(self):
        from django_channels_utils.utils import CustomError


if __name__ == '__main__':
    unittest.main()
