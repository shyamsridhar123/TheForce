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

1. **Clone the repository**:
   ```bash
   git clone https://your-repo-url.git
   cd TheForce
   ```
2. **Run a .force file**:
   ```bash
   python force_compiler.py example.force
   ```
3. **Interactive mode**:
   ```bash
   python force_compiler.py --interactive
   ```

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

### New Advanced Features

| TFPL Keyword            | Python Equivalent    | Description                    |
|-------------------------|----------------------|--------------------------------|
| `force_calculate`       | math operations      | Mathematical calculations      |
| `midichlorians`         | random functions     | Random number generation       |
| `lightsaber_distance`   | distance calc        | Calculate distance/length      |
| `rebellion[...]`        | set{...}             | Set literal                    |
| `jedi_mind_trick`       | ternary operator     | Conditional expressions        |
| `hologram_text`         | f-strings            | String formatting              |
| `protocol_droid`        | text functions       | Text processing operations     |
| `holocron_archive`      | file reading         | Read file contents             |
| `imperial_database`     | file writing         | Write content to file          |
| `hyperdrive`            | generators           | Create generators/iterators    |

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

#### Sets (Rebellion)
```force
holocron unique_planets = rebellion["Tatooine", "Coruscant", "Dagobah"]
```

### Mathematical Operations

#### Basic Calculations
```force
holocron sum = force_calculate("add", 10, 15)        // 25
holocron product = force_calculate("multiply", 6, 7)  // 42
holocron power = force_calculate("power", 2, 8)      // 256
```

#### Random Numbers (Midichlorians)
```force
holocron random_val = midichlorians()                // 0.0 to 1.0
holocron dice_roll = midichlorians(1, 6)            // 1 to 6
holocron reading = midichlorians(1000, 50000)       // Jedi midichlorian count
```

#### Distance Calculations
```force
holocron combat_range = lightsaber_distance(0, 0, 10, 15)  // 18.03 meters
```

### Advanced Control Flow

#### Ternary Operations (Jedi Mind Tricks)
```force
holocron status = jedi_mind_trick(power > 50, "Strong", "Weak")
```

### Text Processing (Protocol Droid)

```force
holocron message = "May the Force be with you"
respond protocol_droid("uppercase", message)  // MAY THE FORCE BE WITH YOU
respond protocol_droid("reverse", message)    // uoy htiw eb ecroF eht yaM
respond protocol_droid("length", message)     // 25
```

### File Operations

#### Holocron Archives (File Reading)
```force
holocron content = holocron_archive("jedi_wisdom.txt")
```

#### Imperial Database (File Writing)
```force
imperial_database("report.txt", "Mission accomplished")
``` 

### I/O

- Output: `respond "..."`
- Input: `holocron name = sense_input("Enter:")`

### Enhanced Error Handling

The Force provides themed error messages that make debugging more engaging:

- **Syntax errors**: "The dark side clouds your syntax"
- **Name errors**: "These aren't the variables you're looking for"
- **Type errors**: "Your lack of type faith is disturbing"  
- **File errors**: "The archives are incomplete"
- **Zero division**: "Even the Force cannot divide by zero"
- **Index errors**: "These aren't the indices you're looking for"
- **Key errors**: "The key to the Force you seek, exists it does not"

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
