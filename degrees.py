import csv
import sys
from collections import deque

# Load data from CSV files into memory
def load_data(directory):
    # Load people
    people = {}
    names = {}
    with open(f"{directory}/people.csv", "r", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            person_id = row["id"]
            name = row["name"]
            birth = row["birth"]
            people[person_id] = {"name": name, "birth": birth, "movies": set()}
            if name in names:
                names[name].add(person_id)
            else:
                names[name] = {person_id}

    # Load movies
    movies = {}
    with open(f"{directory}/movies.csv", "r", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            movie_id = row["id"]
            title = row["title"]
            year = row["year"]
            movies[movie_id] = {"title": title, "year": year, "stars": set()}

    # Load stars
    with open(f"{directory}/stars.csv", "r", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            person_id = row["person_id"]
            movie_id = row["movie_id"]
            if movie_id in movies and person_id in people:
                movies[movie_id]["stars"].add(person_id)
                people[person_id]["movies"].add(movie_id)

    return people, names, movies

def shortest_path(source, target, people, movies):

    # Initialize the queue for BFS
    queue = deque([(source, [])])  # (current actor, path taken)
    visited = set()  # Track visited actors

    while queue:
        current_actor, path = queue.popleft()

        if current_actor == target:
            return path  # Return the path if target is found

        visited.add(current_actor)

        # Explore neighbors (movies)
        for movie_id in people[current_actor]["movies"]:
            for neighbor in movies[movie_id]["stars"]:
                if neighbor not in visited:
                    queue.append((neighbor, path + [(current_actor, movie_id)]))

    return None  # Return None if no path is found

# Main function to load data and find the shortest path
def main():
    directory = "E:/Documents/degrees/degrees/large"  # Updated path
    people, names, movies = load_data(directory)

    # Example usage
    source_name = input("Enter the first actor's name: ")
    target_name = input("Enter the second actor's name: ")

    source_ids = names.get(source_name)
    target_ids = names.get(target_name)

    if not source_ids or not target_ids:
        print("Actor not found.")
        return

    for source_id in source_ids:
        for target_id in target_ids:
            path = shortest_path(source_id, target_id, people, movies)
            if path is not None:
                print(f"{len(path)} degrees of separation.")
                for i, (actor_id, movie_id) in enumerate(path):
                    # Correctly reference the next actor in the path
                    next_actor_id = path[i + 1][0] if i + 1 < len(path) else target_id
                    print(f"{i + 1}: {people[actor_id]['name']} and {people[next_actor_id]['name']} starred in {movies[movie_id]['title']}")
                return

    print("No connection found.")

if __name__ == "__main__":
    main()
