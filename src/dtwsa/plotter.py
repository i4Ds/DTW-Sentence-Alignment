import matplotlib.pyplot as plt
import numpy as np

def visualize_alignment(list1, list2, cost_matrix, alignment):
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Create a heatmap of the cost matrix
    im = ax.imshow(cost_matrix, cmap='YlOrRd')
    
    # Add colorbar
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel("WER Cost", rotation=-90, va="bottom")
    
    # Plot the alignment path
    alignment_coords = [(j, i) for i, j in alignment]
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
            text = ax.text(j, i, f"{cost_matrix[i, j]:.2f}",
                           ha="center", va="center", color="black")
    
    # Adjust layout and display
    plt.tight_layout()
    plt.show()

# Using the data from your previous code
visualize_alignment(list1, list2, cost_matrix, alignment)