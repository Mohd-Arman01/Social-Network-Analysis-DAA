
# SOCIAL NETWORK CONNECTION AND RECOMMENDATION ANALYSIS
# DAA Project 4

from collections import deque
import time


class SocialNetwork:

    def __init__(self):
        self.graph = {}

    # Add user
    def add_user(self, name):
        if name not in self.graph:
            self.graph[name] = set()
            print(name, "added successfully!")
        else:
            print("User already exists!")

    # Add friendship (undirected edge)
    def add_friendship(self, user1, user2):
        if user1 in self.graph and user2 in self.graph:
            self.graph[user1].add(user2)
            self.graph[user2].add(user1)
            print("Friendship added successfully!")
        else:
            print("Both users must exist!")

    # Display network
    def display_network(self):
        print("\n--- SOCIAL NETWORK ---")

        for user, friends in self.graph.items():
            print(user, "->", ", ".join(sorted(friends)) or "No friends")

    # BFS traversal
    def bfs(self, start):
        if start not in self.graph:
            print("User not found!")
            return []

        visited = set()
        queue = deque([start])
        result = []

        while queue:
            user = queue.popleft()

            if user not in visited:
                visited.add(user)
                result.append(user)

                for friend in sorted(self.graph[user]):
                    if friend not in visited:
                        queue.append(friend)

        return result

    # DFS traversal
    def dfs(self, start):
        if start not in self.graph:
            print("User not found!")
            return []

        visited = set()
        stack = [start]
        result = []

        while stack:
            user = stack.pop()

            if user not in visited:
                visited.add(user)
                result.append(user)

                for friend in sorted(self.graph[user], reverse=True):
                    if friend not in visited:
                        stack.append(friend)

        return result

    # Mutual friends
    def mutual_friends(self, user1, user2):
        if user1 not in self.graph or user2 not in self.graph:
            print("User not found!")
            return

        common = self.graph[user1].intersection(self.graph[user2])

        print("\nMutual friends of", user1, "and", user2, ":")

        if common:
            print(", ".join(sorted(common)))
        else:
            print("No mutual friends found.")

    # Shortest path using BFS
    def shortest_path(self, start, destination):
        if start not in self.graph or destination not in self.graph:
            print("User not found!")
            return

        queue = deque([start])
        parent = {start: None}

        while queue:
            user = queue.popleft()

            if user == destination:
                break

            for friend in sorted(self.graph[user]):
                if friend not in parent:
                    parent[friend] = user
                    queue.append(friend)

        if destination not in parent:
            print("No connection path found!")
            return

        path = []
        current = destination

        while current is not None:
            path.append(current)
            current = parent[current]

        path.reverse()

        print("\nShortest connection path:")
        print(" -> ".join(path))
        print("Total connections:", len(path) - 1)


# Create sample network for demonstration
network = SocialNetwork()

users = ["Arman", "Rahul", "Aman", "Neha", "Karan", "Priya"]

for user in users:
    network.add_user(user)

friendships = [
    ("Arman", "Rahul"),
    ("Arman", "Aman"),
    ("Rahul", "Neha"),
    ("Aman", "Neha"),
    ("Neha", "Karan"),
    ("Karan", "Priya")
]

for user1, user2 in friendships:
    network.add_friendship(user1, user2)


# Display network
network.display_network()

# BFS
print("\n--- BFS TRAVERSAL ---")
print(" -> ".join(network.bfs("Arman")))

# DFS
print("\n--- DFS TRAVERSAL ---")
print(" -> ".join(network.dfs("Arman")))

# Mutual friends
network.mutual_friends("Rahul", "Aman")

# Shortest path
network.shortest_path("Arman", "Priya")


# Generate test networks of different sizes
def create_test_network(size):
    test_network = SocialNetwork()

    # Create users
    for i in range(size):
        test_network.graph[f"User{i}"] = set()

    # Create a connected network
    for i in range(size - 1):
        test_network.graph[f"User{i}"].add(f"User{i + 1}")
        test_network.graph[f"User{i + 1}"].add(f"User{i}")

    # Add extra connections
    for i in range(size):
        for step in (2, 5, 10):
            if i + step < size:
                user1 = f"User{i}"
                user2 = f"User{i + step}"

                test_network.graph[user1].add(user2)
                test_network.graph[user2].add(user1)

    return test_network


# Compare BFS and DFS performance
def performance_comparison():

    print("\n--- PERFORMANCE COMPARISON ---")
    print("Average execution time over 5 runs")
    print("-" * 65)
    print(f"{'Users':<12}{'Connections':<15}{'BFS (ms)':<18}{'DFS (ms)':<15}")
    print("-" * 65)

    sizes = [10, 100, 500, 1000]

    for size in sizes:
        test_network = create_test_network(size)
        start = "User0"

        # Warm-up runs
        test_network.bfs(start)
        test_network.dfs(start)

        bfs_total = 0
        dfs_total = 0

        # Run each algorithm 5 times
        for _ in range(5):

            start_time = time.perf_counter()
            test_network.bfs(start)
            bfs_total += time.perf_counter() - start_time

            start_time = time.perf_counter()
            test_network.dfs(start)
            dfs_total += time.perf_counter() - start_time

        bfs_avg = (bfs_total / 5) * 1000
        dfs_avg = (dfs_total / 5) * 1000

        edge_count = sum(
            len(friends) for friends in test_network.graph.values()
        ) // 2

        print(
            f"{size:<12}{edge_count:<15}"
            f"{bfs_avg:<18.4f}{dfs_avg:<15.4f}"
        )

    print("-" * 65)
    print("Performance comparison completed!")


# Run performance comparison
performance_comparison()
