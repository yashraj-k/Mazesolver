import tkinter as tk
from collections import deque

class MazeSolver:
    def __init__(self, maze):
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.visited = [[False] * self.cols for _ in range(self.rows)]

    def is_valid(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols and not self.visited[row][col] and self.maze[row][col] == 0

    def solve(self, start, end):
        queue = deque([(start, [])])

        while queue:
            current, path = queue.popleft()
            row, col = current
            self.visited[row][col] = True

            if current == end:
                return path + [current]

            neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]

            for neighbor in neighbors:
                n_row, n_col = neighbor
                if self.is_valid(n_row, n_col):
                    queue.append(((n_row, n_col), path + [current]))

        return []

def highlight_path(maze, path):
    highlighted_maze = [list(row) for row in maze]
    for (row, col) in path:
        highlighted_maze[row][col] = '*'

    return highlighted_maze

class MazeSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Solver")

        self.create_widgets()

    def create_widgets(self):
        self.maze_label = tk.Label(self.root, text="Enter the maze (0 for open path, 1 for walls):")
        self.maze_label.pack()

        self.maze_text = tk.Text(self.root, height=10, width=40)
        self.maze_text.pack()

        self.start_label = tk.Label(self.root, text="Enter the start point (row col):")
        self.start_label.pack()

        self.start_entry = tk.Entry(self.root)
        self.start_entry.pack()

        self.end_label = tk.Label(self.root, text="Enter the end point (row col):")
        self.end_label.pack()

        self.end_entry = tk.Entry(self.root)
        self.end_entry.pack()

        self.solve_button = tk.Button(self.root, text="Solve Maze", command=self.solve_maze)
        self.solve_button.pack()

        self.result_label = tk.Label(self.root, text="Result:")
        self.result_label.pack()

        self.result_text = tk.Text(self.root, height=10, width=40)
        self.result_text.pack()

    def solve_maze(self):
        maze_input = self.maze_text.get(1.0, tk.END)
        start_input = self.start_entry.get()
        end_input = self.end_entry.get()

        maze = [list(map(int, row.split())) for row in maze_input.split('\n') if row.strip()]
        start = tuple(map(int, start_input.split()))
        end = tuple(map(int, end_input.split()))

        solver = MazeSolver(maze)
        path = solver.solve(start, end)

        if path:
            result = "Shortest Path found!\n"
            highlighted_maze = highlight_path(maze, path)
            for row in highlighted_maze:
                result += ' '.join(map(str, row)) + '\n'
        else:
            result = "No path found."

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeSolverApp(root)
    root.mainloop()
