import folium
import networkx as nx


def find_shortest_path_and_map(locations:list, weights:list):
  G = nx.Graph()
  for i in range(len(locations)):
        for j in range(i + 1, len(locations)):
            G.add_edge(locations[i], locations[j], weight=weights[i + j - 1])

  source = locations[0]
  target = locations[3]
  shortest_path = nx.astar_path(G, source, target, weight="cost")


  center = ((source[0] + target[0]) / 2, (source[1] + target[1]) / 2)
  map = folium.Map(location=center, 
                   zoom_start=16)


  for i, node in enumerate(G.nodes()):
    folium.Marker(location=node, popup=f"Node: {i}").add_to(map)

  for edge in G.edges():
    start, end = edge
    folium.PolyLine(locations=[start, end], weight=2, color='blue').add_to(map)

  # Highlight the shortest path
  folium.PolyLine(locations=shortest_path, weight=5, color='red').add_to(map)

  # Display the map
  map.save('map_with_shortest_path.html')


# Example usage
locations = [(41.041992, 29.009048), 
             (41.045, 29.01), 
             (41.042, 29.008), 
             (41.050204, 29.005827)]
weights = [0, 1, 2, 2, 3, 2]
find_shortest_path_and_map(locations, weights)
