from typing import List, Dict, Tuple, Any
from core_logic.scoring_utils import get_match_score

def build_score_grid(rows: int, cols: int) -> List[List[Dict[str, Any]]]:
    """
    Initializes an empty dynamic programming matrix.
    
    Args:
        rows (int): Number of rows (length of seq1 + 1).
        cols (int): Number of columns (length of seq2 + 1).
        
    Returns:
        List[List[Dict]]: A 2D list of dictionaries containing score, pointer, and is_path flags.
    """
    matrix = []
    for _ in range(rows):
        row = []
        for _ in range(cols):
            row.append({
                "score": 0,
                "pointer": None,  # "diag", "up", or "left"
                "is_path": False
            })
        matrix.append(row)
    return matrix

def compute_global_alignment_matrix(seq1: str, seq2: str, match: int, mismatch: int, gap: int) -> Tuple[List[List[Dict[str, Any]]], int, int]:
    """
    Computes the DP matrix for Global Alignment.
    
    Returns:
        Tuple: (Completed matrix, start_i for traceback, start_j for traceback)
    """
    rows, cols = len(seq1) + 1, len(seq2) + 1
    grid = build_score_grid(rows, cols)

    # Initialize first column and first row with cumulative gap penalties
    for i in range(1, rows):
        grid[i][0]["score"] = i * gap
        grid[i][0]["pointer"] = "up"
        
    for j in range(1, cols):
        grid[0][j]["score"] = j * gap
        grid[0][j]["pointer"] = "left"

    # Fill the DP matrix
    for i in range(1, rows):
        for j in range(1, cols):
            diag_score = grid[i-1][j-1]["score"] + get_match_score(seq1[i-1], seq2[j-1], match, mismatch)
            up_score = grid[i-1][j]["score"] + gap
            left_score = grid[i][j-1]["score"] + gap
            
            max_score = max(diag_score, up_score, left_score)
            grid[i][j]["score"] = max_score
            
            # Determine explicit directional pointer
            if max_score == diag_score:
                grid[i][j]["pointer"] = "diag"
            elif max_score == up_score:
                grid[i][j]["pointer"] = "up"
            else:
                grid[i][j]["pointer"] = "left"

    # Traceback for global alignment starts at the bottom-right corner
    return grid, rows - 1, cols - 1

def compute_local_alignment_matrix(seq1: str, seq2: str, match: int, mismatch: int, gap: int) -> Tuple[List[List[Dict[str, Any]]], int, int]:
    """
    Computes the DP matrix for Local Alignment.
    
    Returns:
        Tuple: (Completed matrix, start_i for traceback, start_j for traceback)
    """
    rows, cols = len(seq1) + 1, len(seq2) + 1
    grid = build_score_grid(rows, cols)
    
    max_overall_score = 0
    max_i, max_j = 0, 0

    # Fill the DP matrix
    for i in range(1, rows):
        for j in range(1, cols):
            diag_score = grid[i-1][j-1]["score"] + get_match_score(seq1[i-1], seq2[j-1], match, mismatch)
            up_score = grid[i-1][j]["score"] + gap
            left_score = grid[i][j-1]["score"] + gap
            
            # Local alignment includes 0 in the recurrence relation
            max_score = max(0, diag_score, up_score, left_score)
            grid[i][j]["score"] = max_score
            
            if max_score > 0:
                if max_score == diag_score:
                    grid[i][j]["pointer"] = "diag"
                elif max_score == up_score:
                    grid[i][j]["pointer"] = "up"
                else:
                    grid[i][j]["pointer"] = "left"
            else:
                grid[i][j]["pointer"] = None

            # Track highest score for traceback origin
            if max_score >= max_overall_score:
                max_overall_score = max_score
                max_i, max_j = i, j

    return grid, max_i, max_j