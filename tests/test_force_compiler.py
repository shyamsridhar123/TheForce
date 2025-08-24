#!/usr/bin/env python3
"""
Comprehensive test suite for The Force Programming Language compiler
"""

import unittest
import sys
import os
import io

# Add parent directory to path to import force_compiler
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from force_compiler import ForceParser, ForceRuntime, ForceInterpreter


class TestForceParser(unittest.TestCase):
    """Test cases for the Force language parser"""
    
    def setUp(self):
        self.parser = ForceParser()
    
    def test_basic_variable_declaration(self):
        """Test basic variable declarations"""
        force_code = "holocron x = 5"
        python_code = self.parser.translate_to_python(force_code)
        self.assertIn("x = 5", python_code)
    
    def test_constant_declaration(self):
        """Test constant declarations"""
        force_code = "kyber PI = 3.14"
        python_code = self.parser.translate_to_python(force_code)
        self.assertIn("PI = 3.14", python_code)
    
    def test_function_definition(self):
        """Test function definitions"""
        force_code = """ability greet(name) {
            respond "Hello, " + name
        }"""
        python_code = self.parser.translate_to_python(force_code)
        self.assertIn("def greet(name):", python_code)
        self.assertIn("print(\"Hello, \" + name)", python_code)
    
    def test_class_definition(self):
        """Test class definitions"""
        force_code = """order Jedi {
            initiate(self, name) {
                self.name = name
            }
        }"""
        python_code = self.parser.translate_to_python(force_code)
        self.assertIn("class Jedi:", python_code)
        self.assertIn("def __init__(self, name):", python_code)
    
    def test_if_statement(self):
        """Test if statements"""
        force_code = """sense (x > 5) {
            respond "Greater than 5"
        } else {
            respond "Not greater than 5"
        }"""
        python_code = self.parser.translate_to_python(force_code)
        self.assertIn("if (x > 5):", python_code)
        self.assertIn("else:", python_code)
    
    def test_while_loop(self):
        """Test while loops"""
        force_code = """meditate (x < 10) {
            x = x + 1
        }"""
        python_code = self.parser.translate_to_python(force_code)
        self.assertIn("while (x < 10):", python_code)
    
    def test_for_loop(self):
        """Test for loops"""
        force_code = "train (holocron i = 0; i < 10; i = i + 1) { respond i }"
        python_code = self.parser.translate_to_python(force_code)
        self.assertIn("for i in range(0, 10, 1):", python_code)
    
    def test_array_declaration(self):
        """Test array declarations"""
        force_code = 'holocron missions = squadron["Tatooine", "Death Star"]'
        python_code = self.parser.translate_to_python(force_code)
        self.assertIn('missions = ["Tatooine", "Death Star"]', python_code)
    
    def test_dictionary_declaration(self):
        """Test dictionary declarations"""
        force_code = "holocron data = datapad { name: 'Luke', age: 20 }"
        python_code = self.parser.translate_to_python(force_code)
        self.assertIn('data = {"name": \'Luke\', "age": 20}', python_code)
    
    def test_comments_removal(self):
        """Test comment removal"""
        force_code = """// This is a comment
        holocron x = 5 // Another comment
        /* Block comment */"""
        python_code = self.parser.translate_to_python(force_code)
        self.assertNotIn("//", python_code)
        self.assertNotIn("/*", python_code)
        self.assertNotIn("*/", python_code)
    
    def test_string_formatting(self):
        """Test string formatting"""
        force_code = 'hologram_text("Hello {}", name)'
        python_code = self.parser.translate_to_python(force_code)
        self.assertIn('f"Hello {name}"', python_code)
    
    def test_ternary_operator(self):
        """Test ternary operator"""
        force_code = "jedi_mind_trick(x > 5, 'big', 'small')"
        python_code = self.parser.translate_to_python(force_code)
        self.assertIn("('big' if x > 5 else 'small')", python_code)


class TestForceRuntime(unittest.TestCase):
    """Test cases for the Force runtime environment"""
    
    def setUp(self):
        self.runtime = ForceRuntime()
    
    def test_force_random_no_args(self):
        """Test random number generation without arguments"""
        result = self.runtime._force_random()
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0)
        self.assertLess(result, 1)
    
    def test_force_random_with_max(self):
        """Test random number generation with maximum"""
        result = self.runtime._force_random(10)
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)
        self.assertLessEqual(result, 10)
    
    def test_force_random_with_range(self):
        """Test random number generation with range"""
        result = self.runtime._force_random(5, 15)
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 5)
        self.assertLessEqual(result, 15)
    
    def test_force_distance(self):
        """Test distance calculation"""
        distance = self.runtime._force_distance(0, 0, 3, 4)
        self.assertEqual(distance, 5.0)
    
    def test_force_format(self):
        """Test string formatting"""
        result = self.runtime._force_format("Hello {}", "World")
        self.assertEqual(result, "Hello World")
    
    def test_force_text_uppercase(self):
        """Test text processing - uppercase"""
        result = self.runtime._force_text("uppercase", "hello")
        self.assertEqual(result, "HELLO")
    
    def test_force_text_lowercase(self):
        """Test text processing - lowercase"""
        result = self.runtime._force_text("lowercase", "HELLO")
        self.assertEqual(result, "hello")
    
    def test_force_text_reverse(self):
        """Test text processing - reverse"""
        result = self.runtime._force_text("reverse", "hello")
        self.assertEqual(result, "olleh")
    
    def test_force_text_length(self):
        """Test text processing - length"""
        result = self.runtime._force_text("length", "hello")
        self.assertEqual(result, "5")
    
    def test_force_ternary(self):
        """Test ternary operator"""
        result = self.runtime._force_ternary(True, "yes", "no")
        self.assertEqual(result, "yes")
        
        result = self.runtime._force_ternary(False, "yes", "no")
        self.assertEqual(result, "no")


class TestForceInterpreter(unittest.TestCase):
    """Integration tests for the complete Force interpreter"""
    
    def setUp(self):
        self.interpreter = ForceInterpreter()
    
    def capture_output(self, func, *args, **kwargs):
        """Helper method to capture print output"""
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        try:
            result = func(*args, **kwargs)
            return result, captured_output.getvalue()
        finally:
            sys.stdout = old_stdout
    
    def test_simple_program(self):
        """Test a simple Force program"""
        force_code = '''
        ability main() {
            respond "Hello, Galaxy!"
        }
        main()
        '''
        result, output = self.capture_output(self.interpreter.run_force_code, force_code)
        self.assertIn("Hello, Galaxy!", output)
    
    def test_variable_program(self):
        """Test program with variables"""
        force_code = '''
        ability main() {
            holocron name = "Luke"
            respond "Hello, " + name
        }
        main()
        '''
        result, output = self.capture_output(self.interpreter.run_force_code, force_code)
        self.assertIn("Hello, Luke", output)
    
    def test_class_program(self):
        """Test program with class definition"""
        force_code = '''
        order Jedi {
            initiate(self, name) {
                self.name = name
            }
            ability greet(self) {
                respond "Hello, I am " + self.name
            }
        }
        ability main() {
            holocron luke = new Jedi("Luke")
            luke.greet()
        }
        main()
        '''
        result, output = self.capture_output(self.interpreter.run_force_code, force_code)
        self.assertIn("Hello, I am Luke", output)
    
    def test_loop_program(self):
        """Test program with loops"""
        force_code = '''
        ability main() {
            train (holocron i = 0; i < 3; i = i + 1) {
                respond "Count: " + str(i)
            }
        }
        main()
        '''
        result, output = self.capture_output(self.interpreter.run_force_code, force_code)
        self.assertIn("Count: 0", output)
        self.assertIn("Count: 1", output)
        self.assertIn("Count: 2", output)
    
    def test_array_program(self):
        """Test program with arrays"""
        force_code = '''
        ability main() {
            holocron items = squadron["apple", "banana", "cherry"]
            respond items[0]
            respond items[1]
        }
        main()
        '''
        result, output = self.capture_output(self.interpreter.run_force_code, force_code)
        self.assertIn("apple", output)
        self.assertIn("banana", output)
    
    def test_conditional_program(self):
        """Test program with conditionals"""
        force_code = '''
        ability main() {
            holocron x = 10
            sense (x > 5) {
                respond "x is greater than 5"
            } else {
                respond "x is not greater than 5"
            }
        }
        main()
        '''
        result, output = self.capture_output(self.interpreter.run_force_code, force_code)
        self.assertIn("x is greater than 5", output)


class TestAdvancedFeatures(unittest.TestCase):
    """Test cases for advanced Force language features"""
    
    def setUp(self):
        self.interpreter = ForceInterpreter()
    
    def capture_output(self, func, *args, **kwargs):
        """Helper method to capture print output"""
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        try:
            result = func(*args, **kwargs)
            return result, captured_output.getvalue()
        finally:
            sys.stdout = old_stdout
    
    def test_string_formatting(self):
        """Test string formatting features"""
        force_code = '''
        ability main() {
            holocron name = "Luke"
            respond hologram_text("Hello, {}", name)
        }
        main()
        '''
        result, output = self.capture_output(self.interpreter.run_force_code, force_code)
        self.assertIn("Hello, Luke", output)
    
    def test_mathematical_operations(self):
        """Test mathematical operations"""
        force_code = '''
        ability main() {
            respond force_calculate("add", 5, 3)
            respond force_calculate("multiply", 4, 2)
        }
        main()
        '''
        result, output = self.capture_output(self.interpreter.run_force_code, force_code)
        self.assertIn("8", output)  # 5 + 3
        self.assertIn("8", output)  # 4 * 2


if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestForceParser,
        TestForceRuntime,
        TestForceInterpreter,
        TestAdvancedFeatures
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Exit with error code if tests failed
    sys.exit(0 if result.wasSuccessful() else 1)