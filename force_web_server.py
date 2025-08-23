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
                'code': '''// A simple greeting from a galaxy far, far away
ability main() {
    respond "Hello, Galaxy!"
    respond "May the Force be with you"
}

main()'''
            },
            'jedi_training': {
                'name': 'Jedi Training',
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
    
    // Mission data
    holocron mission = datapad {
        target: "Death Star",
        status: "In Progress",
        survivors: 1
    }
    
    respond "Mission: " + mission["target"]
    respond "Status: " + mission["status"]
    respond "May the Force be with them all"
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