#!/usr/bin/env python3
"""
Web server for The Force Programming Language
Provides HTTP API to compile and execute Force code
"""

import json
import traceback
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import sys
import os

# Import the Force compiler
from force_compiler import ForceInterpreter

class ForceWebHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.interpreter = ForceInterpreter()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Serve static files or API endpoints"""
        if self.path == '/' or self.path == '/index.html':
            self.serve_file('force_web_ui.html', 'text/html')
        elif self.path == '/style.css':
            self.serve_file('force_web_ui.css', 'text/css')
        elif self.path == '/script.js':
            self.serve_file('force_web_ui.js', 'application/javascript')
        elif self.path == '/examples':
            self.serve_examples()
        else:
            self.send_error(404)
    
    def do_POST(self):
        """Handle API requests"""
        if self.path == '/api/compile':
            self.handle_compile()
        elif self.path == '/api/run':
            self.handle_run()
        else:
            self.send_error(404)
    
    def serve_file(self, filename, content_type):
        """Serve a static file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.send_header('Content-Length', len(content.encode('utf-8')))
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            self.send_error(404)
    
    def serve_examples(self):
        """Serve example Force code"""
        examples = {
            'hello_galaxy': {
                'name': 'Hello Galaxy',
                'description': 'A simple greeting from a galaxy far, far away',
                'code': '''// A simple greeting from a galaxy far, far away
ability main() {
    respond "Hello, Galaxy!"
    respond "May the Force be with you"
}

main()'''
            },
            'jedi_training': {
                'name': 'Jedi Training',
                'description': 'Training simulation for young Padawans with classes and loops',
                'code': '''// Training simulation for young Padawans
order Jedi {
    initiate(self, name) {
        self.name = name
        self.power = 10
        self.level = "Padawan"
    }
    
    ability train(self) {
        self.power = self.power + 5
        respond self.name + " trains hard. Power: " + str(self.power)
    }
    
    ability promote(self) {
        sense (self.power >= 50) {
            self.level = "Jedi Knight"
            respond self.name + " has become a Jedi Knight!"
        } else {
            respond "More training required, young Padawan"
        }
    }
}

ability main() {
    holocron rey = new Jedi("Rey")
    
    train (holocron i = 0; i < 10; i = i + 1) {
        rey.train()
    }
    
    rey.promote()
}

main()'''
            },
            'squadron_mission': {
                'name': 'Squadron Mission',
                'description': 'Rebel Alliance mission planning with arrays and dictionaries',
                'code': '''// Rebel Alliance mission planning
ability main() {
    respond "Rebel Alliance Mission Briefing"
    
    // Create squadron roster
    holocron pilots = squadron["Luke", "Wedge", "Biggs", "Porkins"]
    holocron ships = squadron["Red 5", "Red 2", "Red 3", "Red 6"]
    
    respond "Squadron roster:"
    train (holocron i = 0; i < len(pilots); i = i + 1) {
        respond pilots[i] + " flying " + ships[i]
    }
    
    respond "Mission: Death Star assault"
    respond "Status: Ready for launch"
    respond "May the Force be with them all"
}

main()'''
            },
            'data_structures': {
                'name': 'Advanced Data Structures',
                'description': 'Demonstration of stacks, queues, and other data structures',
                'code': '''// Advanced data structures demonstration
ability main() {
    respond "=== Advanced Data Structures Demo ==="
    
    // Stack example - Jedi Council members
    respond "Stack Operations (Last In, First Out):"
    holocron council_stack = stack_tower(squadron["Yoda", "Mace Windu", "Obi-Wan"])
    council_stack.push("Ki-Adi-Mundi")
    respond "Stack size: " + str(council_stack.size())
    respond "Top member: " + council_stack.peek()
    respond "Removing: " + council_stack.pop()
    respond "New top: " + council_stack.peek()
    
    // Queue example - Cantina service
    respond ""
    respond "Queue Operations (First In, First Out):"
    holocron cantina_queue = queue_line(squadron["Han", "Leia", "Chewbacca"])
    cantina_queue.enqueue("Lando")
    respond "Queue size: " + str(cantina_queue.size())
    respond "Next customer: " + cantina_queue.front()
    respond "Serving: " + cantina_queue.dequeue()
    respond "New next: " + cantina_queue.front()
}

main()'''
            },
            'text_processing': {
                'name': 'Text & String Processing',
                'description': 'Advanced text processing with regex and string manipulation',
                'code': '''// Text and string processing demo
ability main() {
    respond "=== Text Processing Demo ==="
    
    holocron jedi_quote = "Do or do not, there is no try"
    
    // Basic text operations
    respond "Original: " + jedi_quote
    respond "Uppercase: " + protocol_droid("uppercase", jedi_quote)
    respond "Reversed: " + protocol_droid("reverse", jedi_quote)
    respond "Length: " + protocol_droid("length", jedi_quote)
    
    // String formatting
    holocron padawan_name = "Ahsoka Tano"
    respond hologram_text("Welcome, {}! Ready for training?", padawan_name)
    
    // Regular expressions
    holocron force_wisdom = "Fear leads to anger, anger leads to hate"
    respond "Contains 'anger': " + str(regex_pattern("search", "anger", force_wisdom))
    holocron words = regex_pattern("findall", "\\w+", force_wisdom)
    respond "Word count: " + str(len(words))
}

main()'''
            },
            'security_demo': {
                'name': 'Security & Encryption',
                'description': 'Demonstrate encryption, hashing, and security functions',
                'code': '''// Security and encryption demonstration
ability main() {
    respond "=== Security Operations Demo ==="
    
    holocron secret_message = "The Death Star plans are hidden here"
    respond "Secret message: " + secret_message
    
    // Base64 encoding/decoding
    holocron encoded = force_encrypt("base64_encode", secret_message)
    respond "Encoded: " + encoded
    
    holocron decoded = force_encrypt("base64_decode", encoded)
    respond "Decoded: " + decoded
    
    // Hash functions for integrity
    holocron message_hash = force_hash("sha256", secret_message)
    respond "SHA256 hash: " + message_hash
    
    respond "Security demo complete!"
}

main()'''
            },
            'datetime_operations': {
                'name': 'Date & Time Operations',
                'description': 'Working with galactic time and timestamps',
                'code': '''// Date and time operations
ability main() {
    respond "=== Galactic Time Operations ==="
    
    // Current time operations
    holocron current_time = galactic_time("now")
    respond "Current galactic time: " + current_time
    
    holocron timestamp = galactic_time("timestamp")
    respond "Current timestamp: " + str(timestamp)
    
    respond "Time operations complete!"
}

main()'''
            }
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = json.dumps(examples)
        self.wfile.write(response.encode('utf-8'))
    
    def handle_compile(self):
        """Compile Force code to Python"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(post_data)
            
            force_code = data.get('code', '')
            
            # Use the interpreter to translate the code
            python_code = self.interpreter.parser.translate_to_python(force_code)
            
            response = {
                'success': True,
                'python_code': python_code
            }
            
        except Exception as e:
            response = {
                'success': False,
                'error': f"Compilation error: {str(e)}",
                'traceback': traceback.format_exc()
            }
        
        self.send_json_response(response)
    
    def handle_run(self):
        """Compile and run Force code"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(post_data)
            
            force_code = data.get('code', '')
            
            # Capture stdout to return execution output
            from io import StringIO
            import contextlib
            
            old_stdout = sys.stdout
            output_buffer = StringIO()
            
            try:
                with contextlib.redirect_stdout(output_buffer):
                    result = self.interpreter.run_force_code(force_code)
                
                output = output_buffer.getvalue()
                python_code = self.interpreter.parser.translate_to_python(force_code)
                
                response = {
                    'success': True,
                    'python_code': python_code,
                    'output': output,
                    'result': str(result) if result is not None else None
                }
                
            finally:
                sys.stdout = old_stdout
                
        except Exception as e:
            response = {
                'success': False,
                'error': f"Execution error: {str(e)}",
                'traceback': traceback.format_exc()
            }
        
        self.send_json_response(response)
    
    def send_json_response(self, data):
        """Send JSON response with CORS headers"""
        response = json.dumps(data, indent=2)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        self.wfile.write(response.encode('utf-8'))
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def main():
    """Start the Force web server"""
    port = int(os.environ.get('PORT', 8000))
    
    print(f"Starting The Force Programming Language Web Server on port {port}")
    print(f"Open http://localhost:{port} in your browser to explore The Force!")
    print("Use Ctrl+C to stop the server")
    
    server = HTTPServer(('localhost', port), ForceWebHandler)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nMay the Force be with you. Server shutting down...")
        server.server_close()

if __name__ == '__main__':
    main()