#!/usr/bin/env python3
"""
The Force Programming Language Compiler/Interpreter
A Python-based implementation that translates Force code to Python and executes it.
"""

import re
import sys
import ast
import traceback
import random
import math
import os
from typing import Dict, List, Tuple, Any, Optional

class ForceParser:
    """Parser for The Force Programming Language"""
    
    def __init__(self):
        # Define keyword mappings from Force to Python
        self.keyword_map = {
            r'\bholocron\b': 'force_var',        # Variables
            r'\bkyber\b': 'force_const',         # Constants
            r'\bsense\b': 'if',                  # If statements
            r'\bmeditate\b': 'while',            # While loops
            # 'train' loops are handled separately below
            r'\bability\b': 'def',              # Function definitions
            r'\brespond\b': 'print',             # Output
            r'\bsense_input\b': 'input',         # Input
            r'\bsquadron\b': 'list',             # Arrays
            r'\bdatapad\b': 'dict',              # Objects
            r'\border\b': 'class',               # Classes
            r'\binitiate\b': '__init__',         # Constructor
            r'\btry_use_force\b': 'try',         # Try block
            r'\bcatch_disturbance\b': 'except',  # Except block
            r'\bfinally_balance\b': 'finally',   # Finally block
            r'\bforce_projection\b': 'async def',# Async def
            r'\bawait\b': 'await',               # Await keyword
            r'\btransmission\b': 'import',       # Import
            r'\bfrom\b': 'from',                 # From for imports
            
            # Mathematical operations
            r'\bforce_calculate\b': 'force_calculate',  # Mathematical calculations
            r'\bmidichlorians\b': 'force_random',       # Random number generation
            r'\blightsaber_distance\b': 'force_distance', # Distance calculation
            
            # Advanced data structures
            r'\brebellion\b': 'set',             # Sets
            r'\bhyperdrive\b': 'force_generator', # Generators
            r'\btuple_coordinates\b': 'tuple',    # Tuples
            r'\bstack_tower\b': 'force_stack',    # Stack data structure
            r'\bqueue_line\b': 'force_queue',     # Queue data structure
            
            # String manipulation
            r'\bhologram_text\b': 'force_format', # String formatting
            r'\bprotocol_droid\b': 'force_text',  # Text processing
            r'\bregex_pattern\b': 'force_regex',  # Regular expressions
            
            # File operations
            r'\bholocron_archive\b': 'force_read_file',  # File reading
            r'\bimperial_database\b': 'force_write_file', # File writing
            r'\bdata_stream\b': 'force_json',     # JSON processing
            
            # Control flow enhancements
            r'\bjedi_mind_trick\b': 'force_ternary',  # Ternary operator
            r'\bjedi_council\b': 'force_switch',      # Switch-case equivalent
            r'\bforce_lightning\b': 'lambda',         # Lambda functions
            
            # Date/Time operations
            r'\bgalactic_time\b': 'force_datetime', # Date/time operations
            
            # Network operations
            r'\bhyperspace_comm\b': 'force_http',   # HTTP requests
            
            # Encryption/Security
            r'\bforce_encrypt\b': 'force_encryption', # Encryption functions
            r'\bforce_hash\b': 'force_hash_func',     # Hash functions
        }
        
        # Special patterns that need custom handling
        self.special_patterns = [            
            # Handle new keyword for classes
            (r'new (\w+)\(', r'\1('),
            
            # Handle array literal: squadron["a", "b"] -> ["a", "b"]
            (r'squadron\[(.*?)\]', r'[\1]'),
            
            # Handle dictionary literal: datapad { a: 1, b: 2 } -> {"a": 1, "b": 2}
            (r'datapad\s*{([^{}]*(?:{[^{}]*}[^{}]*)*)}', self._handle_datapad),
            
            # Handle set literal: rebellion["a", "b"] -> {"a", "b"} - must come before generic array access
            (r'rebellion\s*\[(.*?)\]', r'{\1}'),
            
            # Handle ternary operator: jedi_mind_trick(condition, true_value, false_value)
            (r'jedi_mind_trick\s*\(\s*([^,]+),\s*([^,]+),\s*([^)]+)\)', r'(\2 if \1 else \3)'),
            
            # Handle string formatting: hologram_text("Hello {}", name) -> f"Hello {name}"
            (r'hologram_text\s*\(\s*(["\'][^"\']*["\'])\s*,\s*([^)]+)\)', self._handle_format),
            
            # Handle mathematical calculations: force_calculate(operation, args...)
            (r'force_calculate\s*\(\s*([^,]+),\s*([^)]+)\)', self._handle_calculate),
            
            # Handle array access: rebels[0] -> rebels[0] - must come AFTER specific patterns
            (r'(\w+)\[([^\]]+)\]', r'\1[\2]'),
        ]
        
        # Variables and constants tracking
        self.variables = set()
        self.constants = set()
        
    def _handle_datapad(self, match) -> str:
        """Convert datapad object syntax to Python dictionary"""
        content = match.group(1).strip()
        
        # If content has line breaks, handle multiline dictionary
        if '\n' in content:
            lines = content.split('\n')
            result_lines = []
            for line in lines:
                line = line.strip()
                if line and not line.endswith(','):
                    # Handle property: value syntax
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip().rstrip(',')
                        # Add quotes around key if not already quoted
                        if not (key.startswith('"') and key.endswith('"')) and not (key.startswith("'") and key.endswith("'")):
                            key = f'"{key}"'
                        result_lines.append(f'{key}: {value}')
                    else:
                        result_lines.append(line)
                else:
                    result_lines.append(line)
            content = ',\n    '.join(result_lines)
            return '{\n    ' + content + '\n}'
        else:
            # Single line - just replace property names with quoted strings and keep on one line
            content = re.sub(r'(\w+):', r'"\1":', content)
            return '{' + content + '}'
    
    def _handle_format(self, match) -> str:
        """Convert hologram_text string formatting to Python f-string"""
        format_str = match.group(1).strip('"\'')
        args = match.group(2).strip()
        
        # For simple single argument, create f-string
        if ',' not in args:
            formatted = format_str.replace('{}', '{' + args + '}')
            return f'f"{formatted}"'
        else:
            # For multiple arguments, use .format() method
            return f'{match.group(1)}.format({args})'
    
    def _handle_calculate(self, match) -> str:
        """Convert force_calculate to appropriate Python math operation"""
        operation = match.group(1).strip().strip('"\'')
        args = match.group(2).strip()
        
        # Map common operations
        op_map = {
            'add': '+',
            'subtract': '-', 
            'multiply': '*',
            'divide': '/',
            'power': '**',
            'modulo': '%'
        }
        
        if operation in op_map:
            # Split arguments and join with operator
            arg_list = [arg.strip() for arg in args.split(',')]
            if len(arg_list) == 2:
                return f'({arg_list[0]} {op_map[operation]} {arg_list[1]})'
        
        # Fallback to function call for complex operations
        return f'force_math_{operation}({args})'
    
    def preprocess(self, code: str) -> str:
        """Initial preprocessing of code before main translation"""
        # Remove Force-style comments
        code = re.sub(r'//.*$', '', code, flags=re.MULTILINE)
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        return code
    
    def translate_to_python(self, force_code: str) -> str:
        """Translate Force code to Python code"""
        # Preprocess the code
        code = self.preprocess(force_code)
        
        # Handle C-style for loops BEFORE applying keyword mappings to avoid 'def' insertion
        # Handle simple numeric range loops: train (holocron i = 0; i < 10; i = i + 1) {
        code = re.sub(
            r'train\s*\(\s*holocron\s+(\w+)\s*=\s*(\d+)\s*;\s*\1\s*<\s*(\d+)\s*;\s*\1\s*=\s*\1\s*\+\s*(\d+)\s*\)\s*\{',
            r'for \1 in range(\2, \3, \4):',
            code
        )
        
        # Handle loops with len() function: train (holocron i = 0; i < len(missions); i = i + 1) {
        code = re.sub(
            r'train\s*\(\s*holocron\s+(\w+)\s*=\s*(\d+)\s*;\s*\1\s*<\s*len\(([^)]+)\)\s*;\s*\1\s*=\s*\1\s*\+\s*(\d+)\s*\)\s*\{',
            r'for \1 in range(\2, len(\3), \4):',
            code
        )
        
        # Apply special patterns first (before keyword mappings to handle complex syntax)
        for pattern, replacement in self.special_patterns:
            if callable(replacement):
                # If the replacement is a function, use re.sub with the function
                code = re.sub(pattern, replacement, code)
            else:
                # Otherwise, use regular re.sub
                code = re.sub(pattern, replacement, code)
        
        # Apply keyword mappings (excluding 'train' since it's already handled)
        for pattern, replacement in self.keyword_map.items():
            if 'train' not in pattern:  # Skip train pattern as it's handled above
                code = re.sub(pattern, replacement, code)
        
        # Fix class methods by adding 'def' keyword if missing (but not to for loops or function calls)
        # Only apply to lines that look like method definitions within classes
        code = re.sub(r'(\s+)(__init__\s*\([^)]*\))', r'\1def \2', code)
        # More careful method detection - only add def if it looks like a method definition
        code = re.sub(r'^(\s+)(\w+\s*\([^)]*\))\s*:$', r'\1def \2:', code, flags=re.MULTILINE)
        
        # Fix the array literal syntax
        code = re.sub(r'list\[(.*?)\]', r'[\1]', code)
        code = re.sub(r'squadron\[(.*?)\]', r'[\1]', code)
        
        # Fix dictionary syntax - handle datapad without braces differently
        code = re.sub(r'dict\s*:\s*$', r'dict(', code, flags=re.MULTILINE)  # Start dict
        # But we need a more comprehensive solution
        
        # Fix set literal syntax 
        code = re.sub(r'set\[(.*?)\]', r'{\1}', code)
        
        # Fix ternary operator results - fix the regex pattern to avoid false matches
        # This was causing issues, let's remove it for now
        # code = re.sub(r'\(([^,]+),\s*([^,]+),\s*([^)]+)\)', r'(\2 if \1 else \3)', code)
        
        # Handle variable declarations
        force_var_pattern = r'force_var\s+(\w+)\s*=\s*(.+)'
        
        def replace_var(match):
            var_name = match.group(1)
            value = match.group(2)
            self.variables.add(var_name)
            return f"{var_name} = {value}"
        
        code = re.sub(force_var_pattern, replace_var, code)
        
        # Handle constant declarations
        force_const_pattern = r'force_const\s+(\w+)\s*=\s*(.+)'
        
        def replace_const(match):
            const_name = match.group(1)
            value = match.group(2)
            self.constants.add(const_name)
            return f"{const_name} = {value}"
        
        code = re.sub(force_const_pattern, replace_const, code)
        
            # Handle print statements by adding parentheses
        code = re.sub(r'print\s+(.+?)$', r'print(\1)', code, flags=re.MULTILINE)
        
        # Fix function calls that weren't properly handled
        # Note: ternary is already handled in special patterns
        
        # Rename .train() method calls to proper Python train() method
        code = re.sub(r'\.train\s*\(', r'.train(', code)
        
        # Convert curly braces to Python indentation
        return self.convert_braces_to_indentation(code)
    
    def convert_braces_to_indentation(self, code: str) -> str:
        """Convert curly braces syntax to Python indentation"""
        # First, handle } else { patterns specially - put else on new line
        code = re.sub(r'\s*\}\s*else\s*\{\s*$', '\nelse:', code, flags=re.MULTILINE)
        
        # Replace opening braces with colons, but protect dictionary literals
        # Dictionary literals are on single lines with = and both { and }
        lines = code.split('\n')
        result_lines = []
        
        for line in lines:
            stripped = line.strip()
            # Check if this line is a single-line dictionary literal 
            if ('=' in stripped and 
                '{' in stripped and 
                '}' in stripped and 
                stripped.count('{') == stripped.count('}') and
                stripped.endswith('}')):
                # This is a dictionary literal, don't convert braces
                result_lines.append(line)
            else:
                # Convert opening braces to colons for control structures
                line = re.sub(r'\s*\{\s*$', ':', line)
                result_lines.append(line)
        
        code = '\n'.join(result_lines)
        
        lines = code.split('\n')
        result_lines = []
        indent_level = 0
        
        for line in lines:
            stripped = line.strip()
            
            # Handle lines that are only closing braces (end of code blocks)
            if stripped == '}':
                indent_level -= 1
                indent_level = max(0, indent_level)
                continue
            
            # Skip empty lines
            if not stripped:
                continue
            
            # Handle lines starting with else: - these should be at current block level minus 1
            if stripped.startswith('else:'):
                result_lines.append('    ' * (indent_level - 1) + stripped)
                continue
            
            # Handle closing braces at the end of lines (but not inside data structures)
            # Only treat } as a structural closing brace if it's at the very end
            if stripped.endswith('}') and not ('{' in stripped and stripped.count('{') >= stripped.count('}')):
                # This is likely a structural closing brace
                indent_level -= stripped.count('}')
                indent_level = max(0, indent_level)
                # Remove only the trailing braces
                line = re.sub(r'\s*\}+\s*$', '', line)
                stripped = line.strip()
            
            # Only process non-empty lines
            if stripped:
                # Apply current indentation
                result_lines.append('    ' * indent_level + stripped)
            
            # Check if line ends with a colon (converted from an opening brace)
            if stripped.endswith(':'):
                indent_level += 1
        
        return '\n'.join(result_lines)

class ForceRuntime:
    """Runtime environment for The Force Programming Language"""
    
    def __init__(self):
        self.globals = {
            # Built-in variables
            'force_power': 0,
            
            # Mathematical functions
            'force_random': self._force_random,
            'force_distance': self._force_distance,
            'force_math_sqrt': math.sqrt,
            'force_math_abs': abs,
            'force_math_round': round,
            'force_math_max': max,
            'force_math_min': min,
            'force_math_sum': sum,
            
            # String functions
            'force_format': self._force_format,
            'force_text': self._force_text,
            'force_regex': self._force_regex,
            
            # File operations
            'force_read_file': self._force_read_file,
            'force_write_file': self._force_write_file,
            
            # Data structure operations
            'force_generator': self._force_generator,
            'force_stack': self._force_stack,
            'force_queue': self._force_queue,
            
            # JSON processing
            'force_json': self._force_json,
            
            # Control flow
            'force_ternary': self._force_ternary,
            'force_switch': self._force_switch,
            
            # Date/time operations
            'force_datetime': self._force_datetime,
            
            # Network operations
            'force_http': self._force_http,
            
            # Encryption/security
            'force_encryption': self._force_encryption,
            'force_hash_func': self._force_hash_func,
        }
    
    def _force_random(self, *args) -> float:
        """Generate random numbers (midichlorians)"""
        if len(args) == 0:
            return random.random()
        elif len(args) == 1:
            return random.randint(0, args[0])
        elif len(args) == 2:
            return random.randint(args[0], args[1])
        else:
            return random.choice(args)
    
    def _force_distance(self, x1, y1, x2=0, y2=0) -> float:
        """Calculate distance between two points (lightsaber_distance)"""
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    def _force_format(self, template: str, *args) -> str:
        """Format strings with arguments (hologram_text)"""
        try:
            return template.format(*args)
        except:
            return template
    
    def _force_text(self, operation: str, text: str, *args) -> str:
        """Text processing operations (protocol_droid)"""
        operations = {
            'uppercase': lambda t: t.upper(),
            'lowercase': lambda t: t.lower(),
            'reverse': lambda t: t[::-1],
            'length': lambda t: str(len(t)),
            'replace': lambda t, old, new: t.replace(old, new) if len(args) >= 2 else t,
            'split': lambda t, sep=' ': t.split(sep if args else ' '),
            'strip': lambda t: t.strip(),
        }
        
        if operation in operations:
            return operations[operation](text, *args)
        return text
    
    def _force_read_file(self, filename: str) -> str:
        """Read file contents (holocron_archive)"""
        try:
            with open(filename, 'r') as f:
                return f.read()
        except Exception as e:
            print(f"The archives are incomplete: {e}")
            return ""
    
    def _force_write_file(self, filename: str, content: str) -> bool:
        """Write content to file (imperial_database)"""
        try:
            with open(filename, 'w') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"The Emperor's database is unreachable: {e}")
            return False
    
    def _force_generator(self, iterable):
        """Create a generator (hyperdrive)"""
        for item in iterable:
            yield item
    
    def _force_ternary(self, condition, true_val, false_val):
        """Ternary operator (jedi_mind_trick)"""
        return true_val if condition else false_val
    
    def _force_regex(self, operation: str, pattern: str, text: str, *args):
        """Regular expression operations (regex_pattern)"""
        import re as regex_module
        
        operations = {
            'match': lambda p, t: bool(regex_module.match(p, t)),
            'search': lambda p, t: bool(regex_module.search(p, t)),
            'findall': lambda p, t: regex_module.findall(p, t),
            'sub': lambda p, t, r: regex_module.sub(p, r, t) if args else t,
            'split': lambda p, t: regex_module.split(p, t),
        }
        
        if operation in operations:
            return operations[operation](pattern, text, *args)
        return text
    
    def _force_stack(self, initial_items=None):
        """Create a stack data structure (stack_tower)"""
        stack = list(initial_items) if initial_items else []
        
        class ForceStack:
            def __init__(self, items):
                self.items = items
            
            def push(self, item):
                self.items.append(item)
                return self
            
            def pop(self):
                return self.items.pop() if self.items else None
            
            def peek(self):
                return self.items[-1] if self.items else None
            
            def is_empty(self):
                return len(self.items) == 0
            
            def size(self):
                return len(self.items)
        
        return ForceStack(stack)
    
    def _force_queue(self, initial_items=None):
        """Create a queue data structure (queue_line)"""
        from collections import deque
        queue = deque(initial_items) if initial_items else deque()
        
        class ForceQueue:
            def __init__(self, items):
                self.items = items
            
            def enqueue(self, item):
                self.items.append(item)
                return self
            
            def dequeue(self):
                return self.items.popleft() if self.items else None
            
            def front(self):
                return self.items[0] if self.items else None
            
            def is_empty(self):
                return len(self.items) == 0
            
            def size(self):
                return len(self.items)
        
        return ForceQueue(queue)
    
    def _force_json(self, operation: str, data, *args):
        """JSON processing operations (data_stream)"""
        import json
        
        operations = {
            'stringify': lambda d: json.dumps(d, indent=2),
            'parse': lambda s: json.loads(s) if isinstance(s, str) else s,
            'load': lambda f: json.load(open(f, 'r')) if isinstance(f, str) else None,
            'save': lambda d, f: json.dump(d, open(f, 'w'), indent=2) if len(args) >= 1 else None,
        }
        
        try:
            if operation in operations:
                return operations[operation](data, *args)
        except Exception as e:
            print(f"JSON processing error: {e}")
        
        return data
    
    def _force_switch(self, value, cases_dict, default=None):
        """Switch-case equivalent (jedi_council)"""
        return cases_dict.get(value, default)
    
    def _force_datetime(self, operation: str, *args):
        """Date/time operations (galactic_time)"""
        from datetime import datetime, timedelta
        
        operations = {
            'now': lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'timestamp': lambda: int(datetime.now().timestamp()),
            'format': lambda dt, fmt='%Y-%m-%d %H:%M:%S': dt.strftime(fmt) if hasattr(dt, 'strftime') else str(dt),
            'parse': lambda s, fmt='%Y-%m-%d %H:%M:%S': datetime.strptime(s, fmt),
            'add_days': lambda dt, days: dt + timedelta(days=days) if hasattr(dt, '__add__') else dt,
            'add_hours': lambda dt, hours: dt + timedelta(hours=hours) if hasattr(dt, '__add__') else dt,
        }
        
        try:
            if operation in operations:
                return operations[operation](*args)
        except Exception as e:
            print(f"DateTime operation error: {e}")
        
        return None
    
    def _force_http(self, method: str, url: str, **kwargs):
        """HTTP client operations (hyperspace_comm)"""
        try:
            import requests
            
            if method.upper() == 'GET':
                response = requests.get(url, **kwargs)
            elif method.upper() == 'POST':
                response = requests.post(url, **kwargs)
            elif method.upper() == 'PUT':
                response = requests.put(url, **kwargs)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, **kwargs)
            else:
                return {'error': 'Unsupported HTTP method'}
            
            return {
                'status_code': response.status_code,
                'text': response.text,
                'json': response.json() if response.headers.get('content-type', '').startswith('application/json') else None,
                'headers': dict(response.headers)
            }
        except ImportError:
            return {'error': 'requests library not available'}
        except Exception as e:
            return {'error': str(e)}
    
    def _force_encryption(self, operation: str, data: str, key: str = None):
        """Encryption operations (force_encrypt)"""
        import hashlib
        import base64
        
        if operation == 'base64_encode':
            return base64.b64encode(data.encode()).decode()
        elif operation == 'base64_decode':
            try:
                return base64.b64decode(data.encode()).decode()
            except:
                return "Decoding failed"
        elif operation == 'simple_cipher':
            # Simple Caesar cipher
            shift = len(key) if key else 3
            result = ""
            for char in data:
                if char.isalpha():
                    ascii_offset = ord('a') if char.islower() else ord('A')
                    result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
                else:
                    result += char
            return result
        
        return data
    
    def _force_hash_func(self, algorithm: str, data: str):
        """Hash functions (force_hash)"""
        import hashlib
        
        algorithms = {
            'md5': hashlib.md5,
            'sha1': hashlib.sha1,
            'sha256': hashlib.sha256,
            'sha512': hashlib.sha512,
        }
        
        if algorithm in algorithms:
            return algorithms[algorithm](data.encode()).hexdigest()
        
        return "Unsupported algorithm"
    
    def run_code(self, python_code: str) -> Any:
        """Execute the translated Python code"""
        try:
            # First, try to compile the code to check for syntax errors
            compiled_code = compile(python_code, '<force_code>', 'exec')
            
            # Execute the code in the global namespace
            exec(compiled_code, self.globals)
            
            # If there's a main function, call it
            if 'main' in self.globals and callable(self.globals['main']):
                return self.globals['main']()
            
            return "Code executed successfully - The Force is strong with this one"
        except SyntaxError as e:
            print(f"The dark side clouds your syntax: {e}")
            return None
        except NameError as e:
            print(f"These aren't the variables you're looking for: {e}")
            return None
        except TypeError as e:
            print(f"Your lack of type faith is disturbing: {e}")
            return None
        except ValueError as e:
            print(f"The value you seek is not the value you need: {e}")
            return None
        except FileNotFoundError as e:
            print(f"The archives are incomplete: {e}")
            return None
        except ZeroDivisionError as e:
            print(f"Even the Force cannot divide by zero: {e}")
            return None
        except IndexError as e:
            print(f"These aren't the indices you're looking for: {e}")
            return None
        except KeyError as e:
            print(f"The key to the Force you seek, exists it does not: {e}")
            return None
        except Exception as e:
            print(f"I find your lack of faith disturbing: {e}")
            traceback.print_exc()
            return None

class ForceInterpreter:
    """Main interpreter class for The Force Programming Language"""
    
    def __init__(self):
        self.parser = ForceParser()
        self.runtime = ForceRuntime()
    
    def run_force_code(self, force_code: str) -> Any:
        """Parse and run Force code"""
        python_code = self.parser.translate_to_python(force_code)
        
        # Uncomment to debug the Python translation
        print("Translated Python code:")
        print("----------------------")
        print(python_code)
        print("----------------------")
        
        return self.runtime.run_code(python_code)
    
    def run_force_file(self, filename: str) -> Any:
        """Read and run Force code from a file"""
        try:
            with open(filename, 'r') as file:
                force_code = file.read()
            return self.run_force_code(force_code)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return None
        except Exception as e:
            print(f"Error reading file: {e}")
            return None

def main():
    """Main entry point for the Force compiler"""
    if len(sys.argv) < 2:
        print("Usage: python force_compiler.py <force_file>")
        print("Or: python force_compiler.py --interactive")
        return
    
    interpreter = ForceInterpreter()
    
    if sys.argv[1] == "--interactive":
        print("=== The Force Programming Language Interactive Shell ===")
        print("Type 'exit()' to quit")
        
        while True:
            try:
                line = input(">>> ")
                if line.strip() == "exit()":
                    break
                result = interpreter.run_force_code(line)
                if result is not None:
                    print(result)
            except KeyboardInterrupt:
                print("\nExiting Force shell...")
                break
            except Exception as e:
                print(f"Error: {e}")
    else:
        interpreter.run_force_file(sys.argv[1])

if __name__ == "__main__":
    main()