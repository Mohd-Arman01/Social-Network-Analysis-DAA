
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import time
from collections import deque

st.set_page_config(
    page_title="Social Network Analysis",
    page_icon="🌐",
    layout="wide"
)

st.title("🌐 Social Network Connection and Recommendation Analysis")
st.write("Explore users, friendships and shortest connection paths.")

# INITIAL NETWORK
if "network" not in st.session_state:
    st.session_state.network = {
        "Arman": ["Rahul", "Aman"],
        "Rahul": ["Arman", "Neha"],
        "Aman": ["Arman", "Neha"],
        "Neha": ["Rahul", "Aman", "Karan"],
        "Karan": ["Neha", "Priya"],
        "Priya": ["Karan"]
    }

network = st.session_state.network

# BFS
def bfs(start):
    visited = []
    queue = deque([start])

    while queue:
        user = queue.popleft()

        if user not in visited:
            visited.append(user)
            for friend in network[user]:
                if friend not in visited:
                    queue.append(friend)

    return visited

# DFS
def dfs(start):
    visited = []
    stack = [start]

    while stack:
        user = stack.pop()

        if user not in visited:
            visited.append(user)
            for friend in reversed(network[user]):
                if friend not in visited:
                    stack.append(friend)

    return visited

# SHORTEST PATH
def shortest_path(start, end):
    queue = deque([start])
    parent = {start: None}

    while queue:
        current = queue.popleft()

        if current == end:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1]

        for friend in network[current]:
            if friend not in parent:
                parent[friend] = current
                queue.append(friend)

    return None

# SIDEBAR: ADD USER
st.sidebar.header("Manage Social Network")

st.sidebar.subheader("Add New User")
new_user = st.sidebar.text_input("Enter user name")

if st.sidebar.button("Add User"):
    name = new_user.strip()

    if not name:
        st.sidebar.error("Please enter a name.")
    elif name in network:
        st.sidebar.warning("User already exists.")
    else:
        network[name] = []
        st.sidebar.success("User added successfully!")
        st.rerun()

# SIDEBAR: ADD CONNECTION
st.sidebar.divider()
st.sidebar.subheader("Add Connection")

users = list(network.keys())

if len(users) >= 2:
    user1 = st.sidebar.selectbox(
        "First User", users, key="connection1"
    )
    user2 = st.sidebar.selectbox(
        "Second User", users, key="connection2"
    )

    if st.sidebar.button("Add Friendship"):
        if user1 == user2:
            st.sidebar.error("Choose two different users.")
        elif user2 in network[user1]:
            st.sidebar.warning("Connection already exists.")
        else:
            network[user1].append(user2)
            network[user2].append(user1)
            st.sidebar.success("Connection added!")
            st.rerun()

# CREATE GRAPH
G = nx.Graph()

for user, friends in network.items():
    G.add_node(user)
    for friend in friends:
        G.add_edge(user, friend)

# DISPLAY GRAPH
st.header("📊 Dynamic Social Network Graph")

fig, ax = plt.subplots(figsize=(11, 6))
pos = nx.spring_layout(G, seed=42)

nx.draw(
    G,
    pos,
    with_labels=True,
    node_color="skyblue",
    node_size=2200,
    font_size=10,
    font_weight="bold",
    edge_color="gray",
    width=2,
    ax=ax
)

ax.set_title("Social Network Connections")
st.pyplot(fig)
plt.close(fig)

# STATISTICS
st.header("📈 Network Statistics")

c1, c2, c3 = st.columns(3)
c1.metric("Total Users", len(network))
c2.metric("Total Connections", G.number_of_edges())
c3.metric("Connected Groups", nx.number_connected_components(G))

# BFS AND DFS
st.header("🔍 BFS and DFS Traversal")

start_user = st.selectbox(
    "Choose Starting User",
    users,
    key="traversal_start"
)

c1, c2 = st.columns(2)

with c1:
    if st.button("Run BFS"):
        st.success("BFS: " + " → ".join(bfs(start_user)))

with c2:
    if st.button("Run DFS"):
        st.success("DFS: " + " → ".join(dfs(start_user)))

# MUTUAL FRIENDS
st.header("🤝 Mutual Friends")

c1, c2 = st.columns(2)

with c1:
    m1 = st.selectbox("First User", users, key="mutual1")

with c2:
    m2 = st.selectbox("Second User", users, key="mutual2")

if st.button("Find Mutual Friends"):
    if m1 == m2:
        st.warning("Choose different users.")
    else:
        common = sorted(set(network[m1]) & set(network[m2]))

        if common:
            st.success("Mutual Friends: " + ", ".join(common))
        else:
            st.info("No mutual friends found.")

# SHORTEST PATH
st.header("🛣️ Shortest Connection Path")

c1, c2 = st.columns(2)

with c1:
    source = st.selectbox("Starting User", users, key="source")

with c2:
    destination = st.selectbox(
        "Destination User", users, key="destination"
    )

if st.button("Find Shortest Path"):
    path = shortest_path(source, destination)

    if path:
        st.success(" → ".join(path))
        st.info(f"Total Connections: {len(path) - 1}")
    else:
        st.warning("No path found.")

# PERFORMANCE ANALYSIS
st.header("⚡ BFS and DFS Performance Analysis")

sizes = [10, 100, 500, 1000]
bfs_times = []
dfs_times = []

for size in sizes:
    test_network = {
        str(i): [] for i in range(size)
    }

    for i in range(size - 1):
        test_network[str(i)].append(str(i + 1))
        test_network[str(i + 1)].append(str(i))

    # BFS timing
    start = time.perf_counter()
    visited = set()
    queue = deque(["0"])

    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            queue.extend(
                n for n in test_network[node]
                if n not in visited
            )

    bfs_times.append(time.perf_counter() - start)

    # DFS timing
    start = time.perf_counter()
    visited = set()
    stack = ["0"]

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            stack.extend(
                n for n in test_network[node]
                if n not in visited
            )

    dfs_times.append(time.perf_counter() - start)

df = pd.DataFrame({
    "Number of Users": sizes,
    "BFS Time (seconds)": bfs_times,
    "DFS Time (seconds)": dfs_times
})

st.dataframe(df, use_container_width=True)
st.line_chart(df.set_index("Number of Users"))

st.success("Social Network Analysis Dashboard is Ready!")
