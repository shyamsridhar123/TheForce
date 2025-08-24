#!/usr/bin/env python3
"""
Test suite for The Force Programming Language web server
"""

import unittest
import json
import sys
import os
import threading
import time
import requests
from http.server import HTTPServer

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from force_web_server import ForceWebHandler


class TestForceWebServer(unittest.TestCase):
    """Test cases for the Force web server"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test server"""
        cls.port = 8888  # Use different port for testing
        cls.server = HTTPServer(('localhost', cls.port), ForceWebHandler)
        
        # Start server in a separate thread
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        
        # Give server time to start
        time.sleep(0.5)
        
        cls.base_url = f'http://localhost:{cls.port}'
    
    @classmethod
    def tearDownClass(cls):
        """Shut down test server"""
        cls.server.shutdown()
        cls.server.server_close()
    
    def test_serve_index_html(self):
        """Test serving the main HTML page"""
        response = requests.get(f'{self.base_url}/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/html', response.headers.get('content-type', ''))
        self.assertIn('The Force Programming Language', response.text)
    
    def test_serve_css(self):
        """Test serving CSS files"""
        response = requests.get(f'{self.base_url}/style.css')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/css', response.headers.get('content-type', ''))
    
    def test_serve_javascript(self):
        """Test serving JavaScript files"""
        response = requests.get(f'{self.base_url}/script.js')
        self.assertEqual(response.status_code, 200)
        self.assertIn('javascript', response.headers.get('content-type', ''))
    
    def test_serve_examples(self):
        """Test serving examples endpoint"""
        response = requests.get(f'{self.base_url}/examples')
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response.headers.get('content-type', ''))
        
        examples = response.json()
        self.assertIsInstance(examples, dict)
        self.assertIn('hello_galaxy', examples)
        self.assertIn('jedi_training', examples)
        self.assertIn('squadron_mission', examples)
    
    def test_compile_endpoint(self):
        """Test the compile API endpoint"""
        test_code = '''
        ability main() {
            respond "Hello, Galaxy!"
        }
        main()
        '''
        
        payload = {'code': test_code}
        response = requests.post(
            f'{self.base_url}/api/compile',
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertTrue(result['success'])
        self.assertIn('python_code', result)
        self.assertIn('def main():', result['python_code'])
        self.assertIn('print("Hello, Galaxy!")', result['python_code'])
    
    def test_run_endpoint(self):
        """Test the run API endpoint"""
        test_code = '''
        ability main() {
            respond "Hello, Galaxy!"
        }
        main()
        '''
        
        payload = {'code': test_code}
        response = requests.post(
            f'{self.base_url}/api/run',
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertTrue(result['success'])
        self.assertIn('output', result)
        self.assertIn('Hello, Galaxy!', result['output'])
    
    def test_compile_error_handling(self):
        """Test error handling in compile endpoint"""
        # Invalid Force code that should cause errors
        test_code = '''
        invalid_syntax_here
        '''
        
        payload = {'code': test_code}
        response = requests.post(
            f'{self.base_url}/api/compile',
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        # The compiler might still succeed with invalid syntax, 
        # but we should get some result
        self.assertIn('success', result)
    
    def test_run_error_handling(self):
        """Test error handling in run endpoint"""
        # Force code that compiles but fails at runtime
        test_code = '''
        ability main() {
            respond undefined_variable
        }
        main()
        '''
        
        payload = {'code': test_code}
        response = requests.post(
            f'{self.base_url}/api/run',
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        # Should handle runtime errors gracefully
        self.assertIn('success', result)
    
    def test_cors_headers(self):
        """Test CORS headers are present"""
        response = requests.get(f'{self.base_url}/examples')
        self.assertIn('access-control-allow-origin', 
                     [h.lower() for h in response.headers.keys()])
        self.assertEqual(response.headers.get('access-control-allow-origin'), '*')
    
    def test_404_handling(self):
        """Test 404 error handling"""
        response = requests.get(f'{self.base_url}/nonexistent')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()