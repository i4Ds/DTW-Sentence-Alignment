# DTW-Sentence-Alignment

A simple, low-dependency package for aligning sentences by minimizing a chosen metric.

## Overview

DTW-Sentence-Alignment is a Python package that provides functionality for aligning sentences using Dynamic Time Warping (DTW) algorithm. It allows users to align sentences based on custom similarity functions or predefined metrics. The alignment works by maximizing a score. Additionally, compared to other implementation, the first starting point does not have to be (0,0) and the last ending point does not have to be (n,m).

## Installation

To install the package, you can use pip:
`pip install dtwsa`

## Usage

Here's a basic example of how to use the package:

```python
from dtwsa import SentenceAligner
from dtwsa.metrics import WER_similarity

# Align sentences
list_1 = [
    "Something which does not match",
    "Matching sentence number one",
    "Something which does not match",
    "Another matching sentence",
    "Something which does not match",
    "Random Sentence which should match",
    "This should be matched with something",
    "Yet another matching sentence",
    "Random Sentence which should match",
    "This should be matched with something",
    "Yet another matching sentence",
    "Something which does not match",
    "Something which does not match",
    "Something that matches again",
    "Something which does not match",
]

list_2 = [
    "Something which does not match",
    "Matching sentence number one",
    "Another matching sentence",
    "Random Sentence which should match",
    "This should be matched with something",
    "Yet another matching sentence",
    "Random Sentence which should match",
    "This should be matched with something",
    "Yet another matching sentence",
    "Something that matches again",
    "Something leftover",
]

alignment, score = aligner.align_sentences(list_1, list_2)

print(f"Alignment: {alignment}")
print(f"Score: {score}")

# Plot the alignment
aligner.visualize_alignment(list_1, list_2)
```

## Features
- Flexible sentence alignment using custom similarity functions
- Predefined metrics like Word Error Rate (WER) similarity
- Simple API for easy integration


## TODO
1. Improve efficiency of the alignment algorithm
2. Improve efficiency of the alignment algorithm
3. Improve efficiency of the alignment algorithm
2. Add new metrics for sentence comparison (e.g., BLEU score, cosine similarity)