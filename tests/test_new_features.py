#!/usr/bin/env python3
"""
Tests for the new advanced features of The Force Programming Language
"""

import unittest
import sys
import os
import io

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from force_compiler import ForceInterpreter, ForceRuntime


class TestNewLanguageFeatures(unittest.TestCase):
    """Test cases for new language features"""
    
    def setUp(self):
        self.interpreter = ForceInterpreter()
        self.runtime = ForceRuntime()
    
    def capture_output(self, func, *args, **kwargs):
        """Helper method to capture print output"""
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        try:
            result = func(*args, **kwargs)
            return result, captured_output.getvalue()
        finally:
            sys.stdout = old_stdout
    
    def test_stack_operations(self):
        """Test stack data structure operations"""
        stack = self.runtime._force_stack([1, 2, 3])
        
        # Test basic operations
        self.assertEqual(stack.size(), 3)
        self.assertEqual(stack.peek(), 3)
        self.assertFalse(stack.is_empty())
        
        # Test push and pop
        stack.push(4)
        self.assertEqual(stack.size(), 4)
        self.assertEqual(stack.pop(), 4)
        self.assertEqual(stack.size(), 3)
    
    def test_queue_operations(self):
        """Test queue data structure operations"""
        queue = self.runtime._force_queue([1, 2, 3])
        
        # Test basic operations
        self.assertEqual(queue.size(), 3)
        self.assertEqual(queue.front(), 1)
        self.assertFalse(queue.is_empty())
        
        # Test enqueue and dequeue
        queue.enqueue(4)
        self.assertEqual(queue.size(), 4)
        self.assertEqual(queue.dequeue(), 1)
        self.assertEqual(queue.size(), 3)
        self.assertEqual(queue.front(), 2)
    
    def test_json_operations(self):
        """Test JSON processing operations"""
        data = {"name": "Luke", "rank": "Jedi"}
        
        # Test stringify
        json_str = self.runtime._force_json('stringify', data)
        self.assertIsInstance(json_str, str)
        self.assertIn('Luke', json_str)
        
        # Test parse
        parsed_data = self.runtime._force_json('parse', json_str)
        self.assertEqual(parsed_data['name'], 'Luke')
        self.assertEqual(parsed_data['rank'], 'Jedi')
    
    def test_switch_case(self):
        """Test switch-case functionality"""
        cases = {
            'jedi': 'Light Side',
            'sith': 'Dark Side',
            'gray': 'Balance'
        }
        
        result1 = self.runtime._force_switch('jedi', cases, 'Unknown')
        self.assertEqual(result1, 'Light Side')
        
        result2 = self.runtime._force_switch('unknown', cases, 'Unknown')
        self.assertEqual(result2, 'Unknown')
    
    def test_datetime_operations(self):
        """Test date/time operations"""
        # Test current time
        now = self.runtime._force_datetime('now')
        self.assertIsInstance(now, str)
        
        # Test timestamp
        timestamp = self.runtime._force_datetime('timestamp')
        self.assertIsInstance(timestamp, int)
    
    def test_encryption_operations(self):
        """Test encryption operations"""
        # Test base64 encoding
        encoded = self.runtime._force_encryption('base64_encode', 'Hello, Galaxy!')
        self.assertIsInstance(encoded, str)
        
        # Test base64 decoding
        decoded = self.runtime._force_encryption('base64_decode', encoded)
        self.assertEqual(decoded, 'Hello, Galaxy!')
        
        # Test simple cipher
        ciphered = self.runtime._force_encryption('simple_cipher', 'abc', 'key')
        self.assertNotEqual(ciphered, 'abc')
    
    def test_hash_functions(self):
        """Test hash functions"""
        text = "The Force is strong with this one"
        
        # Test different hash algorithms
        md5_hash = self.runtime._force_hash_func('md5', text)
        self.assertEqual(len(md5_hash), 32)
        
        sha256_hash = self.runtime._force_hash_func('sha256', text)
        self.assertEqual(len(sha256_hash), 64)
        
        # Test consistency
        md5_hash2 = self.runtime._force_hash_func('md5', text)
        self.assertEqual(md5_hash, md5_hash2)
    
    def test_regex_operations(self):
        """Test regular expression operations"""
        text = "The Force will be with you, always."
        
        # Test match
        result = self.runtime._force_regex('match', r'The', text)
        self.assertTrue(result)
        
        # Test search
        result = self.runtime._force_regex('search', r'Force', text)
        self.assertTrue(result)
        
        # Test findall
        result = self.runtime._force_regex('findall', r'\w+', text)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
    
    def test_advanced_program_with_new_features(self):
        """Test a program using multiple new features"""
        force_code = '''
        ability main() {
            // Test stack operations
            holocron my_stack = stack_tower([1, 2, 3])
            my_stack.push(4)
            respond "Stack size: " + str(my_stack.size())
            
            // Test JSON operations
            holocron data = datapad { name: "Luke", rank: "Jedi" }
            holocron json_str = data_stream("stringify", data)
            respond "JSON: " + json_str
            
            // Test encryption
            holocron message = "Secret Jedi message"
            holocron encoded = force_encrypt("base64_encode", message)
            respond "Encoded: " + encoded
        }
        main()
        '''
        
        result, output = self.capture_output(self.interpreter.run_force_code, force_code)
        self.assertIn("Stack size: 4", output)
        self.assertIn("JSON:", output)
        self.assertIn("Encoded:", output)


if __name__ == '__main__':
    unittest.main()