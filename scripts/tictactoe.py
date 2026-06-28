import os
import re
import sys
from pathlib import Path

README = Path(__file__).parent.parent / "README.md"
BOARD_START = "<!-- TICTACTOE-BOARD-START -->"
BOARD_END = "<!-- TICTACTOE-BOARD-END -->"
REPO = "Aayush-25/Aayush-25"

# ── board helpers ─────────────────────────────────────────────────────────────

def cell_value(cell: str):
    """Return 'X', 'O', or None from a raw markdown cell string."""
    if "❌" in cell:
        return "X"
    if "🤖" in cell:
        return "O"
    return None


def parse_board(section: str) -> list[list]:
    """
    Parse the 3×3 board from the markdown table section.
    When two boards are present (post-game-over state), the second one
    (the fresh board) overwrites the first, leaving all-None.
    """
    board = [[None] * 3 for _ in range(3)]
    # Matches rows like: | **0** | cell | cell | cell |
    for m in re.finditer(r'\|\s*\*\*(\d)\*\*\s*\|(.*?)\|(.*?)\|(.*?)\|', section):
        r = int(m.group(1))
        for c, raw in enumerate([m.group(2), m.group(3), m.group(4)]):
            board[r][c] = cell_value(raw)
    return board


def render_cell(r: int, c: int, val) -> str:
    if val == "X":
        return "❌"
    if val == "O":
        return "🤖"
    return f"[⬜](https://github.com/{REPO}/issues/new?title=ttt:{r},{c}&body=make+move)"


def render_board(board: list[list]) -> str:
    header = "| | 0 | 1 | 2 |\n|---|---|---|---|"
    rows = "\n".join(
        f"| **{r}** | " + " | ".join(render_cell(r, c, board[r][c]) for c in range(3)) + " |"
        for r in range(3)
    )
    return f"{header}\n{rows}"


def fresh_board() -> list[list]:
    return [[None] * 3 for _ in range(3)]


# ── game logic ────────────────────────────────────────────────────────────────

LINES = [
    [(0,0),(0,1),(0,2)], [(1,0),(1,1),(1,2)], [(2,0),(2,1),(2,2)],  # rows
    [(0,0),(1,0),(2,0)], [(0,1),(1,1),(2,1)], [(0,2),(1,2),(2,2)],  # cols
    [(0,0),(1,1),(2,2)], [(0,2),(1,1),(2,0)],                        # diagonals
]


def check_winner(board) -> str | None:
    for line in LINES:
        vals = [board[r][c] for r, c in line]
        if vals == ["X", "X", "X"]:
            return "X"
        if vals == ["O", "O", "O"]:
            return "O"
    return None


def is_full(board) -> bool:
    return all(board[r][c] is not None for r in range(3) for c in range(3))


def minimax(board, is_maximizing: bool) -> int:
    winner = check_winner(board)
    if winner == "O":
        return 10
    if winner == "X":
        return -10
    if is_full(board):
        return 0
    if is_maximizing:
        best = -100
        for r in range(3):
            for c in range(3):
                if board[r][c] is None:
                    board[r][c] = "O"
                    best = max(best, minimax(board, False))
                    board[r][c] = None
        return best
    else:
        best = 100
        for r in range(3):
            for c in range(3):
                if board[r][c] is None:
                    board[r][c] = "X"
                    best = min(best, minimax(board, True))
                    board[r][c] = None
        return best


def best_move(board) -> tuple[int, int] | None:
    best_score, move = -100, None
    for r in range(3):
        for c in range(3):
            if board[r][c] is None:
                board[r][c] = "O"
                score = minimax(board, False)
                board[r][c] = None
                if score > best_score:
                    best_score, move = score, (r, c)
    return move


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    raw = os.environ.get("PLAYER_MOVE", "").strip().removeprefix("ttt:")
    if not raw:
        print("PLAYER_MOVE not set or empty.", file=sys.stderr)
        sys.exit(1)

    try:
        row_s, col_s = raw.split(",", 1)
        row, col = int(row_s.strip()), int(col_s.strip())
    except ValueError:
        print(f"Bad move format '{raw}'. Expected 'row,col'.", file=sys.stderr)
        sys.exit(1)

    if not (0 <= row <= 2 and 0 <= col <= 2):
        print(f"Move ({row},{col}) out of range 0-2.", file=sys.stderr)
        sys.exit(1)

    content = README.read_text(encoding="utf-8")
    s = content.find(BOARD_START)
    e = content.find(BOARD_END)
    if s == -1 or e == -1:
        print("Board markers missing from README.", file=sys.stderr)
        sys.exit(1)

    section = content[s + len(BOARD_START):e]
    board = parse_board(section)

    # If the last game ended and wasn't cleared yet, silently start fresh
    if check_winner(board) or is_full(board):
        board = fresh_board()

    if board[row][col] is not None:
        print(f"Cell ({row},{col}) is already taken.", file=sys.stderr)
        sys.exit(1)

    # Player X moves
    board[row][col] = "X"
    winner = check_winner(board)

    if winner == "X":
        status = "🎉 You win! New game below ↓"
    elif is_full(board):
        status = "🤝 Draw! New game below ↓"
    else:
        # Bot O moves via minimax
        ai = best_move(board)
        if ai:
            board[ai[0]][ai[1]] = "O"
        winner = check_winner(board)
        if winner == "O":
            status = "🤖 Bot wins! New game below ↓"
        elif is_full(board):
            status = "🤝 Draw! New game below ↓"
        else:
            status = None

    if status:
        # Show final state + reset board so the next visitor plays fresh
        new_section = (
            f"\n{render_board(board)}\n\n"
            f"<p align=\"center\"><strong>{status}</strong></p>\n\n"
            f"{render_board(fresh_board())}\n"
        )
        print(f"Game over: {status}")
    else:
        new_section = f"\n{render_board(board)}\n"
        print("Move applied.")

    new_content = content[:s + len(BOARD_START)] + new_section + content[e:]
    README.write_text(new_content, encoding="utf-8")


if __name__ == "__main__":
    main()
