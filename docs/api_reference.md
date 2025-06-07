# API Reference - GPS Navigation System

## Overview

This document provides comprehensive API documentation for the GPS Navigation System built with Dijkstra's algorithm. The system provides both programmatic access and interactive interfaces for route planning and navigation.

## Table of Contents

1. [GPSNavigator Class](#gpsnavigator-class)
2. [Core Methods](#core-methods)
3. [Utility Methods](#utility-methods)
4. [Data Structures](#data-structures)
5. [Return Values](#return-values)
6. [Usage Examples](#usage-examples)
7. [Error Handling](#error-handling)
8. [Configuration](#configuration)

## GPSNavigator Class

### Constructor

```python
class GPSNavigator:
    def __init__(self)
```

Creates a new GPS Navigator instance with a pre-configured city map.

**Parameters:** None

**Initializes:**
- `self.graph`: Adjacency list representation of the road network
- `self.coordinates`: Node coordinates for visualization
- `self.node_names`: Mapping of node IDs to readable location names
- City map with 12 intersections and 22 bidirectional roads

**Example:**
```python
navigator = GPSNavigator()
```

## Core Methods

### dijkstra()

```python
def dijkstra(self, start, end, verbose=False)
```

Finds the shortest path between two locations using Dijkstra's algorithm.

**Parameters:**
- `start` (int): Starting node ID (0-11)
- `end` (int): Destination node ID (0-11)
- `verbose` (bool, optional): Enable step-by-step algorithm output. Default: False

**Returns:**
- `dict`: Route result containing path, distance, and execution details

**Raises:**
- No exceptions raised directly, but invalid nodes return unsuccessful result

**Time Complexity:** O((V + E) log V)
**Space Complexity:** O(V)

**Example:**
```python
result = navigator.dijkstra(start=0, end=11, verbose=True)
print(f"Distance: {result['distance']:.1f} km")
```

### add_road()

```python
def add_road(self, from_node, to_node, distance)
```

Adds a bidirectional road connection between two intersections.

**Parameters:**
- `from_node` (int): Source intersection ID
- `to_node` (int): Destination intersection ID
- `distance` (float): Road distance in kilometers

**Returns:** None

**Side Effects:** Modifies the internal graph structure

**Example:**
```python
navigator.add_road(0, 12, 5.5)  # Add new road: 5.5km
```

### setup_city_map()

```python
def setup_city_map(self)
```

Initializes the default city road network with 12 intersections.

**Parameters:** None

**Returns:** None

**Side Effects:** 
- Populates `self.graph` with road connections
- Sets up `self.coordinates` with intersection positions
- Initializes `self.node_names` with location names

**Note:** Called automatically during initialization

## Utility Methods

### calculate_route_time()

```python
def calculate_route_time(self, distance_km, avg_speed_kmh=30)
```

Calculates estimated travel time for a given distance.

**Parameters:**
- `distance_km` (float): Route distance in kilometers
- `avg_speed_kmh` (int, optional): Average driving speed. Default: 30 km/h

**Returns:**
- `float`: Estimated travel time in minutes

**Example:**
```python
time_minutes = navigator.calculate_route_time(8.4, avg_speed_kmh=45)
print(f"ETA: {time_minutes:.0f} minutes")
```

### get_turn_by_turn_directions()

```python
def get_turn_by_turn_directions(self, path)
```

Generates human-readable turn-by-turn navigation directions.

**Parameters:**
- `path` (list): List of node IDs representing the route

**Returns:**
- `list`: List of direction strings

**Example:**
```python
directions = navigator.get_turn_by_turn_directions([0, 3, 4, 10, 11])
for direction in directions:
    print(direction)
```

### print_route_summary()

```python
def print_route_summary(self, result, start, end)
```

Prints a comprehensive, formatted route summary to console.

**Parameters:**
- `result` (dict): Result dictionary from dijkstra() method
- `start` (int): Starting node ID
- `end` (int): Destination node ID

**Returns:** None

**Side Effects:** Prints formatted output to console

**Example:**
```python
result = navigator.dijkstra(0, 11)
navigator.print_route_summary(result, 0, 11)
```

### visualize_route()

```python
def visualize_route(self, result, start, end, show_algorithm_steps=False)
```

Creates a visual map showing the calculated route and algorithm execution.

**Parameters:**
- `result` (dict): Result dictionary from dijkstra() method
- `start` (int): Starting node ID
- `end` (int): Destination node ID
- `show_algorithm_steps` (bool, optional): Show algorithm execution steps. Default: False

**Returns:** None

**Side Effects:** 
- Opens matplotlib window with route visualization
- Displays interactive map with route highlighting

**Dependencies:** Requires `matplotlib`, `networkx`

**Example:**
```python
result = navigator.dijkstra(0, 11)
navigator.visualize_route(result, 0, 11, show_algorithm_steps=True)
```

### interactive_navigation()

```python
def interactive_navigation(self)
```

Launches an interactive command-line interface for GPS navigation.

**Parameters:** None

**Returns:** None

**Side Effects:** 
- Enters interactive loop
- Prompts user for input
- Displays route information and visualizations

**Exit Conditions:**
- User enters -1 for start location
- KeyboardInterrupt (Ctrl+C)

**Example:**
```python
navigator = GPSNavigator()
navigator.interactive_navigation()
```

## Data Structures

### Graph Representation

```python
# Internal graph structure
self.graph = {
    0: [(1, 2.1), (3, 1.2)],  # Node 0 connects to nodes 1 and 3
    1: [(0, 2.1), (2, 1.9)],  # Bidirectional connections
    # ... more connections
}
```

### Coordinates

```python
# Node coordinates for visualization
self.coordinates = {
    0: (1.0, 5.0),    # Main St & 1st Ave
    1: (3.0, 5.2),    # Park Rd & 2nd Ave
    # ... more coordinates
}
```

### Node Names

```python
# Human-readable location names
self.node_names = {
    0: "Main St & 1st Ave",
    1: "Park Rd & 2nd Ave",
    # ... more names
}
```

## Return Values

### dijkstra() Result Structure

```python
{
    'path': [0, 3, 4, 10, 11],           # List of node IDs in route order
    'distance': 8.4,                     # Total distance in kilometers
    'visited': [0, 3, 1, 4, 7, 10, 11], # Nodes explored during search
    'steps': [                           # Algorithm execution steps
        "Starting navigation from Main St & 1st Ave",
        "Destination: Mountain Rd & 3rd Ave",
        # ... more steps
    ],
    'success': True                      # Whether route was found
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `path` | `list[int]` | Ordered list of node IDs from start to destination |
| `distance` | `float` | Total route distance in kilometers |
| `visited` | `list[int]` | All nodes explored during algorithm execution |
| `steps` | `list[str]` | Human-readable algorithm execution trace |
| `success` | `bool` | True if valid route found, False otherwise |

### Error Conditions

When no route is found:
```python
{
    'path': [],
    'distance': float('infinity'),
    'visited': [0, 3, 1, 4],  # Nodes that were explored
    'steps': ["Starting navigation...", "No path found"],
    'success': False
}
```

## Usage Examples

### Basic Route Finding

```python
# Create navigator
navigator = GPSNavigator()

# Find route
result = navigator.dijkstra(start=0, end=11)

# Check if route found
if result['success']:
    print(f"Route found: {result['distance']:.1f} km")
    navigator.print_route_summary(result, 0, 11)
else:
    print("No route available")
```

### Verbose Algorithm Execution

```python
# Show step-by-step algorithm execution
result = navigator.dijkstra(start=0, end=11, verbose=True)

# Output:
# 🚀 Starting GPS navigation from Main St & 1st Ave to Mountain Rd & 3rd Ave
# 🔍 Exploring: Main St & 1st Ave (Distance: 0.0km)
#   ↳ Updated route to Park Rd & 2nd Ave: 2.1km
#   ↳ Updated route to Elm St & 1st Ave: 1.2km
# ...
```

### Custom Route Analysis

```python
# Find multiple routes for comparison
routes = [
    (0, 11, "Main to Mountain"),
    (1, 8, "Park to Hill"),
    (3, 10, "Elm to Lake")
]

for start, end, description in routes:
    result = navigator.dijkstra(start, end)
    if result['success']:
        time_est = navigator.calculate_route_time(result['distance'])
        print(f"{description}: {result['distance']:.1f}km, {time_est:.0f}min")
```

### Interactive Session

```python
# Launch interactive navigation
navigator = GPSNavigator()
navigator.interactive_navigation()

# User interaction:
# Enter start location ID (or -1 to quit): 0
# Enter destination ID: 11
# 🔄 Calculating route...
# 🎯 ROUTE FOUND!
# From: Main St & 1st Ave
# To: Mountain Rd & 3rd Ave
# Distance: 8.4 km
# ...
```

### Visualization with Algorithm Steps

```python
# Create detailed visualization
result = navigator.dijkstra(0, 11, verbose=True)
navigator.visualize_route(result, 0, 11, show_algorithm_steps=True)

# Shows:
# - Left panel: Route map with highlighted path
# - Right panel: Algorithm execution steps
```

## Error Handling

### Invalid Node IDs

```python
# Handle invalid node IDs
try:
    result = navigator.dijkstra(start=0, end=99)  # Node 99 doesn't exist
    if not result['success']:
        print("Route calculation failed")
except KeyError as e:
    print(f"Invalid node ID: {e}")
```

### No Path Available

```python
# Check for disconnected graph
result = navigator.dijkstra(start=0, end=99)
if not result['success']:
    print("No path exists between these locations")
    print(f"Explored {len(result['visited'])} intersections")
```

### Visualization Dependencies

```python
# Handle missing visualization libraries
try:
    navigator.visualize_route(result, 0, 11)
except ImportError as e:
    print(f"Visualization not available: {e}")
    print("Install required packages: pip install matplotlib networkx")
```

## Configuration

### Default Settings

```python
# Default city map settings
INTERSECTIONS = 12
ROADS = 22  # Bidirectional
AVERAGE_SPEED = 30  # km/h for time estimation
```

### Customizing the Map

```python
# Add custom intersections
navigator = GPSNavigator()

# Add new intersection (programmatically)
new_node_id = 12
navigator.node_names[new_node_id] = "Custom St & New Ave"
navigator.coordinates[new_node_id] = (6.0, 3.0)

# Connect to existing network
navigator.add_road(11, new_node_id, 2.5)  # 2.5km road
```

### Speed Customization

```python
# Custom travel time calculation
def calculate_rush_hour_time(distance_km):
    """Custom time calculation for rush hour traffic"""
    if distance_km < 2.0:
        speed = 15  # Slow local streets
    elif distance_km < 5.0:
        speed = 25  # Moderate arterial roads
    else:
        speed = 35  # Faster main roads
    
    return (distance_km / speed) * 60  # Convert to minutes

# Use custom function
result = navigator.dijkstra(0, 11)
custom_time = calculate_rush_hour_time(result['distance'])
print(f"Rush hour ETA: {custom_time:.0f} minutes")
```

## Performance Considerations

### Time Complexity

| Operation | Complexity | Notes |
|-----------|------------|-------|
| `dijkstra()` | O((V + E) log V) | V=nodes, E=edges |
| `add_road()` | O(1) | Constant time insertion |
| `visualize_route()` | O(V + E) | Graph rendering |
| `print_route_summary()` | O(V) | Path traversal |

### Memory Usage

| Component | Space | Notes |
|-----------|-------|-------|
| Graph storage | O(V + E) | Adjacency list |
| Algorithm execution | O(V) | Distance/previous arrays |
| Visualization | O(V + E) | NetworkX graph copy |

### Optimization Tips

```python
# For large graphs, consider:
# 1. Early termination when destination found
result = navigator.dijkstra(0, 11)  # Stops at destination

# 2. Disable verbose mode for performance
result = navigator.dijkstra(0, 11, verbose=False)

# 3. Reuse navigator instance
navigator = GPSNavigator()  # Create once
for start, end in route_pairs:
    result = navigator.dijkstra(start, end)  # Reuse
```

## Version Information

- **API Version**: 1.0
- **Python Compatibility**: 3.7+
- **Required Dependencies**: 
  - `heapq` (standard library)
  - `math` (standard library)
  - `matplotlib` (visualization)
  - `networkx` (graph visualization)
  - `collections` (standard library)
  - `time` (standard library)

## Support and Troubleshooting

### Common Issues

1. **Import Errors**: Ensure matplotlib and networkx are installed
2. **Visualization Not Showing**: Check if running in appropriate environment
3. **Memory Issues**: Disable visualization for large graphs
4. **Performance**: Use verbose=False for faster execution

### Debug Mode

```python
# Enable detailed logging
result = navigator.dijkstra(0, 11, verbose=True)
print(f"Algorithm steps: {len(result['steps'])}")
print(f"Nodes explored: {len(result['visited'])}")
print(f"Path length: {len(result['path'])}")
```

---

*This API reference provides complete documentation for integrating and extending the GPS Navigation System. For algorithm details, see [algorithm_explanation.md](algorithm_explanation.md).*
