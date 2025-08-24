#!/usr/bin/env python3
"""
Quick Security and Code Quality Improvements for The Force Programming Language
This script demonstrates practical implementations of code review recommendations.
"""

import re
import time
from collections import defaultdict
from typing import Dict, List, Set


class ForceConfig:
    """Configuration constants for The Force Programming Language"""
    
    # Security settings
    MAX_CODE_SIZE = 10000  # 10KB limit
    MAX_EXECUTION_TIME = 5  # 5 seconds
    ENABLE_FILE_OPERATIONS = False  # Disable for security
    ENABLE_NETWORK_OPERATIONS = False  # Disable for security
    
    # Performance settings
    COMPILATION_CACHE_SIZE = 100
    
    # Allowed operations
    SAFE_BUILTINS = {
        'abs', 'bool', 'dict', 'float', 'int', 'len', 'list',
        'max', 'min', 'print', 'range', 'str', 'sum', 'tuple', 'zip'
    }
    
    # Forbidden patterns (for basic security)
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
    ]


class SecurityValidator:
    """Input validation and security checking for Force code"""
    
    def __init__(self, config=None):
        self.config = config or ForceConfig()
    
    def validate_force_code(self, code: str) -> bool:
        """
        Validate Force code for security and size limits
        
        Args:
            code: Force programming language source code
            
        Returns:
            True if code is safe to execute
            
        Raises:
            SecurityError: If code contains forbidden operations
            ValueError: If code exceeds size limits
        """
        # Size validation
        if len(code) > self.config.MAX_CODE_SIZE:
            raise ValueError(f"Code size ({len(code)} chars) exceeds limit ({self.config.MAX_CODE_SIZE})")
        
        # Pattern validation
        for pattern in self.config.FORBIDDEN_PATTERNS:
            if re.search(pattern, code, re.IGNORECASE):
                raise SecurityError(f"Forbidden pattern detected: {pattern}")
        
        # Check for excessive complexity (nested levels)
        brace_depth = 0
        max_depth = 0
        for char in code:
            if char == '{':
                brace_depth += 1
                max_depth = max(max_depth, brace_depth)
            elif char == '}':
                brace_depth -= 1
        
        if max_depth > 10:  # Reasonable nesting limit
            raise ValueError("Code complexity exceeds limit (too deeply nested)")
        
        return True
    
    def sanitize_output(self, output: str) -> str:
        """Sanitize output for safe display"""
        # Remove potential HTML/script tags
        output = re.sub(r'<[^>]*>', '', output)
        # Limit output size
        if len(output) > 5000:
            output = output[:5000] + "\n... (output truncated for safety)"
        return output


class RateLimiter:
    """Simple rate limiting for API endpoints"""
    
    def __init__(self, max_requests=60, window=60):
        self.requests = defaultdict(list)
        self.max_requests = max_requests
        self.window = window
        
    def is_allowed(self, client_ip: str) -> bool:
        """Check if client is within rate limits"""
        current_time = time.time()
        
        # Clean old requests outside window
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if current_time - req_time < self.window
        ]
        
        # Check if under limit
        if len(self.requests[client_ip]) >= self.max_requests:
            return False
        
        # Record this request
        self.requests[client_ip].append(current_time)
        return True
        
    def get_remaining_requests(self, client_ip: str) -> int:
        """Get remaining requests for client"""
        current_count = len(self.requests.get(client_ip, []))
        return max(0, self.max_requests - current_count)


class SecurityError(Exception):
    """Exception for security-related errors"""
    pass


class ForceSecurityEnhancer:
    """Enhanced security features for Force runtime"""
    
    def __init__(self):
        self.validator = SecurityValidator()
        self.rate_limiter = RateLimiter()
        
    def create_safe_globals(self, force_runtime_globals: dict) -> dict:
        """Create safe globals environment for code execution"""
        safe_globals = {
            '__builtins__': {
                name: getattr(__builtins__, name)
                for name in ForceConfig.SAFE_BUILTINS
                if hasattr(__builtins__, name)
            }
        }
        
        # Add only safe Force runtime functions
        safe_force_functions = {}
        for name, func in force_runtime_globals.items():
            if name.startswith('force_') and not name.endswith('_file'):
                # Exclude file operations for security
                if not any(dangerous in name for dangerous in ['file', 'system', 'import', 'exec']):
                    safe_force_functions[name] = func
        
        safe_globals.update(safe_force_functions)
        return safe_globals
    
    def secure_compile_and_run(self, force_code: str, interpreter) -> dict:
        """
        Securely compile and run Force code with safety checks
        
        Returns:
            dict: Result with success status, output, and any errors
        """
        try:
            # Security validation
            self.validator.validate_force_code(force_code)
            
            # Compile to Python
            python_code = interpreter.parser.translate_to_python(force_code)
            
            # Create safe execution environment
            safe_globals = self.create_safe_globals(interpreter.runtime.globals)
            
            # Execute with timeout (requires threading for production)
            import signal
            
            def timeout_handler(signum, frame):
                raise TimeoutError("Code execution timed out")
            
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(ForceConfig.MAX_EXECUTION_TIME)
            
            try:
                # Compile and execute safely
                compiled_code = compile(python_code, '<force_code>', 'exec')
                
                # Capture output
                from io import StringIO
                import contextlib
                
                output_buffer = StringIO()
                with contextlib.redirect_stdout(output_buffer):
                    exec(compiled_code, safe_globals, {})
                
                output = output_buffer.getvalue()
                sanitized_output = self.validator.sanitize_output(output)
                
                return {
                    'success': True,
                    'python_code': python_code,
                    'output': sanitized_output,
                    'security_checks': 'passed'
                }
                
            finally:
                signal.alarm(0)  # Cancel timeout
                
        except SecurityError as e:
            return {
                'success': False,
                'error': f"Security violation: {str(e)}",
                'error_type': 'security'
            }
        except TimeoutError:
            return {
                'success': False,
                'error': "Code execution timed out (dark side influence detected)",
                'error_type': 'timeout'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Execution error: {str(e)}",
                'error_type': 'runtime'
            }


class CodeQualityEnhancer:
    """Code quality improvements demonstration"""
    
    @staticmethod
    def optimize_regex_patterns(parser):
        """Pre-compile regex patterns for better performance"""
        compiled_patterns = []
        
        # Compile special patterns
        for pattern, replacement in parser.special_patterns:
            if isinstance(pattern, str):
                compiled_patterns.append((re.compile(pattern), replacement))
            else:
                compiled_patterns.append((pattern, replacement))
        
        # Compile keyword patterns
        compiled_keywords = []
        for pattern, replacement in parser.keyword_map.items():
            compiled_keywords.append((re.compile(pattern), replacement))
        
        return compiled_patterns, compiled_keywords
    
    @staticmethod
    def add_performance_monitoring():
        """Add basic performance monitoring"""
        import time
        import functools
        
        def monitor_performance(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                
                # Log slow operations
                if duration > 1.0:  # More than 1 second
                    print(f"Performance warning: {func.__name__} took {duration:.2f}s")
                
                return result
            return wrapper
        
        return monitor_performance


# Demonstration of security testing
def test_security_improvements():
    """Test security enhancements"""
    print("=== Security Enhancement Testing ===")
    
    enhancer = ForceSecurityEnhancer()
    
    # Test cases
    test_codes = [
        # Safe code
        ('respond "Hello Galaxy"', True),
        
        # Dangerous code  
        ('import os; respond os.getcwd()', False),
        ('transmission sys; respond sys.version', False),
        ('holocron data = holocron_archive("/etc/passwd")', False),
        
        # Size limit test
        ('respond "x" * 20000', False),  # Too large
    ]
    
    for code, should_pass in test_codes:
        try:
            enhancer.validator.validate_force_code(code)
            result = "PASS" if should_pass else "FAIL (should have been blocked)"
        except (SecurityError, ValueError):
            result = "BLOCKED" if not should_pass else "FAIL (should have passed)"
        
        print(f"Code: {code[:30]}... -> {result}")


def demonstrate_improvements():
    """Demonstrate the security and quality improvements"""
    print("=== The Force Programming Language - Security & Quality Demo ===\n")
    
    # Test security validator
    print("1. Testing Security Validator:")
    test_security_improvements()
    print()
    
    # Test rate limiter
    print("2. Testing Rate Limiter:")
    rate_limiter = RateLimiter(max_requests=3, window=10)
    
    for i in range(5):
        allowed = rate_limiter.is_allowed("127.0.0.1")
        remaining = rate_limiter.get_remaining_requests("127.0.0.1")
        print(f"Request {i+1}: {'Allowed' if allowed else 'Blocked'}, Remaining: {remaining}")
    print()
    
    # Show configuration
    print("3. Security Configuration:")
    config = ForceConfig()
    print(f"Max code size: {config.MAX_CODE_SIZE} characters")
    print(f"Max execution time: {config.MAX_EXECUTION_TIME} seconds")
    print(f"File operations enabled: {config.ENABLE_FILE_OPERATIONS}")
    print(f"Network operations enabled: {config.ENABLE_NETWORK_OPERATIONS}")
    print(f"Safe builtins: {len(config.SAFE_BUILTINS)} functions")
    print()
    
    print("4. Recommendations Summary:")
    print("✅ Input validation implemented")
    print("✅ Rate limiting implemented")  
    print("✅ Configuration system created")
    print("⚠️  Sandboxed execution needs integration")
    print("⚠️  File path validation needs integration")
    print("⚠️  Comprehensive security testing needed")
    print()
    print("🎯 Next steps: Integrate these improvements into the main codebase")


if __name__ == "__main__":
    demonstrate_improvements()