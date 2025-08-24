# Getting Started with The Force

Welcome to The Force Programming Language! This guide will help you set up and start coding in a galaxy far, far away.

## Installation

### Prerequisites

- **Python**: 3.7 or higher
- **Web Browser**: Modern browser with JavaScript support
- **Operating System**: Windows, macOS, or Linux

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/shyamsridhar123/TheForce.git
   cd TheForce
   ```

2. **Verify installation**:
   ```bash
   python force_compiler.py --help
   ```

## Quick Start Options

### Web Interface (Recommended)

Experience The Force in your browser with our enhanced Star Wars-themed web IDE:

1. **Start the web server**:
   ```bash
   python force_web_server.py
   ```

2. **Open your browser** to `http://localhost:8000` and start exploring The Force!

**Web Interface Features:**
- 🌙/☀️ **Theme Toggle**: Switch between Dark Side and Light Side themes
- 📝 **7 Interactive Examples**: From basic syntax to advanced features
- ⌨️ **Keyboard Shortcuts**: 
  - `Ctrl+Enter`: Run code
  - `Ctrl+B`: Compile code
  - `Ctrl+S`: Export code
  - `Ctrl+T`: Toggle theme
  - `Ctrl+K`: Clear editor
- 💾 **Export**: Download your programs as `.force` files
- 🔍 **Enhanced Reference**: Categorized quick reference guide

### Command Line Interface

For those who prefer the command line:

1. **Run a .force file**:
   ```bash
   python force_compiler.py example.force
   ```
   
2. **Run the advanced features demo**:
   ```bash
   python force_compiler.py advanced_features_demo.force
   ```

3. **Interactive mode**:
   ```bash
   python force_compiler.py --interactive
   ```

## Your First Force Program

Create a file called `hello_galaxy.force`:

```force
// Your first Force program
respond "Hello, Galaxy!"
respond "May the Force be with you!"

holocron jedi_name = "Luke Skywalker"
respond "Welcome, " + jedi_name
```

Run it:
```bash
python force_compiler.py hello_galaxy.force
```

## Testing Your Setup

This release includes a comprehensive testing framework to verify everything is working:

```bash
# Run all tests
python tests/run_tests.py

# Run specific test categories
python tests/test_force_compiler.py    # Compiler tests
python tests/test_new_features.py      # New language features
python tests/test_web_server.py        # Web interface tests
```

**Test Coverage:**
- ✅ **49 Total Tests** with 100% pass rate
- ✅ **30 Compiler Tests**: Core language features
- ✅ **9 Advanced Feature Tests**: New data structures and functions  
- ✅ **10 Web Server Tests**: API endpoints and functionality

## Next Steps

- 📚 Read the [Language Reference](language-reference.md) for complete syntax documentation
- 💡 Try the [Examples](examples.md) to learn different features
- 🌐 Explore the [Web Interface Guide](web-interface.md) for the full web IDE experience
- 🤝 Check out [Contributing](contributing.md) if you want to help improve The Force

## Troubleshooting

### Common Issues

**Python not found:**
- Ensure Python 3.7+ is installed and in your PATH
- Try `python3` instead of `python` on some systems

**Port 8000 already in use:**
- The web server uses port 8000 by default
- Kill any existing processes using that port or modify `force_web_server.py`

**Import errors:**
- Ensure you're running commands from the project root directory
- Check that all required files are present

### Getting Help

- Check the [Examples](examples.md) for common patterns
- Review the [Language Reference](language-reference.md) for syntax details
- Open an issue on GitHub if you encounter bugs

May the Force be with you! 🌟