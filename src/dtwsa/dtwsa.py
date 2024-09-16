import numpy as np
from collections.abc import Callable
from functools import lru_cache
import matplotlib.pyplot as plt

class SentenceAligner:
    def __init__(self, similarity_function: Callable[[str, str], float], min_matching_value: float =  0.7, normalize_matrix: bool = False):
        self.similarity_function = similarity_function
        self.min_matching_value = min_matching_value
        self.normalize_matrix = normalize_matrix

    def _similarity(self, word1: str, word2: str) -> float:
        return self.similarity_function(word1, word2)
        
    def _get_cost_matrix(self, list1, list2):
        n, m = len(list1), len(list2)
        cost_matrix = np.zeros((n, m))

        for i in range(n):     
            for j in range(m):         
                cost_matrix[i, j] = self._similarity(list1[i], list2[j])

        if self.normalize_matrix:
            cost_matrix = (cost_matrix - cost_matrix.min()) / (cost_matrix.max() - cost_matrix.min())

        self.cost_matrix = cost_matrix

    def align_sentences(self, list1, list2): # The Dynamic-Programming Alignment Algorithm.
        n, m = len(list1), len(list2)
        
        # Initialize the dynamic programming matrix
        self.dp = np.zeros((n + 1, m + 1))

        # Calculate cost matrix
        self._get_cost_matrix(list1, list2)
        
        # Fill the dynamic programming matrix
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                if self.cost_matrix[i-1][j-1] >= self.min_matching_value:
                    match = self.dp[i-1][j-1] + self.cost_matrix[i-1][j-1]
                else:
                    match = self.dp[i-1][j-1]  # No score added if below threshold
                skip_list1 = self.dp[i-1][j] 
                skip_list2 = self.dp[i][j-1]  
                self.dp[i][j] = max(match, skip_list1, skip_list2)
        
        # Backtrack to find the optimal alignment
        alignment = []
        i, j = n, m
        while i > 0 and j > 0:
            if self.dp[i][j] == self.dp[i-1][j-1] + self.cost_matrix[i-1][j-1]:
                alignment.append((i-1, j-1))
                i -= 1
                j -= 1
            elif self.dp[i][j] == self.dp[i-1][j]:
                i -= 1
            else:
                j -= 1
        
        # Reverse the alignment to get the correct order
        alignment.reverse()
        self.alignment = alignment
        
        return self.alignment, self.dp[n][m]  # Return alignment and final score

    def visualize_alignment(self, list1, list2):
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Create a heatmap of the cost matrix
        im = ax.imshow(self.cost_matrix, cmap='YlOrRd')
        
        # Add colorbar
        cbar = ax.figure.colorbar(im, ax=ax)
        cbar.ax.set_ylabel("WER Cost", rotation=-90, va="bottom")
        
        # Plot the alignment path
        alignment_coords = [(j, i) for i, j in self.alignment]
        x, y = zip(*alignment_coords)
        ax.plot(x, y, color='blue', linewidth=2, marker='o', markersize=6)
        
        # Set labels and title
        ax.set_xlabel('List 2')
        ax.set_ylabel('List 1')
        ax.set_title('Sentence Alignment Visualization')
        
        # Set tick labels
        ax.set_xticks(np.arange(len(list2)))
        ax.set_yticks(np.arange(len(list1)))
        ax.set_xticklabels(list2)
        ax.set_yticklabels(list1)
        
        # Rotate the tick labels and set their alignment
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
        
        # Loop over data dimensions and create text annotations
        for i in range(len(list1)):
            for j in range(len(list2)):
                text = ax.text(j, i, f"{self.cost_matrix[i, j]:.2f}",
                            ha="center", va="center", color="black")
        
        # Adjust layout and display
        plt.tight_layout()
        plt.show()
