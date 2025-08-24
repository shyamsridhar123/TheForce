#!/usr/bin/env python3
"""
Example Security Fix Implementation for The Force Programming Language
This demonstrates how to implement the critical security recommendations.
"""

import re
import json
import traceback
from collections import defaultdict
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import sys
import os

# Import the Force compiler (would need to be patched)
from force_compiler import ForceInterpreter


class SecurityError(Exception):
    """Security-related exception"""
    pass


class ForceSecurityConfig:
    """Security configuration for The Force Programming Language"""
    
    # Input limits
    MAX_CODE_SIZE = 10000  # 10KB
    MAX_EXECUTION_TIME = 5  # 5 seconds
    
    # Rate limiting
    MAX_REQUESTS_PER_MINUTE = 60
    MAX_REQUESTS_PER_HOUR = 1000
    
    # Safe builtins (restricted Python environment)
    SAFE_BUILTINS = {
        'abs': abs, 'bool': bool, 'dict': dict, 'float': float,
        'int': int, 'len': len, 'list': list, 'max': max, 'min': min,
        'print': print, 'range': range, 'str': str, 'sum': sum, 
        'tuple': tuple, 'zip': zip, 'round': round, 'sorted': sorted,
        'enumerate': enumerate
    }
    
    # Forbidden patterns in Force code
    FORBIDDEN_PATTERNS = [
        r'import\s+os',
        r'import\s+sys', 
        r'import\s+subprocess',
        r'__import__',
        r'exec\s*\(',
        r'eval\s*\(',
        r'compile\s*\(',
        r'open\s*\(',
        r'file\s*\(',
        r'input\s*\(',  # Disable input for web security
    ]


class RateLimiter:
    """Rate limiting implementation"""
    
    def __init__(self, config=None):
        self.config = config or ForceSecurityConfig()
        self.requests = defaultdict(list)
        
    def is_allowed(self, client_ip: str) -> bool:
        """Check if request is within rate limits"""
        current_time = time.time()
        
        # Clean old requests (older than 1 hour)
        cutoff_time = current_time - 3600  # 1 hour
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if req_time > cutoff_time
        ]
        
        # Check minute limit
        minute_cutoff = current_time - 60
        recent_requests = [
            req_time for req_time in self.requests[client_ip]
            if req_time > minute_cutoff
        ]
        
        if len(recent_requests) >= self.config.MAX_REQUESTS_PER_MINUTE:
            return False
            
        # Check hour limit
        if len(self.requests[client_ip]) >= self.config.MAX_REQUESTS_PER_HOUR:
            return False
        
        # Record this request
        self.requests[client_ip].append(current_time)
        return True


class InputValidator:
    """Input validation for Force code"""
    
    def __init__(self, config=None):
        self.config = config or ForceSecurityConfig()
        
    def validate_force_code(self, code: str) -> bool:
        """
        Validate Force code for security and safety
        
        Args:
            code: Force programming language source code
            
        Returns:
            True if code is safe
            
        Raises:
            SecurityError: If code contains dangerous patterns
            ValueError: If code violates size/complexity limits
        """
        # Basic size check
        if len(code) > self.config.MAX_CODE_SIZE:
            raise ValueError(f"Code size ({len(code)} characters) exceeds limit ({self.config.MAX_CODE_SIZE})")
        
        # Check for forbidden patterns
        for pattern in self.config.FORBIDDEN_PATTERNS:
            if re.search(pattern, code, re.IGNORECASE):
                raise SecurityError(f"Forbidden operation detected: {pattern}")
        
        # Check for excessive complexity
        brace_depth = 0
        max_depth = 0
        for char in code:
            if char == '{':
                brace_depth += 1
                max_depth = max(max_depth, brace_depth)
            elif char == '}':
                brace_depth -= 1
        
        if max_depth > 15:  # Reasonable nesting limit
            raise ValueError("Code complexity exceeds safety limits (too deeply nested)")
        
        # Check for suspicious patterns
        suspicious_patterns = [
            r'[\w\s]*\*\s*\d{4,}',  # Large multiplication (potential DoS)
            r'while\s+True\s*:',    # Infinite loops (after translation)
            r'\[\s*\d+\s*\]\s*\*\s*\d{3,}',  # Large list creation
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, code):
                raise SecurityError(f"Suspicious pattern detected: {pattern}")
        
        return True


class SecureForceInterpreter:
    """Security-enhanced Force interpreter"""
    
    def __init__(self):
        self.interpreter = ForceInterpreter()
        self.validator = InputValidator()
        self.config = ForceSecurityConfig()
        
    def create_safe_environment(self) -> dict:
        """Create a restricted execution environment"""
        # Start with safe builtins only
        safe_globals = {
            '__builtins__': self.config.SAFE_BUILTINS.copy()
        }
        
        # Add only safe Force runtime functions
        for name, func in self.interpreter.runtime.globals.items():
            if name.startswith('force_'):
                # Exclude dangerous functions
                if not any(danger in name for danger in ['file', 'read', 'write', 'http', 'system']):
                    safe_globals[name] = func
        
        return safe_globals
    
    def secure_compile(self, force_code: str) -> dict:
        """Securely compile Force code with validation"""
        try:
            # Validate input
            self.validator.validate_force_code(force_code)
            
            # Compile to Python
            python_code = self.interpreter.parser.translate_to_python(force_code)
            
            return {
                'success': True,
                'python_code': python_code,
                'security_status': 'validated'
            }
            
        except (SecurityError, ValueError) as e:
            return {
                'success': False,
                'error': str(e),
                'error_type': 'security'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Compilation error: {str(e)}",
                'error_type': 'compilation'
            }
    
    def secure_execute(self, python_code: str) -> dict:
        """Securely execute Python code with restrictions"""
        try:
            # Create safe execution environment
            safe_globals = self.create_safe_environment()
            
            # Set up timeout (simplified version - production needs threading)
            import signal
            
            def timeout_handler(signum, frame):
                raise TimeoutError("Execution timeout - The dark side has consumed too much time!")
                
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(self.config.MAX_EXECUTION_TIME)
            
            try:
                # Capture output safely
                from io import StringIO
                import contextlib
                
                output_buffer = StringIO()
                
                with contextlib.redirect_stdout(output_buffer):
                    # Compile and execute in restricted environment
                    compiled_code = compile(python_code, '<force_code>', 'exec')
                    exec(compiled_code, safe_globals, {})
                
                output = output_buffer.getvalue()
                
                # Sanitize output
                if len(output) > 5000:  # Limit output size
                    output = output[:5000] + "\n... (output truncated for safety)"
                
                return {
                    'success': True,
                    'output': output,
                    'security_status': 'executed_safely'
                }
                
            finally:
                signal.alarm(0)  # Cancel timeout
                
        except TimeoutError as e:
            return {
                'success': False,
                'error': str(e),
                'error_type': 'timeout'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Execution error: {str(e)}",
                'error_type': 'runtime'
            }


class SecureForceWebHandler(BaseHTTPRequestHandler):
    """Security-enhanced web handler"""
    
    def __init__(self, *args, **kwargs):
        self.secure_interpreter = SecureForceInterpreter()
        self.rate_limiter = RateLimiter()
        super().__init__(*args, **kwargs)
    
    def do_POST(self):
        """Handle API requests with security checks"""
        # Rate limiting
        client_ip = self.client_address[0]
        if not self.rate_limiter.is_allowed(client_ip):
            self.send_error(429, "Too Many Requests - The Force needs rest")
            return
        
        if self.path == '/api/compile':
            self.handle_secure_compile()
        elif self.path == '/api/run':
            self.handle_secure_run()
        else:
            self.send_error(404)
    
    def handle_secure_compile(self):
        """Securely handle compilation requests"""
        try:
            # Read and validate request
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 50000:  # 50KB limit
                self.send_error(413, "Request too large")
                return
                
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(post_data)
            
            force_code = data.get('code', '')
            
            # Secure compilation
            result = self.secure_interpreter.secure_compile(force_code)
            
            self.send_json_response(result)
            
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
        except Exception as e:
            error_response = {
                'success': False,
                'error': f"Server error: {str(e)}",
                'error_type': 'server'
            }
            self.send_json_response(error_response)
    
    def handle_secure_run(self):
        """Securely handle execution requests"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 50000:
                self.send_error(413, "Request too large")
                return
                
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(post_data)
            
            force_code = data.get('code', '')
            
            # Secure compilation and execution
            compile_result = self.secure_interpreter.secure_compile(force_code)
            
            if not compile_result['success']:
                self.send_json_response(compile_result)
                return
            
            # Execute if compilation succeeded
            python_code = compile_result['python_code']
            execution_result = self.secure_interpreter.secure_execute(python_code)
            
            # Combine results
            combined_result = {
                **compile_result,
                **execution_result
            }
            
            self.send_json_response(combined_result)
            
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
        except Exception as e:
            error_response = {
                'success': False,
                'error': f"Server error: {str(e)}",
                'error_type': 'server'
            }
            self.send_json_response(error_response)
    
    def send_json_response(self, data):
        """Send JSON response with security headers"""
        response = json.dumps(data, indent=2)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        
        # Security headers
        self.send_header('Access-Control-Allow-Origin', 'http://localhost:8000')  # Specific origin
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'DENY')
        self.send_header('X-XSS-Protection', '1; mode=block')
        
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))
    
    def log_message(self, format, *args):
        """Custom logging with security context"""
        client_ip = self.client_address[0]
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        message = format % args
        print(f"[{timestamp}] {client_ip} - {message}")


def run_secure_server(port=8000):
    """Run the secure web server"""
    print(f"🛡️  Starting secure Force web server on port {port}")
    print("Security features enabled:")
    print("  ✅ Input validation")
    print("  ✅ Rate limiting") 
    print("  ✅ Restricted code execution")
    print("  ✅ Security headers")
    print("  ✅ Request size limits")
    print()
    
    server = HTTPServer(('localhost', port), SecureForceWebHandler)
    
    try:
        print(f"🌟 The Force (Secure Edition) is serving at http://localhost:{port}")
        print("May the Force be with you... securely! ⚡🛡️")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        server.server_close()


if __name__ == "__main__":
    # Demonstration mode
    print("=== The Force Programming Language - Security Enhancement Demo ===")
    print()
    
    # Test security validator
    print("🔍 Testing Security Validator:")
    validator = InputValidator()
    
    test_cases = [
        ("respond 'Hello Galaxy'", "✅ Safe code"),
        ("import os; respond os.getcwd()", "🚫 Dangerous import"),
        ("respond 'x' * 50000", "🚫 Large output"),
        ("ability evil() { meditate True { respond 'infinite' } }", "🚫 Potential infinite loop"),
    ]
    
    for code, description in test_cases:
        try:
            validator.validate_force_code(code)
            status = "ALLOWED"
        except (SecurityError, ValueError) as e:
            status = f"BLOCKED: {e}"
        
        print(f"  {description}: {status}")
    
    print()
    
    # Test rate limiter
    print("🚦 Testing Rate Limiter:")
    rate_limiter = RateLimiter()
    
    for i in range(5):
        allowed = rate_limiter.is_allowed("127.0.0.1")
        print(f"  Request {i+1}: {'✅ Allowed' if allowed else '🚫 Rate limited'}")
    
    print()
    
    # Test secure interpreter
    print("🔒 Testing Secure Interpreter:")
    secure_interp = SecureForceInterpreter()
    
    test_code = '''
    ability main() {
        respond "Hello from secure Force!"
        holocron data = datapad { greeting: "May the Force be with you" }
        respond data["greeting"]
    }
    main()
    '''
    
    compile_result = secure_interp.secure_compile(test_code)
    if compile_result['success']:
        print("  ✅ Compilation: SUCCESS")
        
        exec_result = secure_interp.secure_execute(compile_result['python_code'])
        if exec_result['success']:
            print("  ✅ Execution: SUCCESS")
            print(f"  📤 Output: {exec_result['output'].strip()}")
        else:
            print(f"  ❌ Execution: {exec_result['error']}")
    else:
        print(f"  ❌ Compilation: {compile_result['error']}")
    
    print()
    print("🎯 Security enhancements ready for integration!")
    print("Next steps:")
    print("  1. Replace ForceWebHandler with SecureForceWebHandler")
    print("  2. Add security configuration to main application") 
    print("  3. Add security tests to test suite")
    print("  4. Update documentation with security practices")
    print()
    print("⚠️  Note: This is a demonstration. Full integration requires")
    print("   careful testing and gradual rollout.")