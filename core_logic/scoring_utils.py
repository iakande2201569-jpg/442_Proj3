def get_match_score(char1: str, char2: str, match_reward: int, mismatch_penalty: int) -> int:
    """
    Evaluates two characters and returns the corresponding score.
    
    Args:
        char1 (str): Character from the first sequence.
        char2 (str): Character from the second sequence.
        match_reward (int): Score added for a match.
        mismatch_penalty (int): Score subtracted/added for a mismatch.
        
    Returns:
        int: The calculated evaluation score.
    """
    if char1 == char2:
        return match_reward
    return mismatch_penalty