# The Force Programming Examples

Learn The Force through practical examples that demonstrate key language features and programming concepts.

## Basic Examples

### Hello Galaxy
Your first Force program - a simple greeting:

```force
// Your first Force program
respond "Hello, Galaxy!"
respond "May the Force be with you!"

holocron jedi_name = "Luke Skywalker"
respond "Welcome, " + jedi_name
```

### Variables and Data Types
Working with different types of data:

```force
// Variables and constants
holocron name = "Yoda"
holocron age = 900
kyber PI = 3.14159

respond "Master " + name + " is " + str(age) + " years old"
respond "PI constant: " + str(PI)
```

## Object-Oriented Programming

### Basic Jedi Training Program
Learn classes and objects through Jedi training:

```force
order Jedi {
  initiate(self, name) {
    self.name = name
    self.power = 10
  }
  
  ability train(self) {
    self.power = self.power + 5
    respond self.name + " trains. Power: " + str(self.power)
  }
}

ability main() {
  holocron rey = new Jedi("Rey")
  train (holocron i = 0; i < 5; i = i + 1) {
    rey.train()
  }
  respond "Training complete!"
}

main()
```

### Advanced Class Example
A more complex class with multiple abilities:

```force
order Lightsaber {
  initiate(self, color, owner) {
    self.color = color
    self.owner = owner
    self.activated = false
  }
  
  ability activate(self) {
    self.activated = true
    respond self.owner + "'s " + self.color + " lightsaber ignites!"
  }
  
  ability deactivate(self) {
    self.activated = false
    respond "Lightsaber deactivated"
  }
  
  ability attack(self, target) {
    sense (self.activated) {
      respond self.owner + " attacks " + target + " with " + self.color + " blade!"
    } else {
      respond "Must activate lightsaber first!"
    }
  }
}

holocron luke_saber = new Lightsaber("green", "Luke")
luke_saber.activate()
luke_saber.attack("Training Dummy")
```

## Data Structures

### Arrays and Basic Collections
Working with squadrons (arrays) and data manipulation:

```force
ability squadron_mission() {
  holocron rebels = squadron["Luke", "Leia", "Han", "Chewbacca"]
  
  respond "Rebel Alliance members:"
  train (holocron i = 0; i < len(rebels); i = i + 1) {
    respond str(i + 1) + ". " + rebels[i]
  }
  
  // Add new member
  rebels.append("Lando")
  respond "New member joined: " + rebels[len(rebels) - 1]
}

squadron_mission()
```

### Dictionaries and Objects
Using datapads (dictionaries) for structured data:

```force
ability character_database() {
  holocron characters = datapad {
    "luke": datapad {
      "name": "Luke Skywalker",
      "homeworld": "Tatooine", 
      "species": "Human",
      "lightsaber": "Green"
    },
    "yoda": datapad {
      "name": "Yoda",
      "homeworld": "Dagobah",
      "species": "Unknown", 
      "lightsaber": "Green"
    }
  }
  
  respond "=== Character Database ==="
  holocron keys = list(characters.keys())
  train (holocron i = 0; i < len(keys); i = i + 1) {
    holocron key = keys[i]
    holocron character = characters[key]
    respond character["name"] + " from " + character["homeworld"]
  }
}

character_database()
```

### Advanced Data Structures Demo
Stacks and queues for complex data handling:

```force
ability demonstrate_structures() {
  // Stack operations - Last In, First Out
  holocron council = stack_tower(squadron["Yoda", "Mace Windu"])
  council.push("Obi-Wan")
  respond "Council size: " + str(council.size())
  respond "Council leader: " + council.peek()
  respond "Removing: " + council.pop()
  
  // Queue operations - First In, First Out
  holocron cantina = queue_line(squadron["Han", "Leia"]) 
  cantina.enqueue("Luke")
  respond "Next customer: " + cantina.front()
  respond "Serving: " + cantina.dequeue()
  
  // Tuple coordinates
  holocron death_star_location = tuple_coordinates(152.7, -89.3, 1024.5)
  respond "Death Star coordinates: " + str(death_star_location)
}

demonstrate_structures()
```

## Text Processing

### String Manipulation with Protocol Droids
Advanced text processing capabilities:

```force
ability text_processing_demo() {
  holocron message = "The Force will be with you, always"
  
  respond "Original: " + message
  respond "Uppercase: " + protocol_droid("uppercase", message)
  respond "Reversed: " + protocol_droid("reverse", message)
  respond "Length: " + str(protocol_droid("length", message))
  
  // String formatting
  holocron name = "Young Padawan"
  holocron formatted = hologram_text("Welcome, {}! Your training begins now.", name)
  respond formatted
  
  // Regular expressions
  respond "Contains 'Force': " + str(regex_pattern("search", "Force", message))
  holocron words = regex_pattern("findall", "\\w+", message)
  respond "Word count: " + str(len(words))
}

text_processing_demo()
```

## Date and Time Operations

### Galactic Time Management
Working with dates and timestamps:

```force
ability datetime_operations() {
  respond "=== Galactic Time Operations ==="
  
  // Get current time
  holocron current_time = galactic_time("now")
  respond "Current time: " + current_time
  
  // Get timestamp
  holocron timestamp = galactic_time("timestamp")
  respond "Timestamp: " + str(timestamp)
  
  // Time-based mission planning
  respond "Mission scheduled for timestamp: " + str(timestamp + 3600)
}

datetime_operations()
```

## Security and Encryption

### Security & Encryption Example
Protecting sensitive rebel intelligence:

```force
ability secure_transmission(message) {
  respond "=== Secure Transmission Protocol ==="
  respond "Original: " + message
  
  // Base64 encoding
  holocron encoded = force_encrypt("base64_encode", message)
  respond "Encrypted: " + encoded
  
  // Hash for integrity verification
  holocron signature = force_hash("sha256", message)
  respond "Signature: " + signature[:16] + "..."
  
  // Decryption
  holocron decoded = force_encrypt("base64_decode", encoded)
  respond "Decrypted: " + decoded
  
  // Verify integrity
  holocron verify_signature = force_hash("sha256", decoded)
  sense (signature == verify_signature) {
    respond "✓ Message integrity verified"
  } else {
    respond "✗ Message integrity compromised!"
  }
}

secure_transmission("The Death Star plans are ready")
```

## JSON Processing

### Data Stream Operations
Working with structured data using JSON:

```force
ability json_processing_demo() {
  respond "=== JSON Data Processing ==="
  
  // Create structured data
  holocron mission_data = datapad {
    "mission": "Destroy Death Star",
    "team": squadron["Luke", "Leia", "Han"],
    "equipment": datapad {
      "ships": 3,
      "lightsabers": 1,
      "blasters": 2
    },
    "priority": "CRITICAL"
  }
  
  // Convert to JSON
  holocron json_string = data_stream("stringify", mission_data)
  respond "Mission data (JSON):"
  respond json_string
  
  // Parse JSON back
  holocron parsed = data_stream("parse", json_string)
  respond "\nMission: " + parsed["mission"]
  respond "Team leader: " + parsed["team"][0]
  respond "Ships available: " + str(parsed["equipment"]["ships"])
}

json_processing_demo()
```

## Advanced Control Flow

### Conditional Logic and Decision Making
Advanced decision-making patterns:

```force
ability jedi_council_meeting() {
  holocron threat_levels = squadron["low", "medium", "high", "extreme"]
  
  train (holocron i = 0; i < len(threat_levels); i = i + 1) {
    holocron level = threat_levels[i]
    
    // Ternary operations
    holocron urgency = jedi_mind_trick(level == "extreme", "IMMEDIATE", "STANDARD")
    
    // Switch-case logic
    holocron decisions = datapad {
      "low": "Send a Padawan",
      "medium": "Send a Jedi Knight",
      "high": "Send a Master", 
      "extreme": "Send multiple Masters"
    }
    
    holocron decision = jedi_council("threat_" + level, decisions, "Meditate on this")
    respond "Threat: " + level + " | Decision: " + decision + " | Urgency: " + urgency
  }
}

jedi_council_meeting()
```

## Mathematical Operations

### Force Calculations and Random Events
Mathematical operations and randomness:

```force
ability force_mathematics() {
  respond "=== Force Mathematics ==="
  
  // Random midichlorian count
  holocron midichlorian_count = midichlorians("randint", 1000, 20000)
  respond "Midichlorian count: " + str(midichlorian_count)
  
  // Distance calculations
  holocron distance = lightsaber_distance("distance", 
    tuple_coordinates(0, 0), 
    tuple_coordinates(3, 4)
  )
  respond "Distance to target: " + str(distance) + " parsecs"
  
  // Force calculations
  holocron power_level = force_calculate("sqrt", midichlorian_count)
  respond "Force power level: " + str(int(power_level))
}

force_mathematics()
```

## File Operations

### Holocron Archives and Imperial Databases
Working with files in the Force universe:

```force
ability file_operations_demo() {
  respond "=== Holocron Archive Operations ==="
  
  holocron jedi_wisdom = "Do or do not, there is no try - Master Yoda"
  
  // Write to imperial database (file)
  imperial_database("jedi_wisdom.txt", jedi_wisdom)
  respond "Wisdom stored in holocron archive"
  
  // Read from holocron archive (file)
  holocron retrieved_wisdom = holocron_archive("jedi_wisdom.txt")
  respond "Retrieved wisdom: " + retrieved_wisdom
}

// Note: This example requires file system access
// file_operations_demo()
```

## Error Handling

### Dealing with Disturbances in the Force
Proper error handling techniques:

```force
ability error_handling_example() {
  respond "=== Error Handling Demo ==="
  
  // Example of potential error conditions
  holocron test_data = squadron[1, 2, 3]
  
  // Safe array access
  sense (len(test_data) > 5) {
    respond "Element: " + str(test_data[5])
  } else {
    respond "Array too small, cannot access element 5"
  }
  
  // Safe division
  holocron divisor = 0
  sense (divisor != 0) {
    respond "Result: " + str(10 / divisor)
  } else {
    respond "Cannot divide by zero - the Force prevents this!"
  }
}

error_handling_example()
```

## Running the Examples

### In the Web Interface
1. Start the Force web server: `python force_web_server.py`
2. Open your browser to `http://localhost:8000`
3. Click on the example buttons to load pre-built examples
4. Modify the code and click "Run" to see results

### From Command Line
Save any example to a `.force` file and run:
```bash
python force_compiler.py example_name.force
```

### Interactive Mode
Experiment with code snippets in interactive mode:
```bash
python force_compiler.py --interactive
```

## Building Your Own Programs

Use these examples as starting points for your own Force programs:

1. **Start Simple**: Begin with variables and basic output
2. **Add Structure**: Use functions (`ability`) to organize code
3. **Embrace Objects**: Create classes (`order`) for complex entities
4. **Use Data Structures**: Leverage arrays, dictionaries, and advanced structures
5. **Add Polish**: Include error handling and user-friendly output

May the Force guide your coding journey! 🌟