import numpy as np
from collections.abc import Callable
from functools import lru_cache

class SentenceAligner:
    def __init__(self, similarity_function: Callable[[str, str], float]):
        self.similarity_function = similarity_function

    @lru_cache(maxsize=None)
    def _similaity(self, word1: str, word2: str) -> float:
        return self.similarity_function(word1, word2)
        
    def align_sentences(self, list1, list2): # The Dynamic-Programming Alignment Algorithm.
        n, m = len(list1), len(list2)
        
        # Initialize the dynamic programming matrix
        dp = np.zeros((n + 1, m + 1)) 
        
        # Fill the dynamic programming matrix
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                match = dp[i-1][j-1] + self._similaity(list1[i-1], list2[j-1])
                skip_list1 = dp[i-1][j]  # No penalty for skipping
                skip_list2 = dp[i][j-1]  # No penalty for skipping
                dp[i][j] = max(match, skip_list1, skip_list2)
        
        # Backtrack to find the optimal alignment
        alignment = []
        i, j = n, m
        while i > 0 and j > 0:
            if dp[i][j] == dp[i-1][j-1] + self._similaity(list1[i-1], list2[j-1]):
                alignment.append((i-1, j-1))
                i -= 1
                j -= 1
            elif dp[i][j] == dp[i-1][j]:
                i -= 1
            else:
                j -= 1
        
        # Reverse the alignment to get the correct order
        alignment.reverse()
        
        return alignment, dp[n][m]  # Return alignment and final score

