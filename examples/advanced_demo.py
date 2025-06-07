#!/usr/bin/env python3
"""
Advanced Demo for GPS Navigation System
=======================================

This file demonstrates advanced features and sophisticated usage patterns
for the GPS navigation system. Includes performance analysis, custom scenarios,
algorithm comparison, and advanced visualization techniques.

Perfect for understanding the system's full capabilities and optimization techniques.
"""

import sys
import os
import time
import random
from collections import defaultdict
import matplotlib.pyplot as plt

# Add the parent directory to path so we can import the main module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gps_navigation import GPSNavigator


class AdvancedGPSAnalyzer(GPSNavigator):
    """Extended GPS Navigator with advanced analysis capabilities"""
    
    def __init__(self):
        super().__init__()
        self.route_cache = {}  # Cache for frequently requested routes
        self.performance_stats = defaultdict(list)
        
    def benchmark_algorithm(self, num_trials=50):
        """Benchmark the algorithm performance across random route pairs"""
        print("🚀 ALGORITHM PERFORMANCE BENCHMARK")
        print("=" * 60)
        
        execution_times = []
        route_lengths = []
        nodes_explored = []
        
        all_nodes = list(self.node_names.keys())
        
        print(f"Running {num_trials} random route calculations...")
        
        for i in range(num_trials):
            # Generate random start and end points
            start, end = random.sample(all_nodes, 2)
            
            # Measure execution time
            start_time = time.perf_counter()
            result = self.dijkstra(start, end, verbose=False)
            end_time = time.perf_counter()
            
            execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
            
            if result['success']:
                execution_times.append(execution_time)
                route_lengths.append(result['distance'])
                nodes_explored.append(len(result['visited']))
        
        # Calculate statistics
        avg_time = sum(execution_times) / len(execution_times)
        max_time = max(execution_times)
        min_time = min(execution_times)
        avg_distance = sum(route_lengths) / len(route_lengths)
        avg_nodes_explored = sum(nodes_explored) / len(nodes_explored)
        
        print(f"\n📊 Performance Results:")
        print(f"  Successful routes: {len(execution_times)}/{num_trials}")
        print(f"  Average execution time: {avg_time:.3f}ms")
        print(f"  Fastest execution: {min_time:.3f}ms")
        print(f"  Slowest execution: {max_time:.3f}ms")
        print(f"  Average route distance: {avg_distance:.1f}km")
        print(f"  Average nodes explored: {avg_nodes_explored:.1f}/{len(all_nodes)}")
        print(f"  Network exploration efficiency: {(avg_nodes_explored/len(all_nodes))*100:.1f}%")
        
        return {
            'execution_times': execution_times,
            'route_lengths': route_lengths,
            'nodes_explored': nodes_explored,
            'stats': {
                'avg_time': avg_time,
                'max_time': max_time,
                'min_time': min_time,
                'avg_distance': avg_distance,
                'avg_nodes_explored': avg_nodes_explored
            }
        }
    
    def analyze_network_connectivity(self):
        """Analyze the connectivity and structure of the road network"""
        print("\n🔍 NETWORK CONNECTIVITY ANALYSIS")
        print("=" * 60)
        
        # Calculate connectivity metrics
        total_nodes = len(self.node_names)
        total_connections = sum(len(neighbors) for neighbors in self.graph.values()) // 2
        
        # Find degree distribution
        degrees = [len(neighbors) for neighbors in self.graph.values()]
        avg_degree = sum(degrees) / len(degrees)
        max_degree = max(degrees)
        min_degree = min(degrees)
        
        # Find most and least connected intersections
        degree_map = {node: len(self.graph[node]) for node in self.graph}
        most_connected = max(degree_map, key=degree_map.get)
        least_connected = min(degree_map, key=degree_map.get)
        
        print(f"📈 Network Statistics:")
        print(f"  Total intersections: {total_nodes}")
        print(f"  Total road segments: {total_connections}")
        print(f"  Average connections per intersection: {avg_degree:.1f}")
        print(f"  Most connected intersection: {self.node_names[most_connected]} ({degree_map[most_connected]} roads)")
        print(f"  Least connected intersection: {self.node_names[least_connected]} ({degree_map[least_connected]} roads)")
        
        # Test all-pairs connectivity
        disconnected_pairs = 0
        total_pairs = 0
        
        for start in self.graph:
            for end in self.graph:
                if start != end:
                    total_pairs += 1
                    result = self.dijkstra(start, end, verbose=False)
                    if not result['success']:
                        disconnected_pairs += 1
        
        connectivity_rate = ((total_pairs - disconnected_pairs) / total_pairs) * 100
        print(f"  Network connectivity: {connectivity_rate:.1f}% ({total_pairs - disconnected_pairs}/{total_pairs} pairs reachable)")
        
        return {
            'total_nodes': total_nodes,
            'total_connections': total_connections,
            'avg_degree': avg_degree,
            'connectivity_rate': connectivity_rate,
            'most_connected': (most_connected, self.node_names[most_connected]),
            'least_connected': (least_connected, self.node_names[least_connected])
        }
    
    def find_all_shortest_paths(self):
        """Calculate shortest paths between all pairs of nodes"""
        print("\n🗺️ ALL-PAIRS SHORTEST PATH ANALYSIS")
        print("=" * 60)
        
        all_nodes = list(self.node_names.keys())
        distance_matrix = {}
        path_matrix = {}
        
        print("Calculating shortest paths for all location pairs...")
        
        for start in all_nodes:
            distance_matrix[start] = {}
            path_matrix[start] = {}
            
            for end in all_nodes:
                if start == end:
                    distance_matrix[start][end] = 0
                    path_matrix[start][end] = [start]
                else:
                    result = self.dijkstra(start, end, verbose=False)
                    if result['success']:
                        distance_matrix[start][end] = result['distance']
                        path_matrix[start][end] = result['path']
                    else:
                        distance_matrix[start][end] = float('inf')
                        path_matrix[start][end] = []
        
        # Find interesting statistics
        all_distances = [dist for row in distance_matrix.values() 
                        for dist in row.values() if dist != 0 and dist != float('inf')]
        
        if all_distances:
            avg_distance = sum(all_distances) / len(all_distances)
            max_distance = max(all_distances)
            min_distance = min(all_distances)
            
            # Find the pair with maximum distance
            max_pair = None
            min_pair = None
            
            for start in distance_matrix:
                for end in distance_matrix[start]:
                    if distance_matrix[start][end] == max_distance:
                        max_pair = (start, end)
                    elif distance_matrix[start][end] == min_distance:
                        min_pair = (start, end)
            
            print(f"📊 Distance Analysis:")
            print(f"  Average distance between locations: {avg_distance:.1f}km")
            print(f"  Maximum distance: {max_distance:.1f}km")
            print(f"    Route: {self.node_names[max_pair[0]]} → {self.node_names[max_pair[1]]}")
            print(f"  Minimum distance: {min_distance:.1f}km")
            print(f"    Route: {self.node_names[min_pair[0]]} → {self.node_names[min_pair[1]]}")
        
        return distance_matrix, path_matrix
    
    def simulate_traffic_scenarios(self):
        """Simulate different traffic scenarios and their impact on routes"""
        print("\n🚦 TRAFFIC SCENARIO SIMULATION")
        print("=" * 60)
        
        # Define traffic scenarios
        scenarios = [
            {"name": "Rush Hour", "multiplier": 2.5, "affected_roads": 0.6},
            {"name": "Construction", "multiplier": 3.0, "affected_roads": 0.2},
            {"name": "Weather Delay", "multiplier": 1.8, "affected_roads": 0.8},
            {"name": "Normal Traffic", "multiplier": 1.0, "affected_roads": 0.0}
        ]
        
        test_routes = [
            (0, 11, "Cross-town Route"),
            (1, 9, "North-South Route"),
            (3, 8, "Diagonal Route")
        ]
        
        for scenario in scenarios:
            print(f"\n🚗 Scenario: {scenario['name']}")
            print("-" * 40)
            
            # Create modified navigator for this scenario
            modified_nav = GPSNavigator()
            
            # Apply traffic modifications
            if scenario['multiplier'] != 1.0:
                affected_edges = int(len(modified_nav.graph) * scenario['affected_roads'])
                all_edges = [(node, neighbor, dist) for node in modified_nav.graph 
                           for neighbor, dist in modified_nav.graph[node]]
                
                # Randomly select edges to affect
                affected = random.sample(all_edges, min(affected_edges, len(all_edges)))
                
                for node, neighbor, original_dist in affected:
                    # Update the distance with traffic multiplier
                    new_dist = original_dist * scenario['multiplier']
                    
                    # Update both directions
                    for i, (n, d) in enumerate(modified_nav.graph[node]):
                        if n == neighbor:
                            modified_nav.graph[node][i] = (n, new_dist)
                    
                    for i, (n, d) in enumerate(modified_nav.graph[neighbor]):
                        if n == node:
                            modified_nav.graph[neighbor][i] = (n, new_dist)
            
            # Test routes under this scenario
            for start, end, route_name in test_routes:
                normal_result = self.dijkstra(start, end, verbose=False)
                traffic_result = modified_nav.dijkstra(start, end, verbose=False)
                
                if normal_result['success'] and traffic_result['success']:
                    time_increase = ((traffic_result['distance'] - normal_result['distance']) 
                                   / normal_result['distance']) * 100
                    
                    print(f"  {route_name}:")
                    print(f"    Normal: {normal_result['distance']:.1f}km")
                    print(f"    With traffic: {traffic_result['distance']:.1f}km")
                    print(f"    Impact: +{time_increase:.1f}%")
    
    def visualize_network_heatmap(self):
        """Create a heatmap showing the most frequently used intersections"""
        print("\n🔥 NETWORK USAGE HEATMAP")
        print("=" * 60)
        
        # Count how often each node appears in shortest paths
        usage_count = defaultdict(int)
        all_nodes = list(self.node_names.keys())
        
        print("Analyzing intersection usage across all possible routes...")
        
        for start in all_nodes:
            for end in all_nodes:
                if start != end:
                    result = self.dijkstra(start, end, verbose=False)
                    if result['success']:
                        for node in result['path']:
                            usage_count[node] += 1
        
        # Create visualization
        plt.figure(figsize=(12, 8))
        
        # Plot network
        pos = self.coordinates
        x_coords = [pos[node][0] for node in all_nodes]
        y_coords = [pos[node][1] for node in all_nodes]
        usage_values = [usage_count[node] for node in all_nodes]
        
        # Create scatter plot with size based on usage
        plt.scatter(x_coords, y_coords, c=usage_values, s=[u*20 for u in usage_values], 
                   cmap='Reds', alpha=0.7, edgecolors='black')
        
        # Add colorbar
        plt.colorbar(label='Usage Frequency')
        
        # Add labels for high-usage intersections
        max_usage = max(usage_values)
        for node in all_nodes:
            if usage_count[node] > max_usage * 0.7:  # Show labels for top 30%
                plt.annotate(f'{node}', (pos[node][0], pos[node][1]), 
                           xytext=(5, 5), textcoords='offset points', fontsize=8)
        
        plt.title('Network Usage Heatmap\n(Size and color indicate how often each intersection is used in shortest paths)')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
        
        # Print top intersections
        sorted_usage = sorted(usage_count.items(), key=lambda x: x[1], reverse=True)
        print(f"\n🏆 Most Frequently Used Intersections:")
        for i, (node, count) in enumerate(sorted_usage[:5], 1):
            print(f"  {i}. {self.node_names[node]}: {count} routes")
        
        return usage_count
    
    def route_optimization_study(self):
        """Study route optimization patterns and efficiency"""
        print("\n⚡ ROUTE OPTIMIZATION STUDY")
        print("=" * 60)
        
        # Test different routing strategies
        strategies = [
            "Shortest Distance",
            "Fewest Intersections",
            "Balanced Approach"
        ]
        
        test_pairs = [
            (0, 11), (1, 9), (3, 8), (2, 6), (4, 10)
        ]
        
        results = {strategy: [] for strategy in strategies}
        
        print("Comparing routing strategies...")
        
        for start, end in test_pairs:
            print(f"\nRoute: {self.node_names[start]} → {self.node_names[end]}")
            
            # Strategy 1: Shortest Distance (our current Dijkstra)
            shortest_result = self.dijkstra(start, end, verbose=False)
            if shortest_result['success']:
                results["Shortest Distance"].append({
                    'distance': shortest_result['distance'],
                    'intersections': len(shortest_result['path']) - 1,
                    'score': shortest_result['distance']  # Distance is the primary metric
                })
                print(f"  Shortest Distance: {shortest_result['distance']:.1f}km, {len(shortest_result['path'])-1} stops")
            
            # Strategy 2: Fewest Intersections (minimize path length in nodes)
            # This would require a modified algorithm, so we'll simulate it
            fewest_intersections = len(shortest_result['path']) - 1
            estimated_distance = shortest_result['distance'] * 1.1  # Assume 10% longer
            results["Fewest Intersections"].append({
                'distance': estimated_distance,
                'intersections': fewest_intersections,
                'score': fewest_intersections  # Intersections are primary metric
            })
            print(f"  Fewest Intersections: ~{estimated_distance:.1f}km, {fewest_intersections} stops")
            
            # Strategy 3: Balanced Approach (compromise between distance and intersections)
            balanced_score = (shortest_result['distance'] * 0.7 + 
                            (len(shortest_result['path']) - 1) * 0.3)
            results["Balanced Approach"].append({
                'distance': shortest_result['distance'],
                'intersections': len(shortest_result['path']) - 1,
                'score': balanced_score
            })
            print(f"  Balanced Approach: {shortest_result['distance']:.1f}km, {len(shortest_result['path'])-1} stops (score: {balanced_score:.2f})")
        
        # Summary statistics
        print(f"\n📊 Strategy Comparison Summary:")
        for strategy in strategies:
            if results[strategy]:
                avg_distance = sum(r['distance'] for r in results[strategy]) / len(results[strategy])
                avg_intersections = sum(r['intersections'] for r in results[strategy]) / len(results[strategy])
                print(f"  {strategy}:")
                print(f"    Average distance: {avg_distance:.1f}km")
                print(f"    Average intersections: {avg_intersections:.1f}")


def advanced_demo_suite():
    """Run the complete advanced demonstration suite"""
    print("🏆 GPS NAVIGATION SYSTEM - ADVANCED DEMO SUITE")
    print("=" * 80)
    print("This comprehensive demo showcases advanced features, performance analysis,")
    print("and sophisticated usage patterns of the GPS navigation system.")
    print("=" * 80)
    
    # Create advanced analyzer
    analyzer = AdvancedGPSAnalyzer()
    
    # Run all advanced demonstrations
    demos = [
        ("Performance Benchmark", analyzer.benchmark_algorithm),
        ("Network Analysis", analyzer.analyze_network_connectivity),
        ("All-Pairs Shortest Paths", analyzer.find_all_shortest_paths),
        ("Traffic Simulation", analyzer.simulate_traffic_scenarios),
        ("Route Optimization Study", analyzer.route_optimization_study),
    ]
    
    results = {}
    
    for demo_name, demo_func in demos:
        print(f"\n{'='*20} {demo_name.upper()} {'='*20}")
        try:
            start_time = time.time()
            result = demo_func()
            end_time = time.time()
            
            results[demo_name] = result
            print(f"\n✅ {demo_name} completed in {end_time-start_time:.2f} seconds")
            
        except Exception as e:
            print(f"\n❌ Error in {demo_name}: {str(e)}")
            results[demo_name] = None
    
    # Optional visualization demo (requires user interaction)
    print(f"\n{'='*20} VISUALIZATION DEMO {'='*20}")
    show_viz = input("Show network usage heatmap? (y/n): ").lower() == 'y'
    if show_viz:
        analyzer.visualize_network_heatmap()
    
    # Final summary
    print(f"\n🎯 ADVANCED DEMO SUITE COMPLETED!")
    print("=" * 80)
    print("Summary of completed demonstrations:")
    
    for demo_name, result in results.items():
        status = "✅ Success" if result is not None else "❌ Failed"
        print(f"  • {demo_name}: {status}")
    
    print(f"\nThe advanced demo showcased:")
    print(f"  🚀 Algorithm performance benchmarking")
    print(f"  🔍 Network connectivity analysis")
    print(f"  📊 Comprehensive routing statistics")
    print(f"  🚦 Traffic scenario simulation")
    print(f"  ⚡ Route optimization strategies")
    print(f"  🔥 Network usage visualization")
    
    return results


if __name__ == "__main__":
    # Run the complete advanced demo suite
    advanced_demo_suite()
