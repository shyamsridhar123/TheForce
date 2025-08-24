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
- **Advanced Data Structures**: Stacks, queues, and tuples
- **JSON Processing**: Full JSON support with `data_stream`
- **Security & Encryption**: Base64 and hashing with `force_encrypt`
- **Regular Expressions**: Pattern matching with `regex_pattern`
- **Switch-Case Logic**: Decision making with `jedi_council`

### 🎨 **Enhanced Web Interface**
- **Theme Toggle**: Dark Side and Light Side themes
- **7 Interactive Examples**: From basic syntax to advanced features
- **Export Functionality**: Download your `.force` programs
- **Keyboard Shortcuts**: Full keyboard support for power users

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

- ✅ **49 Total Tests** with 100% pass rate
- ✅ **Comprehensive Test Coverage** for all features
- ✅ **Automated Testing Framework** for continuous validation

Run tests with: `python tests/run_tests.py`

## 🌟 Key Features

- **Star Wars Themed Syntax**: Learn programming with Jedi, Sith, and galactic terminology
- **Python Transpilation**: Your Force code runs as optimized Python
- **Interactive Web IDE**: Code in a beautiful, space-themed interface
- **Educational Focus**: Perfect for learning programming concepts
- **Comprehensive Documentation**: Detailed guides and examples
- **Active Development**: Regular updates and new features

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