import heapq
import math
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict, deque
import time

class GPSNavigator:
    """
    GPS Navigation system using Dijkstra's algorithm to find shortest paths
    between locations on a road network.
    """
    
    def __init__(self):
        self.graph = defaultdict(list)  # Adjacency list: node -> [(neighbor, weight), ...]
        self.coordinates = {}  # Node coordinates for visualization
        self.node_names = {}   # Node ID to readable name mapping
        self.setup_city_map()
    
    def setup_city_map(self):
        """Initialize a realistic city road network with intersections and distances"""
        
        # Define intersection names and coordinates
        locations = [
            ("Main St & 1st Ave", (1, 5)),
            ("Park Rd & 2nd Ave", (3, 5.2)),
            ("Oak St & 3rd Ave", (5, 5.1)),
            ("Elm St & 1st Ave", (1.2, 4)),
            ("Pine St & 2nd Ave", (3.1, 3.8)),
            ("Maple St & 3rd Ave", (5.2, 4.1)),
            ("Broadway & 1st Ave", (1.1, 2.5)),
            ("Center St & 2nd Ave", (3.2, 2.3)),
            ("Hill Rd & 3rd Ave", (5.3, 2.6)),
            ("River St & 1st Ave", (1.3, 1)),
            ("Lake Ave & 2nd Ave", (3.5, 0.8)),
            ("Mountain Rd & 3rd Ave", (5.4, 1.1))
        ]
        
        # Store node information
        for i, (name, coords) in enumerate(locations):
            self.node_names[i] = name
            self.coordinates[i] = coords
        
        # Define road connections with realistic distances (in km)
        connections = [
            (0, 1, 2.1), (1, 2, 1.9), (0, 3, 1.2), (1, 4, 1.4),
            (2, 5, 1.3), (3, 4, 1.9), (4, 5, 2.1), (3, 6, 1.5),
            (4, 7, 1.7), (5, 8, 1.4), (6, 7, 1.8), (7, 8, 2.0),
            (6, 9, 1.6), (7, 10, 1.9), (8, 11, 1.5), (9, 10, 2.2),
            (10, 11, 1.8), (1, 7, 3.2), (4, 10, 3.5), (0, 6, 4.1),
            (2, 8, 3.8), (5, 11, 3.3)
        ]
        
        # Add edges to graph (bidirectional roads)
        for from_node, to_node, distance in connections:
            self.add_road(from_node, to_node, distance)
    
    def add_road(self, from_node, to_node, distance):
        """Add a bidirectional road between two intersections"""
        self.graph[from_node].append((to_node, distance))
        self.graph[to_node].append((from_node, distance))
    
    def dijkstra(self, start, end, verbose=False):
        """
        Find shortest path using Dijkstra's algorithm
        
        Args:
            start (int): Starting node ID
            end (int): Destination node ID
            verbose (bool): Print step-by-step execution
            
        Returns:
            dict: Contains path, distance, visited nodes, and algorithm steps
        """
        # Initialize data structures
        distances = {node: float('infinity') for node in self.graph}
        distances[start] = 0
        previous = {}
        visited = set()
        priority_queue = [(0, start)]  # (distance, node)
        steps = []
        
        if verbose:
            print(f"\n🚀 Starting GPS navigation from {self.node_names[start]} to {self.node_names[end]}")
            print("=" * 80)
        
        steps.append(f"Starting navigation from {self.node_names[start]}")
        steps.append(f"Destination: {self.node_names[end]}")
        steps.append(f"Initializing distances: Start=0km, Others=∞")
        
        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)
            
            # Skip if already processed
            if current_node in visited:
                continue
            
            visited.add(current_node)
            
            if verbose:
                print(f"\n🔍 Exploring: {self.node_names[current_node]} (Distance: {current_distance:.1f}km)")
            
            steps.append(f"Exploring {self.node_names[current_node]} (Distance: {current_distance:.1f}km)")
            
            # Found destination
            if current_node == end:
                steps.append(f"✅ Reached destination: {self.node_names[end]}")
                if verbose:
                    print(f"✅ Destination reached!")
                break
            
            # Explore neighbors
            for neighbor, road_distance in self.graph[current_node]:
                if neighbor not in visited:
                    new_distance = current_distance + road_distance
                    
                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        previous[neighbor] = current_node
                        heapq.heappush(priority_queue, (new_distance, neighbor))
                        
                        if verbose:
                            print(f"  ↳ Updated route to {self.node_names[neighbor]}: {new_distance:.1f}km")
                        
                        steps.append(f"  → Updated route to {self.node_names[neighbor]}: {new_distance:.1f}km")
        
        # Reconstruct path
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = previous.get(current)
        path.reverse()
        
        # Validate path
        if not path or path[0] != start:
            return {
                'path': [],
                'distance': float('infinity'),
                'visited': list(visited),
                'steps': steps,
                'success': False
            }
        
        return {
            'path': path,
            'distance': distances[end],
            'visited': list(visited),
            'steps': steps,
            'success': True
        }
    
    def calculate_route_time(self, distance_km, avg_speed_kmh=30):
        """Calculate estimated travel time"""
        return (distance_km / avg_speed_kmh) * 60  # Convert to minutes
    
    def get_turn_by_turn_directions(self, path):
        """Generate turn-by-turn navigation directions"""
        if len(path) < 2:
            return []
        
        directions = []
        total_distance = 0
        
        for i in range(len(path) - 1):
            current = path[i]
            next_node = path[i + 1]
            
            # Find distance between current and next node
            distance = None
            for neighbor, road_distance in self.graph[current]:
                if neighbor == next_node:
                    distance = road_distance
                    break
            
            total_distance += distance
            
            if i == 0:
                directions.append(f"1. Start at {self.node_names[current]}")
            
            direction_num = i + 2
            if i == len(path) - 2:  # Last step
                directions.append(f"{direction_num}. Arrive at {self.node_names[next_node]} ({distance:.1f}km)")
            else:
                directions.append(f"{direction_num}. Continue to {self.node_names[next_node]} ({distance:.1f}km)")
        
        return directions
    
    def print_route_summary(self, result, start, end):
        """Print a comprehensive route summary"""
        if not result['success']:
            print(f"\n❌ No route found from {self.node_names[start]} to {self.node_names[end]}")
            return
        
        print(f"\n🎯 ROUTE FOUND!")
        print("=" * 60)
        print(f"From: {self.node_names[start]}")
        print(f"To: {self.node_names[end]}")
        print(f"Distance: {result['distance']:.1f} km")
        print(f"Estimated Time: {self.calculate_route_time(result['distance']):.0f} minutes")
        print(f"Intersections Explored: {len(result['visited'])}")
        
        print(f"\n🛣️  ROUTE OVERVIEW:")
        route_names = [self.node_names[node] for node in result['path']]
        print(" → ".join(route_names))
        
        print(f"\n🧭 TURN-BY-TURN DIRECTIONS:")
        directions = self.get_turn_by_turn_directions(result['path'])
        for direction in directions:
            print(direction)
    
    def visualize_route(self, result, start, end, show_algorithm_steps=False):
        """Create a visual map showing the route and algorithm execution"""
        plt.figure(figsize=(15, 10))
        
        # Create network graph
        G = nx.Graph()
        
        # Add nodes
        for node_id, coords in self.coordinates.items():
            G.add_node(node_id, pos=coords)
        
        # Add edges
        for node, neighbors in self.graph.items():
            for neighbor, weight in neighbors:
                if not G.has_edge(node, neighbor):
                    G.add_edge(node, neighbor, weight=weight)
        
        pos = nx.get_node_attributes(G, 'pos')
        
        # Draw all roads (light gray)
        nx.draw_networkx_edges(G, pos, edge_color='lightgray', width=1, alpha=0.6)
        
        # Draw all intersections
        nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                              node_size=300, alpha=0.8)
        
        # Highlight visited nodes (explored during algorithm)
        if result['visited']:
            visited_nodes = [n for n in result['visited'] if n != start and n != end]
            if visited_nodes:
                nx.draw_networkx_nodes(G, pos, nodelist=visited_nodes,
                                      node_color='orange', node_size=350, alpha=0.9)
        
        # Highlight the optimal path
        if result['success'] and len(result['path']) > 1:
            path_edges = [(result['path'][i], result['path'][i+1]) 
                         for i in range(len(result['path'])-1)]
            nx.draw_networkx_edges(G, pos, edgelist=path_edges,
                                  edge_color='purple', width=4, alpha=0.8)
            
            # Highlight path nodes
            path_nodes = [n for n in result['path'] if n != start and n != end]
            if path_nodes:
                nx.draw_networkx_nodes(G, pos, nodelist=path_nodes,
                                      node_color='purple', node_size=400, alpha=0.9)
        
        # Highlight start and end nodes
        nx.draw_networkx_nodes(G, pos, nodelist=[start], 
                              node_color='green', node_size=500, alpha=1.0)
        nx.draw_networkx_nodes(G, pos, nodelist=[end], 
                              node_color='red', node_size=500, alpha=1.0)
        
        # Add node labels
        labels = {i: str(i) for i in self.coordinates.keys()}
        nx.draw_networkx_labels(G, pos, labels, font_size=8, font_weight='bold')
        
        # Add edge labels (distances)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        edge_labels = {edge: f"{weight:.1f}km" for edge, weight in edge_labels.items()}
        nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=6)
        
        plt.title(f"GPS Navigation: {self.node_names[start]} → {self.node_names[end]}", 
                 fontsize=14, fontweight='bold')
        
        # Add legend
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='green', 
                      markersize=10, label='Start'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', 
                      markersize=10, label='Destination'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', 
                      markersize=10, label='Explored'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='purple', 
                      markersize=10, label='Optimal Path'),
            plt.Line2D([0], [0], color='purple', linewidth=3, label='Route')
        ]
        plt.legend(handles=legend_elements, loc='upper right')
        
        plt.axis('off')
        plt.tight_layout()
        
        if show_algorithm_steps:
            # Create a second subplot for algorithm steps
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
            
            # Plot the map on the left
            plt.sca(ax1)
            # (repeat the plotting code above for ax1)
            
            # Show algorithm steps on the right
            ax2.text(0.05, 0.95, "Algorithm Execution Steps:", 
                    transform=ax2.transAxes, fontsize=12, fontweight='bold',
                    verticalalignment='top')
            
            step_text = "\n".join(result['steps'][:20])  # Show first 20 steps
            ax2.text(0.05, 0.85, step_text, transform=ax2.transAxes, 
                    fontsize=8, verticalalignment='top', fontfamily='monospace')
            
            ax2.set_xlim(0, 1)
            ax2.set_ylim(0, 1)
            ax2.axis('off')
        
        plt.show()
    
    def interactive_navigation(self):
        """Interactive CLI for GPS navigation"""
        print("🗺️  GPS NAVIGATION SYSTEM")
        print("=" * 50)
        print("Available locations:")
        for node_id, name in self.node_names.items():
            print(f"{node_id:2d}. {name}")
        
        while True:
            try:
                print("\n" + "─" * 50)
                start = int(input("Enter start location ID (or -1 to quit): "))
                if start == -1:
                    break
                
                end = int(input("Enter destination ID: "))
                
                if start not in self.node_names or end not in self.node_names:
                    print("❌ Invalid location ID. Please try again.")
                    continue
                
                if start == end:
                    print("❌ Start and destination cannot be the same.")
                    continue
                
                # Find route
                print("\n🔄 Calculating route...")
                result = self.dijkstra(start, end, verbose=True)
                
                # Display results
                self.print_route_summary(result, start, end)
                
                # Ask if user wants to see visualization
                show_viz = input("\nShow route visualization? (y/n): ").lower() == 'y'
                if show_viz:
                    self.visualize_route(result, start, end)
                
            except ValueError:
                print("❌ Please enter valid numbers.")
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break

def demo_gps_navigation():
    """Demonstrate the GPS navigation system with example routes"""
    navigator = GPSNavigator()
    
    print("🚗 GPS NAVIGATION SYSTEM DEMO")
    print("=" * 60)
    
    # Demo routes
    demo_routes = [
        (0, 11, "Main St & 1st Ave", "Mountain Rd & 3rd Ave"),
        (3, 10, "Elm St & 1st Ave", "Lake Ave & 2nd Ave"),
        (1, 8, "Park Rd & 2nd Ave", "Hill Rd & 3rd Ave")
    ]
    
    for i, (start, end, start_name, end_name) in enumerate(demo_routes, 1):
        print(f"\n📍 DEMO ROUTE {i}: {start_name} → {end_name}")
        print("─" * 60)
        
        result = navigator.dijkstra(start, end, verbose=False)
        navigator.print_route_summary(result, start, end)
        
        # Show visualization for first demo
        if i == 1:
            print("\n📊 Showing route visualization...")
            navigator.visualize_route(result, start, end)
    
    # Interactive mode
    print(f"\n🎮 Ready for interactive navigation!")
    navigator.interactive_navigation()

if __name__ == "__main__":
    # You can run different modes:
    
    # 1. Full demo with examples and interactive mode
    demo_gps_navigation()
    
    # 2. Or create your own navigator instance
    # navigator = GPSNavigator()
    # result = navigator.dijkstra(0, 11, verbose=True)
    # navigator.print_route_summary(result, 0, 11)
    # navigator.visualize_route(result, 0, 11)