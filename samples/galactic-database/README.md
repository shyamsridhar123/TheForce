# Galactic Database - Data Structures & Collections

Welcome to the Galactic Database! This sample demonstrates advanced data structure usage in The Force Programming Language through a comprehensive galactic information management system.

## Learning Objectives

By completing this sample, you will learn:
- Array operations using `squadron`
- Stack data structure using `stack_tower`
- Queue data structure using `queue_line`
- Dictionary operations using `datapad`
- Set operations using `rebellion`
- Data manipulation and filtering
- Complex data organization patterns

## What This Program Does

This program simulates a galactic database system that:
1. Manages star systems using arrays
2. Tracks Imperial fleets using stacks (LIFO - Last In, First Out)
3. Manages refugee evacuation queues (FIFO - First In, First Out)
4. Stores planetary data using dictionaries
5. Tracks rebel alliances using sets
6. Demonstrates various data operations and transformations

## Data Structures Explained

### Arrays (squadron)
```force
holocron planets = squadron["Tatooine", "Alderaan", "Coruscant"]
```
Arrays store ordered collections of items with indexed access.

### Stacks (stack_tower)
```force
holocron fleet_stack = stack_tower(squadron["Star Destroyer", "TIE Fighter"])
fleet_stack.push("Death Star")
```
Stacks follow Last-In-First-Out (LIFO) principle - like stacking plates.

### Queues (queue_line)
```force
holocron refugee_queue = queue_line(squadron["Family A", "Family B"])
refugee_queue.enqueue("Family C")
```
Queues follow First-In-First-Out (FIFO) principle - like waiting in line.

### Dictionaries (datapad)
```force
holocron planet_data = datapad{
    name: "Tatooine",
    population: 200000,
    climate: "arid"
}
```
Dictionaries store key-value pairs for structured data.

### Sets (rebellion)
```force
holocron allied_systems = rebellion["Alderaan", "Mon Calamari"]
```
Sets store unique items with no duplicates.

## How to Run

1. Navigate to the galactic-database directory
2. Run the program using the Force compiler:
   ```bash
   python ../../force_compiler.py main.force
   ```

## Expected Output

```
=== Galactic Database System ===

Star Systems Database:
- Tatooine: Desert world in Outer Rim
- Alderaan: Peaceful planet (destroyed)
- Coruscant: Galactic capital
- Naboo: Home of Senator Amidala

Imperial Fleet Management (Stack):
Fleet Stack Size: 3
Top Fleet Unit: Death Star
Deploying: Death Star
Current Top Unit: Star Destroyer

Refugee Evacuation Queue:
Queue Size: 3
Next Family: Skywalker Family
Processing: Skywalker Family
New Next: Organa Family

Planetary Information System:
Tatooine - Population: 200000, Climate: arid, Faction: neutral
Alderaan - Population: 0, Climate: temperate, Faction: destroyed

Rebel Alliance Systems:
Allied Systems: 3
Systems: Alderaan, Mon Calamari, Yavin 4
```

## Try It Yourself

Experiment with the code by:
1. Adding more star systems to the database
2. Creating additional fleet types in stacks
3. Managing different types of queues (supply lines, transport schedules)
4. Expanding planetary data with more attributes
5. Creating specialized data structures for different purposes

## Next Steps

Once you've mastered data structures, try:
- [rebel-communications](../rebel-communications/) for text processing
- [mission-control](../mission-control/) for complex applications

May the data be with you! 🌌