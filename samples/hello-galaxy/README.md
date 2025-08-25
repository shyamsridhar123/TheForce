# Hello Galaxy - Basic Force Programming

Welcome to your first Force program! This sample introduces you to the fundamental concepts of The Force Programming Language through a simple but complete example.

## Learning Objectives

By completing this sample, you will learn:
- Basic syntax and structure of Force programs
- Variable declaration using `holocron`
- Output using `respond`
- Simple control flow with `sense` (if statements)
- Basic string operations and concatenation
- How to run Force programs

## What This Program Does

This program demonstrates a simple greeting system that:
1. Declares variables to store names and messages
2. Responds with personalized greetings
3. Uses conditional logic to provide different responses
4. Shows basic string manipulation and formatting

## Code Explanation

### Variables (holocron)
```force
holocron jedi_name = "Luke Skywalker"
```
Variables in Force are declared using the `holocron` keyword, representing data storage like ancient Jedi knowledge crystals.

### Output (respond)
```force
respond "Hello, Galaxy!"
```
The `respond` keyword outputs text, like a Jedi communicating across the galaxy.

### Conditionals (sense)
```force
sense (force_level > 50) {
    respond "The Force is strong with this one!"
}
```
The `sense` keyword is used for conditional logic, representing a Jedi's ability to sense the Force.

## How to Run

1. Navigate to the hello-galaxy directory
2. Run the program using the Force compiler:
   ```bash
   python ../../force_compiler.py main.force
   ```

## Expected Output

```
A long time ago in a galaxy far, far away...
Hello, Galaxy!
May the Force be with you!
Welcome, Luke Skywalker
The Force is strong with this one!
Your Force level is: 75
Ready for Jedi training: Yes
```

## Try It Yourself

Experiment with the code by:
1. Changing the jedi_name variable to your own name
2. Modifying the force_level value to see different responses
3. Adding more conditional checks
4. Creating additional greeting messages

## Next Steps

Once you've mastered this basic example, try:
- [jedi-academy](../jedi-academy/) for object-oriented programming
- [navigation-system](../navigation-system/) for mathematical operations

May the Force guide your coding journey! ⭐