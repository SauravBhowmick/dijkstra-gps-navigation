#!/usr/bin/env python3
"""
Basic Usage Examples for GPS Navigation System
==============================================

This file demonstrates simple and common usage patterns for the GPS navigation
system using Dijkstra's algorithm. Perfect for beginners and quick reference.

Run this file to see basic navigation examples in action.
"""

import sys
import os

# Add the parent directory to path so we can import the main module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gps_navigation import GPSNavigator


def example_1_simple_route():
    """Example 1: Find a simple route between two locations"""
    print("=" * 60)
    print("EXAMPLE 1: Simple Route Finding")
    print("=" * 60)
    
    # Create navigator instance
    navigator = GPSNavigator()
    
    # Define start and end points
    start = 0  # Main St & 1st Ave
    end = 5    # Maple St & 3rd Ave
    
    print(f"Finding route from:")
    print(f"  Start: {navigator.node_names[start]}")
    print(f"  End: {navigator.node_names[end]}")
    
    # Find the route
    result = navigator.dijkstra(start, end)
    
    # Print basic results
    if result['success']:
        print(f"\n✅ Route found!")
        print(f"Distance: {result['distance']:.1f} km")
        print(f"Number of stops: {len(result['path']) - 1}")
        
        # Show the route
        route_names = [navigator.node_names[node] for node in result['path']]
        print(f"\nRoute: {' → '.join(route_names)}")
    else:
        print("❌ No route found!")


def example_2_with_directions():
    """Example 2: Get turn-by-turn directions"""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Turn-by-Turn Directions")
    print("=" * 60)
    
    navigator = GPSNavigator()
    
    start = 1   # Park Rd & 2nd Ave
    end = 11    # Mountain Rd & 3rd Ave
    
    print(f"Getting directions from {navigator.node_names[start]} to {navigator.node_names[end]}")
    
    # Find route
    result = navigator.dijkstra(start, end)
    
    if result['success']:
        # Get turn-by-turn directions
        directions = navigator.get_turn_by_turn_directions(result['path'])
        
        print(f"\n🧭 Turn-by-Turn Directions:")
        for direction in directions:
            print(f"  {direction}")
        
        # Calculate travel time
        travel_time = navigator.calculate_route_time(result['distance'])
        print(f"\n⏰ Estimated travel time: {travel_time:.0f} minutes")


def example_3_compare_routes():
    """Example 3: Compare multiple routes from the same starting point"""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Compare Multiple Routes")
    print("=" * 60)
    
    navigator = GPSNavigator()
    
    start = 0  # Main St & 1st Ave
    destinations = [6, 9, 11]  # Broadway & 1st Ave, River St & 1st Ave, Mountain Rd & 3rd Ave
    
    print(f"Comparing routes from {navigator.node_names[start]} to different destinations:")
    
    routes = []
    for end in destinations:
        result = navigator.dijkstra(start, end)
        if result['success']:
            routes.append({
                'destination': navigator.node_names[end],
                'distance': result['distance'],
                'time': navigator.calculate_route_time(result['distance']),
                'stops': len(result['path']) - 1
            })
    
    # Sort by distance
    routes.sort(key=lambda x: x['distance'])
    
    print(f"\n📊 Route Comparison (sorted by distance):")
    print(f"{'Destination':<25} {'Distance':<10} {'Time':<8} {'Stops'}")
    print("-" * 55)
    
    for route in routes:
        print(f"{route['destination']:<25} {route['distance']:<8.1f}km {route['time']:<6.0f}min {route['stops']} stops")


def example_4_detailed_analysis():
    """Example 4: Detailed route analysis with algorithm insights"""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Detailed Route Analysis")
    print("=" * 60)
    
    navigator = GPSNavigator()
    
    start = 3   # Elm St & 1st Ave  
    end = 8     # Hill Rd & 3rd Ave
    
    print(f"Detailed analysis for route:")
    print(f"  From: {navigator.node_names[start]}")
    print(f"  To: {navigator.node_names[end]}")
    
    # Find route with verbose output disabled for cleaner display
    result = navigator.dijkstra(start, end, verbose=False)
    
    if result['success']:
        print(f"\n📈 Algorithm Performance:")
        print(f"  Nodes explored: {len(result['visited'])}")
        print(f"  Total nodes in network: {len(navigator.node_names)}")
        print(f"  Efficiency: {(len(result['visited'])/len(navigator.node_names))*100:.1f}% of network explored")
        
        print(f"\n🛣️ Route Details:")
        print(f"  Total distance: {result['distance']:.1f} km")
        print(f"  Number of segments: {len(result['path']) - 1}")
        print(f"  Average segment length: {result['distance']/(len(result['path'])-1):.1f} km")
        
        # Show individual segments
        print(f"\n📍 Route Segments:")
        total_dist = 0
        for i in range(len(result['path']) - 1):
            current = result['path'][i]
            next_node = result['path'][i + 1]
            
            # Find distance between segments
            segment_distance = None
            for neighbor, dist in navigator.graph[current]:
                if neighbor == next_node:
                    segment_distance = dist
                    break
            
            total_dist += segment_distance
            print(f"  {i+1}. {navigator.node_names[current]} → {navigator.node_names[next_node]} ({segment_distance:.1f}km)")


def example_5_error_handling():
    """Example 5: Proper error handling and validation"""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Error Handling Examples")
    print("=" * 60)
    
    navigator = GPSNavigator()
    
    # Test cases that might cause issues
    test_cases = [
        (0, 0, "Same start and destination"),
        (0, 999, "Invalid destination"),
        (-1, 5, "Invalid start location"),
    ]
    
    for start, end, description in test_cases:
        print(f"\nTesting: {description}")
        print(f"  Route: {start} → {end}")
        
        try:
            # Check if nodes exist before calling dijkstra
            if start not in navigator.node_names:
                print(f"  ❌ Error: Start location {start} doesn't exist")
                continue
            
            if end not in navigator.node_names:
                print(f"  ❌ Error: End location {end} doesn't exist")
                continue
            
            if start == end:
                print(f"  ⚠️  Warning: Start and destination are the same")
                continue
            
            result = navigator.dijkstra(start, end)
            
            if result['success']:
                print(f"  ✅ Success: Route found ({result['distance']:.1f}km)")
            else:
                print(f"  ❌ No route available")
                
        except Exception as e:
            print(f"  ❌ Exception: {str(e)}")


def show_all_locations():
    """Helper function to display all available locations"""
    print("\n" + "=" * 60)
    print("AVAILABLE LOCATIONS")
    print("=" * 60)
    
    navigator = GPSNavigator()
    
    print("The following locations are available in the city network:")
    print()
    
    for node_id in sorted(navigator.node_names.keys()):
        name = navigator.node_names[node_id]
        coords = navigator.coordinates[node_id]
        print(f"  {node_id:2d}. {name:<25} (x={coords[0]:.1f}, y={coords[1]:.1f})")


def main():
    """Run all basic usage examples"""
    print("🗺️ GPS NAVIGATION SYSTEM - BASIC USAGE EXAMPLES")
    print("=" * 60)
    print("This script demonstrates common usage patterns for the GPS navigation system.")
    print("Each example shows different features and capabilities.")
    
    # Show available locations first
    show_all_locations()
    
    # Run all examples
    example_1_simple_route()
    example_2_with_directions()
    example_3_compare_routes()
    example_4_detailed_analysis()
    example_5_error_handling()
    
    print("\n" + "=" * 60)
    print("🎉 BASIC EXAMPLES COMPLETED!")
    print("=" * 60)
    print("Next steps:")
    print("  • Run 'python gps_navigation.py' for the full interactive demo")
    print("  • Check 'advanced_demo.py' for more complex examples")
    print("  • Use the GPSNavigator class in your own projects")


if __name__ == "__main__":
    main()