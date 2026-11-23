from typing import List, Tuple, Dict

ACTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Left, Right, Up, Down
START = (0, 3)
LIVING_REWARD = -0.04

GRID_LITERAL = [
    [0, 0, 0, 0],
    [0, "X", 0, 0],
    [0, 0, 0, 0],
    [0, -1, 0, 10],
]

def gridValues(x: int, y: int) -> float:
    """Get the value of a tile at (x, y)."""
    return GRID_LITERAL[3 - y][x]

def is_terminal(state: Tuple[int, int]) -> bool:
    """Check if the state is terminal (trap or recharge)."""
    x, y = state
    return gridValues(x, y) in (-1, 10)

def step(state: Tuple[int, int], action: Tuple[int, int]) -> Tuple[Tuple[int, int], float, bool]:
    """
    Perform a move from state with given action.
    Returns (next_state, reward, done).
    """
    x, y = state
    dx, dy = action
    
    # Check bounds and wall
    nx, ny = x + dx, y + dy
    if not (0 <= nx < 4 and 0 <= ny < 4):
        return state, LIVING_REWARD, False
    if gridValues(nx, ny) == "X":
        return state, LIVING_REWARD, False
    
    next_state = (nx, ny)
    tile_value = gridValues(nx, ny)
    reward = tile_value + LIVING_REWARD
    done = is_terminal(next_state)
    
    return next_state, reward, done

def print_policy(best_action_fn: callable) -> None:
    """Print the policy as a 4x4 grid."""
    for y in range(3, -1, -1):
        row = []
        for x in range(4):
            if gridValues(x, y) == "X":
                row.append("X")
            elif is_terminal((x, y)):
                val = gridValues(x, y)
                row.append(str(val))
            else:
                action = best_action_fn((x, y))
                if action == (0, -1):
                    row.append("v")
                elif action == (0, 1):
                    row.append("^")
                elif action == (-1, 0):
                    row.append("<")
                else:
                    row.append(">")
        print(" ".join(row))

def print_path(path: List[Tuple[int, int]]) -> None:
    """Print the path from start to end."""
    if not path:
        return
    for i, (x, y) in enumerate(path):
        marker = "S" if (x, y) == START else "E" if is_terminal((x, y)) else "."
        print(f"({x}, {y}) [{marker}]")
