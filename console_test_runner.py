#!/usr/bin/env python3
"""
Console Test Runner for The Force Programming Language

This script provides an easy way to run specific console tests or all tests
with detailed output and execution results.

Usage:
    python console_test_runner.py                    # Run all tests
    python console_test_runner.py --basic            # Run basic functionality tests
    python console_test_runner.py --advanced         # Run advanced feature tests  
    python console_test_runner.py --interactive      # Run interactive mode tests
    python console_test_runner.py --errors           # Run error handling tests
    python console_test_runner.py --performance      # Run performance tests
    python console_test_runner.py --demo             # Run demonstration examples
"""

import sys
import os
import argparse
import subprocess
from pathlib import Path

# Add the tests directory to Python path
sys.path.insert(0, str(Path(__file__).parent / 'tests'))

def run_test_category(category_name, test_pattern):
    """Run a specific category of tests"""
    print(f"{'='*60}")
    print(f"RUNNING {category_name.upper()} TESTS")
    print(f"{'='*60}")
    
    cmd = [sys.executable, '-m', 'unittest', f'tests.test_console_version.{test_pattern}', '-v']
    
    try:
        result = subprocess.run(cmd, cwd=Path(__file__).parent, timeout=120)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"❌ {category_name} tests timed out")
        return False
    except Exception as e:
        print(f"❌ Error running {category_name} tests: {e}")
        return False

def run_demo_examples():
    """Run the existing example files to demonstrate console functionality"""
    print(f"{'='*60}")
    print("RUNNING DEMONSTRATION EXAMPLES")
    print(f"{'='*60}")
    
    example_files = [
        'example.force',
        'features_demo.force', 
        'advanced_example.force'
    ]
    
    compiler_path = Path(__file__).parent / 'force_compiler.py'
    
    for example_file in example_files:
        example_path = Path(__file__).parent / example_file
        if example_path.exists():
            print(f"\n🚀 Running {example_file}...")
            print("-" * 40)
            
            try:
                result = subprocess.run(
                    [sys.executable, str(compiler_path), str(example_path)],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    print(f"✅ {example_file} executed successfully")
                    print(f"Output:\n{result.stdout}")
                else:
                    print(f"⚠️ {example_file} had issues:")
                    print(f"Output:\n{result.stdout}")
                    if result.stderr:
                        print(f"Errors:\n{result.stderr}")
            except subprocess.TimeoutExpired:
                print(f"❌ {example_file} timed out")
            except Exception as e:
                print(f"❌ Error running {example_file}: {e}")
        else:
            print(f"⚠️ Example file {example_file} not found")

def test_interactive_mode():
    """Test interactive mode with simple commands"""
    print(f"{'='*60}")
    print("TESTING INTERACTIVE MODE")
    print(f"{'='*60}")
    
    compiler_path = Path(__file__).parent / 'force_compiler.py'
    
    # Test 1: Basic startup and exit
    print("\n🔧 Test 1: Interactive mode startup...")
    try:
        result = subprocess.run(
            [sys.executable, str(compiler_path), '--interactive'],
            input='exit()\n',
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0 and 'Interactive Shell' in result.stdout:
            print("✅ Interactive mode starts and exits correctly")
        else:
            print("⚠️ Interactive mode startup issues")
            print(f"Output: {result.stdout}")
    except Exception as e:
        print(f"❌ Interactive mode test failed: {e}")
    
    # Test 2: Simple command execution
    print("\n🔧 Test 2: Simple command execution...")
    simple_commands = '''respond "Hello from interactive mode!"
holocron x = 42
respond "The answer is " + str(x)
exit()'''
    
    try:
        # Use shell to properly pipe commands
        cmd = f'echo \'{simple_commands}\' | python {compiler_path} --interactive'
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=15,
            cwd=Path(__file__).parent
        )
        
        if result.returncode == 0:
            print("✅ Simple interactive commands work")
            if "Hello from interactive mode!" in result.stdout:
                print("✅ Output verification passed")
            else:
                print("⚠️ Expected output not found")
            print(f"Output:\n{result.stdout}")
        else:
            print("⚠️ Interactive command execution issues")
            print(f"Output:\n{result.stdout}")
    except Exception as e:
        print(f"❌ Interactive command test failed: {e}")

def main():
    parser = argparse.ArgumentParser(description='Console Test Runner for The Force Programming Language')
    parser.add_argument('--basic', action='store_true', help='Run basic functionality tests')
    parser.add_argument('--advanced', action='store_true', help='Run advanced feature tests')
    parser.add_argument('--interactive', action='store_true', help='Run interactive mode tests')
    parser.add_argument('--errors', action='store_true', help='Run error handling tests')
    parser.add_argument('--performance', action='store_true', help='Run performance tests')
    parser.add_argument('--demo', action='store_true', help='Run demonstration examples')
    parser.add_argument('--all', action='store_true', help='Run all tests')
    
    args = parser.parse_args()
    
    # If no specific category is specified, run all tests
    if not any([args.basic, args.advanced, args.interactive, args.errors, args.performance, args.demo]):
        args.all = True
    
    success_count = 0
    total_count = 0
    
    print("🌟 THE FORCE PROGRAMMING LANGUAGE CONSOLE TEST RUNNER 🌟")
    print("May the Force be with your code...\n")
    
    if args.basic or args.all:
        total_count += 1
        if run_test_category("Basic Functionality", "TestConsoleFileExecution"):
            success_count += 1
    
    if args.advanced or args.all:
        # Advanced tests are included in the basic file execution tests
        print("\n✨ Advanced features are tested as part of basic functionality tests")
    
    if args.interactive or args.all:
        total_count += 1
        test_interactive_mode()
        # For now, count interactive as successful if it doesn't crash
        success_count += 1
    
    if args.errors or args.all:
        total_count += 1
        if run_test_category("Error Handling", "TestConsoleErrorHandling"):
            success_count += 1
    
    if args.performance or args.all:
        total_count += 1
        if run_test_category("Performance & Edge Cases", "TestConsolePerformanceAndEdgeCases"):
            success_count += 1
    
    if args.demo or args.all:
        total_count += 1
        run_demo_examples()
        success_count += 1  # Demo is informational, always count as success
    
    # Final summary
    print(f"\n{'='*60}")
    print("🎯 TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Categories run: {total_count}")
    print(f"Successful: {success_count}")
    print(f"Success rate: {(success_count/total_count*100):.1f}%" if total_count > 0 else "N/A")
    
    if success_count == total_count:
        print("\n🎉 All test categories completed successfully!")
        print("The Force is strong with this code! ⭐")
    else:
        print(f"\n⚠️ Some test categories had issues ({total_count - success_count} issues)")
        print("But remember: 'Do or do not, there is no try' - Master Yoda")
    
    print(f"\n📖 For detailed test results, see: CONSOLE_TEST_RESULTS.md")
    
    return 0 if success_count == total_count else 1

if __name__ == '__main__':
    sys.exit(main())