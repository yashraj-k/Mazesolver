#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

struct MazeSolver {
    int** maze;
    int rows;
    int cols;
    bool** visited;
};

bool isValid(struct MazeSolver* solver, int row, int col) {
    return 0 <= row && row < solver->rows && 0 <= col && col < solver->cols &&
           !solver->visited[row][col] && solver->maze[row][col] == 0;
}

int* solve(struct MazeSolver* solver, int* start, int* end, int* pathLength) {
    int* queue = (int*)malloc(sizeof(int) * (solver->rows * solver->cols * 3)); // Added space for row and column information
    int* path = (int*)malloc(sizeof(int) * (solver->rows * solver->cols * 3)); // Added space for row and column information

    int queueFront = 0, queueRear = 0;

    queue[queueRear++] = start[0]; // Enqueue the row of the start
    queue[queueRear++] = start[1]; // Enqueue the column of the start

    while (queueFront < queueRear) {
        int currentRow = queue[queueFront++];
        int currentCol = queue[queueFront++];
        solver->visited[currentRow][currentCol] = true;

        if (currentRow == end[0] && currentCol == end[1]) {
            int pathIndex = 0;
            int current = queueFront - 2; // Adjust for the queue layout
            while (current != -2) {
                path[pathIndex++] = current;
                current = queue[current];
            }
            *pathLength = pathIndex / 3;
            return path;
        }

        int neighbors[4][2] = {{currentRow - 1, currentCol},
                               {currentRow + 1, currentCol},
                               {currentRow, currentCol - 1},
                               {currentRow, currentCol + 1}};

        for (int i = 0; i < 4; i++) {
            int nRow = neighbors[i][0];
            int nCol = neighbors[i][1];
            if (isValid(solver, nRow, nCol)) {
                queue[queueRear++] = nRow;
                queue[queueRear++] = nCol;
                queue[queueRear++] = queueFront - 2; // Store the previous element index
            }
        }
    }

    *pathLength = 0;
    return NULL;
}

int main() {
    int rows, cols;
    printf("Enter the number of rows and columns: ");
    scanf("%d %d", &rows, &cols);

    int** maze = (int**)malloc(sizeof(int*) * rows);
    for (int i = 0; i < rows; i++) {
        maze[i] = (int*)malloc(sizeof(int) * cols);
    }

    printf("Enter the maze (0 for open path, 1 for walls):\n");
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            scanf("%d", &maze[i][j]);
        }
    }

    struct MazeSolver solver;
    solver.maze = maze;
    solver.rows = rows;
    solver.cols = cols;

    int* path;
    int pathLength = 0;
    int start[2], end[2];

    printf("Enter the start point (row col): ");
    scanf("%d %d", &start[0], &start[1]);

    printf("Enter the end point (row col): ");
    scanf("%d %d", &end[0], &end[1]);

    solver.visited = (bool**)malloc(sizeof(bool*) * rows);
    for (int i = 0; i < rows; i++) {
        solver.visited[i] = (bool*)calloc(cols, sizeof(bool));
    }

    path = solve(&solver, start, end, &pathLength);

    if (path != NULL) {
        printf("Shortest Path found!\n");
        for (int i = pathLength - 1; i >= 0; i--) {
            int row = path[i * 3]; // Extract row information
            int col = path[i * 3 + 1]; // Extract column information
            printf("(%d, %d) ", row, col);
            maze[row][col] = -1; // Mark the path with -1
        }
        printf("\n");

        printf("Maze with Path:\n");
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                if (maze[i][j] == -1) {
                    printf("* "); // Print asterisk for the path
                } else {
                    printf("%d ", maze[i][j]);
                }
            }
            printf("\n");
        }
    } else {
        printf("No path found.\n");
    }

    for (int i = 0; i < rows; i++) {
        free(maze[i]);
        free(solver.visited[i]);
    }
    free(maze);
    free(solver.visited);
    free(path); // Free allocated path

    return 0;
}

