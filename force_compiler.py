#!/usr/bin/env python3
"""
The Force Programming Language Compiler/Interpreter
A Python-based implementation that translates Force code to Python and executes it.
"""

import re
import sys
import ast
import traceback
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
        }
        
        # Special patterns that need custom handling
        self.special_patterns = [
            # Handle array access: rebels[0] -> rebels[0]
            (r'(\w+)\[([^\]]+)\]', r'\1[\2]'),
            
            # Handle new keyword for classes
            (r'new (\w+)\(', r'\1('),
            
            # Handle array literal: squadron["a", "b"] -> ["a", "b"]
            (r'squadron\[(.*?)\]', r'[\1]'),
            
            # Handle dictionary literal: datapad { a: 1, b: 2 } -> {"a": 1, "b": 2}
            (r'datapad\s*{(.*?)}', self._handle_datapad),
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
        
        # Rename .train() method calls to proper Python train() method
        code = re.sub(r'\.train\s*\(', r'.train(', code)
        
        # Convert curly braces to Python indentation
        return self.convert_braces_to_indentation(code)
    
    def convert_braces_to_indentation(self, code: str) -> str:
        """Convert curly braces syntax to Python indentation"""
        # Replace opening braces with colons
        code = re.sub(r'\s*\{\s*$', ':', code, flags=re.MULTILINE)
        
        lines = code.split('\n')
        result_lines = []
        indent_level = 0
        
        for line in lines:
            stripped = line.strip()
            
            # Handle closing braces
            closing_braces = stripped.count('}')
            indent_level -= closing_braces
            indent_level = max(0, indent_level)  # Ensure indent level doesn't go negative
            
            # Remove closing braces
            line = re.sub(r'\s*\}\s*', '', line)
            
            # Only process non-empty lines after removing braces
            if line.strip():
                # Apply current indentation
                result_lines.append('    ' * indent_level + line.strip())
            
            # Count any remaining braces for next line's indentation
            stripped_after = line.strip()
            # Check if line ends with a colon (converted from an opening brace)
            if stripped_after.endswith(':'):
                indent_level += 1
        
        return '\n'.join(result_lines)

class ForceRuntime:
    """Runtime environment for The Force Programming Language"""
    
    def __init__(self):
        self.globals = {
            # Add any built-in functions or variables here
            'force_power': 0,
        }
    
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
            
            return "Code executed successfully"
        except Exception as e:
            print(f"The dark side clouds everything: {e}")
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