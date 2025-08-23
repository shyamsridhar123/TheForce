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
            
            # String manipulation
            r'\bhologram_text\b': 'force_format', # String formatting
            r'\bprotocol_droid\b': 'force_text',  # Text processing
            
            # File operations
            r'\bholocron_archive\b': 'force_read_file',  # File reading
            r'\bimperial_database\b': 'force_write_file', # File writing
            
            # Control flow enhancements
            r'\bjedi_mind_trick\b': 'force_ternary',  # Ternary operator
        }
        
        # Special patterns that need custom handling
        self.special_patterns = [            
            # Handle new keyword for classes
            (r'new (\w+)\(', r'\1('),
            
            # Handle array literal: squadron["a", "b"] -> ["a", "b"]
            (r'squadron\[(.*?)\]', r'[\1]'),
            
            # Handle dictionary literal: datapad { a: 1, b: 2 } -> {"a": 1, "b": 2}
            (r'datapad\s*{(.*?)}', self._handle_datapad),
            
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
        # Replace property names with quoted strings
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
        # Handle C-style for loops for train syntax: train (holocron i = 0; i < len(missions); i = i + 1) {
        code = re.sub(
            r'train\s*\(\s*holocron\s+(\w+)\s*=\s*(\d+)\s*;\s*\1\s*<\s*len\(([^)]+)\)\s*;\s*\1\s*=\s*\1\s*\+\s*(\d+)\s*\)\s*\{',
            r'for \1 in range(\2, len(\3), \4):',
            code
        )
        
        # Apply keyword mappings
        for pattern, replacement in self.keyword_map.items():
            code = re.sub(pattern, replacement, code)
        
        # Fix class methods by adding 'def' keyword if missing
        code = re.sub(r'(\s+)(__init__\s*\([^)]*\))', r'\1def \2', code)
        code = re.sub(r'(\s+)(\w+\s*\([^)]*\))\s*:', r'\1def \2:', code)  # Add def to other methods
        
        # Apply special patterns
        for pattern, replacement in self.special_patterns:
            if callable(replacement):
                # If the replacement is a function, use re.sub with the function
                code = re.sub(pattern, replacement, code)
            else:
                # Otherwise, use regular re.sub
                code = re.sub(pattern, replacement, code)
        
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
        
        # Replace opening braces with colons
        code = re.sub(r'\s*\{\s*$', ':', code, flags=re.MULTILINE)
        
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
            
            # File operations
            'force_read_file': self._force_read_file,
            'force_write_file': self._force_write_file,
            
            # Advanced data structures
            'force_generator': self._force_generator,
            
            # Control flow
            'force_ternary': self._force_ternary,
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