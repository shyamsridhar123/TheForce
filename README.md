# The Force Programming Language

![The Force Web IDE](https://github.com/user-attachments/assets/e8cd8bab-8023-49c9-804a-03f9e14e4b06)

*A long time ago in a galaxy far, far away...*

**The Force Programming Language** is a Star Wars-themed programming language that transpiles to Python. Designed for both education and entertainment, it combines the beloved Star Wars universe with programming fundamentals, making coding an adventure through the galaxy.

## 🚀 Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/shyamsridhar123/TheForce.git
   cd TheForce
   ```

2. **Start the web interface**:
   ```bash
   python force_web_server.py
   ```

3. **Open your browser** to `http://localhost:8000` and start exploring!

4. **Try the command line** (optional):
   ```bash
   python force_compiler.py example.force          # Run a file
   python force_compiler.py --interactive         # Interactive mode
   ```

## 📖 Documentation

Our documentation has been organized into a comprehensive guide:

- **📚 [Complete Documentation](docs/index.md)** - Start here for the full documentation hub
- **🚀 [Getting Started](docs/getting-started.md)** - Installation, setup, and first steps  
- **🌐 [Web Interface Guide](docs/web-interface.md)** - Master the Star Wars-themed IDE
- **📖 [Language Reference](docs/language-reference.md)** - Complete syntax and features
- **💡 [Examples](docs/examples.md)** - Learn through practical examples
- **🤝 [Contributing](docs/contributing.md)** - Join our galactic development team

### Development Documentation
- **🔧 [Development Docs](docs/development/)** - Technical documentation for contributors
- **📋 [Product Requirements](docs/prd.md)** - PRD and roadmap

## ✨ What's New

### 🚀 **Major Language Enhancements**
- **Advanced Data Structures**: Stacks (`stack_tower`), Queues (`queue_line`), and Tuples (`tuple_coordinates`)
- **JSON Processing**: Full JSON support with `data_stream` operations
- **Date & Time Operations**: Galactic time management with `galactic_time`
- **Security & Encryption**: Base64 encoding/decoding and hashing with `force_encrypt` and `force_hash`
- **Regular Expressions**: Pattern matching with `regex_pattern` operations
- **Switch-Case Logic**: Advanced decision making with `jedi_council`

### 🎨 **Enhanced Web Interface**
- **Theme Toggle**: Switch between Dark Side and Light Side themes
- **7 Interactive Examples**: From basic syntax to advanced features
- **Enhanced Quick Reference**: Organized by categories with all new keywords
- **Export Functionality**: Download your `.force` programs as `.force` files
- **Improved UI Design**: Better organized sidebar with grouped references
- **Keyboard Shortcuts**: Full keyboard support for power users

### 🧪 **Comprehensive Testing**
- **67 Unit Tests** with extensive feature coverage
- **Automated Testing Framework** for continuous validation
- **Integration Tests** for web server functionality  
- **Feature-Specific Tests** for all new language constructs

## 🔥 Quick Example

```force
// Your first Force program
order Jedi {
  initiate(self, name) {
    self.name = name
    self.power = 50
  }
  
  ability train(self) {
    self.power = self.power + 10
    respond self.name + " gains power: " + str(self.power)
  }
}

holocron luke = new Jedi("Luke Skywalker")
luke.train()
respond "May the Force be with you!"
```

## 🧪 Testing & Quality

- ✅ **67 Total Tests** with 95.5% pass rate
- ✅ **Comprehensive Test Coverage** for all features  
- ✅ **Automated Testing Framework** for continuous validation
- ✅ **Integration Tests** for web server functionality
- ✅ **Feature-Specific Tests** for all new language constructs

Run tests with: `python tests/run_tests.py`

## 📋 Sample Programs

Explore practical examples in the [`samples/`](samples/) directory:

- **🌟 [hello-galaxy](samples/hello-galaxy/)** - Basic syntax and variables
- **⚔️ [jedi-academy](samples/jedi-academy/)** - Object-oriented programming with classes
- **🗃️ [galactic-database](samples/galactic-database/)** - Data structures and collections
- **📡 [rebel-communications](samples/rebel-communications/)** - Text processing and encryption
- **🧮 [navigation-system](samples/navigation-system/)** - Mathematical operations
- **🚀 [mission-control](samples/mission-control/)** - Complex application showcase

Each sample includes detailed documentation and demonstrates different aspects of The Force language.

## 🌟 Key Features

- **Star Wars Themed Syntax**: Learn programming with Jedi, Sith, and galactic terminology
- **Python Transpilation**: Your Force code runs as optimized Python
- **Interactive Web IDE**: Code in a beautiful, space-themed interface with theme toggle
- **Educational Focus**: Perfect for learning programming concepts in an engaging way
- **Advanced Data Structures**: Support for stacks, queues, tuples, and JSON processing
- **Security Features**: Built-in encryption and hashing capabilities
- **Pattern Matching**: Regular expression support for text processing
- **Comprehensive Documentation**: Detailed guides, examples, and API reference
- **Active Development**: Regular updates and new features
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🎯 Language Philosophy

The Force Programming Language bridges the gap between entertainment and education by using familiar Star Wars terminology to make programming concepts more accessible and memorable. Whether you're a Padawan learning your first programming concepts or a Jedi Master exploring advanced techniques, The Force provides an engaging way to develop coding skills while having fun with the galaxy far, far away.

## 🤝 Community

We welcome contributions from developers across the galaxy! Check out our [Contributing Guide](docs/contributing.md) to get started.

### Areas for Contribution
- 🌟 New language features and Star Wars-themed keywords
- 🎨 Web interface improvements and themes
- 📚 Examples, tutorials, and educational content
- 🧪 Testing and quality assurance
- 📖 Documentation improvements

## 📋 System Requirements

- **Python**: 3.7 or higher
- **Web Browser**: Modern browser with JavaScript support
- **Operating System**: Windows, macOS, or Linux

## 📄 License

MIT © 2025 The Force Dev Team

---

**May the Force be with you!** 🌟

*For complete documentation, examples, and guides, visit our [documentation hub](docs/index.md).*