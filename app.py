import streamlit as st
import random

GRID_SIZE = 4  # Define the size of the Sudoku grid (4x4)

# Function to create an empty grid
def clear_grid():
    return [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

# Function to randomize the top row of the grid
def randomize_top_row(grid):
    grid[0] = random.sample(range(1, GRID_SIZE + 1), GRID_SIZE)
    return grid

# Function to check if a number can be placed in a given cell
def is_valid_cell(grid, row, col, num):
    # Check if the number is already in the same row or column
    if num in grid[row] or num in (grid[i][col] for i in range(GRID_SIZE)):
        return False
    
    # Check if the number is in the 2x2 box
    box_row, box_col = 2 * (row // 2), 2 * (col // 2)
    return not any(grid[i][j] == num for i in range(box_row, box_row + 2) for j in range(box_col, box_col + 2))

# Function to find the next empty cell in the grid
def find_empty_cell(grid):
    return next(((i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if grid[i][j] == 0), (-1, -1))

# Recursive function to solve the Sudoku puzzle
def sudoku_solve(grid):
    row, col = find_empty_cell(grid)
    if row == -1:  # If no empty cell is found, the puzzle is solved
        return True
    
    for num in range(1, GRID_SIZE + 1):
        if is_valid_cell(grid, row, col, num):
            grid[row][col] = num
            if sudoku_solve(grid):  # Recursively solve the rest of the puzzle
                return True
            grid[row][col] = 0  # Backtrack if the current solution doesn't work
    return False

# Function to generate a new Sudoku grid with a given difficulty
def generate_new_grid(difficulty):
    grid = randomize_top_row(clear_grid())
    sudoku_solve(grid)
    solution_grid = [row[:] for row in grid]  # Create a copy of the solved grid
    
    # Hide cells based on difficulty
    cells_to_hide = {"Easy": 4, "Medium": 6, "Hard": 8}.get(difficulty, 4)
    for _ in range(cells_to_hide):
        row, col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        while grid[row][col] == 0:
            row, col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        grid[row][col] = 0
    
    return grid, solution_grid, "Not Solved"

# Function to check if the current grid matches the solution
def check_solution(grid, solution_grid):
    return "Solved" if grid == solution_grid else "Incorrect!"

# Streamlit UI
st.title("(Game) Mini Sudoku Solver (4x4)")

# Initialize the game state if it doesn't exist
if 'game' not in st.session_state:
    st.session_state.game, st.session_state.solution, st.session_state.status = generate_new_grid("Easy")

# Difficulty selection
difficulty = st.radio("Select Difficulty:", ["Easy", "Medium", "Hard"])

# Button to generate a new grid
if st.button("Generate New Grid"):
    st.session_state.game, st.session_state.solution, st.session_state.status = generate_new_grid(difficulty)

# Create the Sudoku grid UI
for i in range(GRID_SIZE):
    cols = st.columns(GRID_SIZE)
    for j in range(GRID_SIZE):
        with cols[j]:
            value = st.session_state.game[i][j]
            new_value = st.number_input("", min_value=0, max_value=4, value=value, key=f"cell_{i}_{j}", 
                                        label_visibility="collapsed", format="%d", step=1)
            st.session_state.game[i][j] = new_value

# Button to check the solution
if st.button("Check Solution"):
    st.session_state.status = check_solution(st.session_state.game, st.session_state.solution)

# Display the current game state
st.write(f"Game State: {st.session_state.status}")