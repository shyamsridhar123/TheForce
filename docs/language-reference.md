# The Force Programming Language Reference

Complete syntax and feature documentation for The Force Programming Language.

## Comments
```force
// Single line comment
/* Multi-line comment */
```

## Keywords

### Core Language Features
| Force Keyword | Python Equivalent | Description |
|---------------|-------------------|-------------|
| `order` | `class` | Class definition |
| `ability` | `def` | Function definition |
| `holocron` | variable | Variable declaration |
| `kyber` | constant | Constant declaration |
| `respond` | `print` | Output statement |
| `sense` | `if` | Conditional statement |
| `meditate` | `while` | While loop |
| `train` | `for` | For loop |
| `new` | instantiation | Create new object |

### Advanced Data Structures
| Force Keyword | Python Equivalent | Description |
|---------------|-------------------|-------------|
| `squadron` | `list` | Array/List literal |
| `datapad` | `dict` | Dictionary/Object literal |
| `rebellion` | `set` | Set literal |
| `stack_tower` | Stack class | Stack data structure |
| `queue_line` | Queue class | Queue data structure |
| `tuple_coordinates` | `tuple` | Tuple data structure |

### Advanced Features
| Force Keyword | Python Equivalent | Description |
|---------------|-------------------|-------------|
| `protocol_droid` | text functions | Text processing operations |
| `hologram_text` | f-strings | String formatting |
| `regex_pattern` | regex operations | Regular expressions |
| `galactic_time` | datetime functions | Date/time operations |
| `data_stream` | JSON operations | JSON processing |
| `force_encrypt` | encryption | Encryption functions |
| `force_hash` | hash functions | Hash operations |
| `jedi_mind_trick` | ternary operator | Conditional expressions |
| `jedi_council` | switch-case | Multi-way branching |

### Mathematical & Utility Operations
| Force Keyword | Python Equivalent | Description |
|---------------|-------------------|-------------|
| `midichlorians` | random functions | Random number generation |
| `lightsaber_distance` | distance calc | Calculate distance/length |
| `force_calculate` | math operations | Mathematical calculations |
| `hyperdrive` | generators | Create generators/iterators |

### File & Network Operations
| Force Keyword | Python Equivalent | Description |
|---------------|-------------------|-------------|
| `holocron_archive` | file reading | Read file contents |
| `imperial_database` | file writing | Write content to file |
| `hyperspace_comm` | HTTP requests | Network operations |

## Variables & Constants

```force
holocron x = 5     // variable
kyber PI = 3.14    // constant

respond x + PI
```

## Classes & Objects

```force
order Jedi {
  initiate(self, name) {
    self.name = name
    self.power = 50
  }
  
  ability train(self) {
    self.power = self.power + 10
    respond self.name + " gains power: " + str(self.power)
  }
  
  ability use_force(self, target) {
    respond self.name + " uses the Force on " + target
  }
}

// Instantiate and use
holocron luke = new Jedi("Luke Skywalker")
luke.train()
luke.use_force("Training Remote")
```

## Functions

```force
ability greet_jedi(name, rank) {
  respond hologram_text("Greetings, {} {}!", rank, name)
  respond "May the Force be with you!"
}

greet_jedi("Obi-Wan", "Master")
```

## Control Flow

### Conditionals
```force
holocron force_level = 75

sense (force_level > 50) {
  respond "Strong with the Force, you are!"
} else {
  respond "More training, you need."
}
```

### Loops
```force
// While loop
holocron power = 0
meditate (power < 100) {
  power = power + 10
  respond "Training... Power: " + str(power)
}

// For loop
train (holocron i = 0; i < 5; i = i + 1) {
  respond "Training session: " + str(i + 1)
}
```

## Data Structures

### Arrays/Lists
```force
holocron jedis = squadron["Yoda", "Obi-Wan", "Luke", "Rey"]
respond "First Jedi: " + jedis[0]
respond "Jedi count: " + str(len(jedis))
```

### Dictionaries/Objects
```force
holocron jedi_info = datapad {
  name: "Yoda",
  species: "Unknown",
  age: 900,
  lightsaber: "Green"
}

respond "Master: " + jedi_info["name"]
respond "Age: " + str(jedi_info["age"]) + " years"
```

### Advanced Data Structures
```force
// Stack (Last In, First Out)
holocron jedi_council = stack_tower(squadron["Yoda", "Mace Windu"])
jedi_council.push("Obi-Wan")
respond "Council head: " + jedi_council.peek()
respond "Removed: " + jedi_council.pop()

// Queue (First In, First Out)  
holocron training_queue = queue_line(squadron["Luke", "Leia"])
training_queue.enqueue("Han")
respond "Next trainee: " + training_queue.front()
respond "Now training: " + training_queue.dequeue()
```

## String Processing & Text Operations

```force
holocron message = "The Force will be with you, always"

// Basic text operations
respond protocol_droid("uppercase", message)
respond protocol_droid("reverse", message)  
respond "Length: " + protocol_droid("length", message)

// String formatting
holocron name = "Padawan"
respond hologram_text("Welcome, {}! Ready for training?", name)

// Regular expressions
respond "Contains 'Force': " + str(regex_pattern("search", "Force", message))
holocron words = regex_pattern("findall", "\\w+", message)
respond "Word count: " + str(len(words))
```

## Date & Time Operations

```force
// Get current time
holocron current_time = galactic_time("now")
respond "Current time: " + current_time

// Get timestamp
holocron timestamp = galactic_time("timestamp") 
respond "Timestamp: " + str(timestamp)
```

## JSON Processing

```force
// Create data structure
holocron jedi_data = datapad {
  name: "Luke Skywalker",
  rank: "Jedi Knight", 
  homeworld: "Tatooine"
}

// Convert to JSON
holocron json_string = data_stream("stringify", jedi_data)
respond "JSON: " + json_string

// Parse JSON back
holocron parsed = data_stream("parse", json_string)
respond "Name: " + parsed["name"]
```

## Security & Encryption

```force
holocron secret = "The Death Star plans"

// Base64 encoding
holocron encoded = force_encrypt("base64_encode", secret)
respond "Encoded: " + encoded

// Decoding
holocron decoded = force_encrypt("base64_decode", encoded)
respond "Decoded: " + decoded

// Hash functions
holocron hash_value = force_hash("sha256", secret)
respond "SHA256: " + hash_value
```

## Advanced Control Flow

### Ternary Operator (Jedi Mind Trick)
```force
holocron power = 75
holocron status = jedi_mind_trick(power > 50, "Jedi", "Padawan")
respond "Status: " + status
```

### Switch-Case Logic (Jedi Council)
```force
ability council_decision(threat_level) {
  holocron decisions = datapad {
    "low": "Send a Padawan",
    "medium": "Send a Jedi Knight", 
    "high": "Send a Master",
    "extreme": "Send multiple Masters"
  }
  
  holocron decision = jedi_council(threat_level, decisions, "Meditate on this")
  respond "Council decides: " + decision
}

council_decision("high")
```

## Error Handling

The Force provides themed error messages to help guide your journey:

- **Syntax Errors**: "The dark side clouds your syntax"
- **Runtime Errors**: "A disturbance in the Force detected"
- **Logic Errors**: "Your Jedi training is incomplete"

## Best Practices

### Code Style
- Use meaningful variable names that fit the Star Wars theme
- Comment your code with `//` for single lines or `/* */` for blocks
- Organize classes and functions logically
- Use proper indentation for code blocks

### Performance Tips
- Use appropriate data structures for your needs
- Avoid deeply nested loops when possible
- Cache frequently used calculations in variables
- Use generators with `hyperdrive` for large datasets

### Security Considerations
- Always validate user input
- Use `force_encrypt` and `force_hash` for sensitive data
- Be careful with file operations using `holocron_archive` and `imperial_database`
- Sanitize data when using `hyperspace_comm` for network requests

## Type System

The Force is dynamically typed like Python, but uses themed keywords:

- **Numbers**: Integer and float values
- **Strings**: Text enclosed in quotes
- **Arrays**: Use `squadron` for ordered collections
- **Dictionaries**: Use `datapad` for key-value pairs
- **Sets**: Use `rebellion` for unique collections
- **Booleans**: `true` and `false`

## Standard Library

The Force includes several built-in modules:

- **Text Processing**: `protocol_droid` functions
- **Date/Time**: `galactic_time` operations
- **JSON**: `data_stream` processing
- **Cryptography**: `force_encrypt` and `force_hash`
- **Regular Expressions**: `regex_pattern` matching
- **File I/O**: `holocron_archive` and `imperial_database`
- **HTTP**: `hyperspace_comm` requests

May the Force guide your coding adventures! 🌟