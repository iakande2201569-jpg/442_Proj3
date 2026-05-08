from typing import List, Dict, Tuple, Any

def reconstruct_alignment_path(matrix: List[List[Dict[str, Any]]], seq1: str, seq2: str, start_i: int, start_j: int, is_local: bool) -> Tuple[str, str, int, List[List[Dict[str, Any]]]]:
    """
    Traces back through the DP matrix to reconstruct the aligned sequences.
    
    Returns:
        Tuple: (aligned_sequence_1, aligned_sequence_2, final_score, mutated_matrix_with_path_flags)
    """
    aligned_seq1 = []
    aligned_seq2 = []
    
    curr_i, curr_j = start_i, start_j
    final_score = matrix[curr_i][curr_j]["score"]

    # Traverse backwards following explicit pointers
    while True:
        # Stop condition for local alignment (score drops to 0 or pointer is None)
        if is_local and (matrix[curr_i][curr_j]["score"] == 0 or matrix[curr_i][curr_j]["pointer"] is None):
            matrix[curr_i][curr_j]["is_path"] = True
            break
        
        # Stop condition for global alignment (reached origin)
        if not is_local and curr_i == 0 and curr_j == 0:
            matrix[curr_i][curr_j]["is_path"] = True
            break

        matrix[curr_i][curr_j]["is_path"] = True
        pointer = matrix[curr_i][curr_j]["pointer"]

        if pointer == "diag":
            aligned_seq1.append(seq1[curr_i - 1])
            aligned_seq2.append(seq2[curr_j - 1])
            curr_i -= 1
            curr_j -= 1
        elif pointer == "up":
            aligned_seq1.append(seq1[curr_i - 1])
            aligned_seq2.append("-")
            curr_i -= 1
        elif pointer == "left":
            aligned_seq1.append("-")
            aligned_seq2.append(seq2[curr_j - 1])
            curr_j -= 1
        else:
            # Fallback for unexpected states
            break

    # Reverse the reconstructed sequences since we traced backwards
    aligned_seq1.reverse()
    aligned_seq2.reverse()

    return "".join(aligned_seq1), "".join(aligned_seq2), final_score, matrix