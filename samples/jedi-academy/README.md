# Jedi Academy - Object-Oriented Programming

Welcome to the Jedi Academy! This sample demonstrates object-oriented programming concepts in The Force Programming Language through a comprehensive Jedi training simulation.

## Learning Objectives

By completing this sample, you will learn:
- Class definition using `order`
- Constructor methods using `initiate`
- Instance methods using `ability`
- Object instantiation and method calls
- Instance variables and encapsulation
- Inheritance concepts (basic)
- Object interaction and composition

## What This Program Does

This program simulates a Jedi Academy training system that:
1. Defines a `Jedi` class with properties like name, rank, and Force power
2. Implements training methods that increase abilities
3. Creates different types of Jedi with varying skills
4. Demonstrates Force powers and lightsaber combat
5. Shows progression from Padawan to Jedi Knight
6. Includes a `Master` class that can train other Jedi

## Code Structure

### Classes Defined
- **Jedi**: Base class for all Force users
- **Master**: Specialized Jedi who can train others
- **Academy**: Manages multiple Jedi and training programs

### Key Concepts Demonstrated
- **Constructors**: Using `initiate` to initialize objects
- **Methods**: Using `ability` to define class functionality
- **Instance Variables**: Storing object state
- **Method Chaining**: Objects calling methods on other objects
- **Encapsulation**: Bundling data and methods together

## How to Run

1. Navigate to the jedi-academy directory
2. Run the program using the Force compiler:
   ```bash
   python ../../force_compiler.py main.force
   ```

## Expected Output

```
=== Welcome to the Jedi Academy ===

Creating new Jedi...
Luke Skywalker joins as Padawan (Force: 50)
Obi-Wan Kenobi joins as Master (Force: 95)

Training Session 1:
Luke Skywalker trains basic Force techniques (Force: 60)
Luke Skywalker trains lightsaber combat (Force: 70)

Master Obi-Wan teaches Luke:
Master Obi-Wan Kenobi is teaching Luke Skywalker
Luke Skywalker learns from the Master (Force: 85)

Luke has achieved Jedi Knight status!

Academy Status:
- Total Jedi: 2
- Masters: 1
- Knights: 1
- Padawans: 0
```

## Code Explanation

### Class Definition (order)
```force
order Jedi {
    initiate(self, name, rank) {
        self.name = name
        self.rank = rank
        self.force_power = 50
    }
}
```

### Method Definition (ability)
```force
ability train_force(self) {
    self.force_power = self.force_power + 10
    respond self.name + " trains Force techniques"
}
```

### Object Creation
```force
holocron luke = new Jedi("Luke Skywalker", "Padawan")
```

## Try It Yourself

Experiment with the code by:
1. Creating your own Jedi character
2. Adding new training methods
3. Implementing different Force powers
4. Creating specialized Jedi classes (Guardian, Consular, Sentinel)
5. Adding a Sith class as the dark side counterpart

## Next Steps

Once you've mastered object-oriented programming, try:
- [galactic-database](../galactic-database/) for advanced data structures
- [mission-control](../mission-control/) for complex applications

May the Force be with you, young programmer! ⚔️