# The Force Programming Language

```plaintext
####### #     # #######    ####### ####### ######   #####  ####### 
   #    #     # #          #       #     # #     # #     # #       
   #    #     # #          #       #     # #     # #       #       
   #    ####### #####      #####   #     # ######  #       #####   
   #    #     # #          #       #     # #   #   #       #       
   #    #     # #          #       #     # #    #  #     # #       
   #    #     # #######    #       ####### #     #  #####  ####### 
                                      
```


Welcome to **The Force Programming Language** (TFPL), a Star Wars–themed domain-specific language that compiles to Python.

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Language Syntax](#language-syntax)
   - [Comments](#comments)
   - [Keywords](#keywords)
   - [Variables & Constants](#variables--constants)
   - [Classes & Objects](#classes--objects)
   - [Functions](#functions)
   - [Control Flow](#control-flow)
   - [Data Structures](#data-structures)
   - [I/O](#io)
4. [Example Program](#example-program)
5. [PRD](#PRD)
6. [Contributing](#contributing)
7. [License](#license)

---

## Introduction

TFPL uses Star Wars terminology (Jedi, holocron, kyber) to teach programming concepts. It translates `.force` files into Python and executes them via `force_compiler.py`.

---

## Getting Started

### Web Interface (Recommended)

Experience The Force in your browser with our Star Wars-themed web IDE:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/shyamsridhar123/TheForce.git
   cd TheForce
   ```

2. **Start the web server**:
   ```bash
   python force_web_server.py
   ```

3. **Open your browser** to `http://localhost:8000` and start exploring The Force!

### Command Line Interface

1. **Run a .force file**:
   ```bash
   python force_compiler.py example.force
   ```
2. **Interactive mode**:
   ```bash
   python force_compiler.py --interactive
   ```

---

## Web Interface Features

The Force Web IDE provides an immersive Star Wars-themed programming experience:

### 🎮 **Interactive Code Editor**
- Syntax highlighting for The Force language keywords
- Real-time compilation to Python with visual feedback
- Code execution with live output display
- Auto-completion and error detection

### 🌟 **Star Wars Theming** 
- Space-themed background with animated stars
- Jedi/Sith color palette and typography
- Themed error messages and status updates
- Force power meter that responds to code complexity

### 📚 **Built-in Examples**
- **Hello Galaxy**: Simple greeting program
- **Jedi Training**: Class-based training simulation  
- **Squadron Mission**: Array and object manipulation
- Easy one-click loading of example code

### ⚡ **Developer Features**
- Quick reference guide for Force language syntax
- Keyboard shortcuts (Ctrl+Enter to run, Ctrl+B to compile)
- Responsive design for desktop and mobile
- Real-time Python code translation view

### 🚀 **Getting Started**
Open the web interface and try these features:
1. Click "Hello Galaxy" to load a simple example
2. Press the "▶ Run Code" button to execute
3. Watch the Python translation and output appear
4. Modify the code and see your Force power increase!

---

## Language Syntax

### Comments

- Single-line: `// This is a comment`
- Multi-line: `/* comment block */`

### Keywords

| TFPL Keyword        | Python Equivalent | Description             |
|---------------------|-------------------|-------------------------|
| `holocron`          | variable          | Declare a variable      |
| `kyber`             | constant          | Declare a constant      |
| `order`             | class             | Define a class          |
| `initiate`          | `__init__`        | Class constructor       |
| `ability`           | def               | Function definition     |
| `respond`           | print(...)        | Output                  |
| `sense_input`       | input(...)        | Input                   |
| `meditate`          | while             | While loop              |
| `sense`             | if                | If statement            |
| `else`              | else              | Else branch             |
| `train (…) {}`      | for (…) in range  | C-style for loops       |
| `squadron[...]`     | list[...]         | Array literal           |
| `datapad {…}`       | dict{…}           | Object literal          |
| `try_use_force`     | try               | Try block               |
| `catch_disturbance` | except            | Exception handler       |
| `finally_balance`   | finally           | Finally block           |
| `transmission`      | import            | Import module           |
| `from`              | from              | From-import             |

### Variables & Constants

```force
holocron x = 5     // variable
kyber PI = 3.14    // constant

respond x + PI
```

### Classes & Objects

```force
order Jedi {
  initiate(self, name) {
    self.name = name
  }
  ability greet(self) {
    respond "Hello, " + self.name
  }
}

// Instantiate
holocron y = new Jedi("Luke")
y.greet()
```

### Functions

```force
ability add(a, b) {
  respond a + b
}

add(2, 3)
```

### Control Flow

#### If/Else
```force
sense (x > 0) {
  respond "Positive"
} else {
  respond "Non-positive"
}
```

#### While
```force
meditate (count < 5) {
  respond count
  count = count + 1
}
```

#### For
```force
train (holocron i = 0; i < len(arr); i = i + 1) {
  respond arr[i]
}
```

### Data Structures

#### Arrays (Squadrons)
```force
holocron squad = squadron[1, 2, 3]
squad[0]  // 1
```

#### Objects (Datapads)
```force
datapad {a:1, b:2}
``` 

### I/O

- Output: `respond "..."`
- Input: `holocron name = sense_input("Enter:")`

---

## Example Program

```force
order Jedi {
  initiate(self, name) {
    self.name = name
    self.power = 50
  }
  ability train(self) {
    self.power = self.power + 10
    respond self.name + " trains. Power: " + str(self.power)
  }
}

ability main() {
  respond "Start training"
  holocron luke = new Jedi("Luke")
  holocron days = 0
  meditate (luke.power < 100) {
    luke.train()
    days = days + 1
  }
  respond "Done in " + str(days) + " days"
}

main()
```

---

## PRD
Please see the "the_force_prd.md" for information about key features and the roadmap.

## Contributing

Pull requests welcome! Please open an issue first for major changes.

---

## License

MIT © 2025 The Force Dev Team
