import pytest
import numpy as np
from dtwsa.dtwsa import SentenceAligner

# Define a simple similarity function for testing
def simple_similarity(word1, word2):
    return 1 if word1 == word2 else 0

@pytest.fixture
def aligner():
    return SentenceAligner(simple_similarity)

def test_init():
    aligner = SentenceAligner(simple_similarity)
    assert aligner.similarity_function == simple_similarity

def test_similarity_caching(aligner):
    # Test that the _similarity method is correctly cached
    assert aligner._similaity("word", "word") == 1
    assert aligner._similaity("word", "other") == 0
    
    # Call it again to ensure it's cached
    assert aligner._similaity("word", "word") == 1
    assert aligner._similaity("word", "other") == 0

def test_align_identical_sentences(aligner):
    list1 = ["The", "cat", "is", "black"]
    list2 = ["The", "cat", "is", "black"]
    alignment, score = aligner.align_sentences(list1, list2)
    assert alignment == [(0, 0), (1, 1), (2, 2), (3, 3)]
    assert score == 4

def test_align_different_sentences(aligner):
    list1 = ["The", "cat", "is", "black"]
    list2 = ["A", "dog", "is", "white"]
    alignment, score = aligner.align_sentences(list1, list2)
    assert alignment == [(0,0), (1,1), (2,2), (3,3)]
    assert score == 1

def test_align_with_skips(aligner):
    list1 = ["The", "quick", "brown", "fox"]
    list2 = ["The", "fox"]
    alignment, score = aligner.align_sentences(list1, list2)
    assert alignment == [(0, 0), (3, 1)]
    assert score == 2

def test_align_empty_lists(aligner):
    list1 = []
    list2 = []
    alignment, score = aligner.align_sentences(list1, list2)
    assert alignment == []
    assert score == 0

def test_align_one_empty_list(aligner):
    list1 = ["The", "cat"]
    list2 = []
    alignment, score = aligner.align_sentences(list1, list2)
    assert alignment == []
    assert score == 0

def test_custom_similarity_function():
    def custom_similarity(word1, word2):
        return len(set(word1) & set(word2)) / len(set(word1) | set(word2))
    
    aligner = SentenceAligner(custom_similarity)
    list1 = ["apple", "banana"]
    list2 = ["apricot", "berry"]
    alignment, score = aligner.align_sentences(list1, list2)
    assert alignment == [(0, 0), (1, 1)]
    assert score > 0 and score < 2  # The exact score will depend on the similarity function

