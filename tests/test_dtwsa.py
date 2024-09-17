import pytest
from dtwsa import SentenceAligner
from dtwsa.metrics import WER_similarity
from test_data import big_list_1, big_list_2


# Define a simple similarity function for testing
def simple_similarity(word1, word2):
    return 1 if word1 == word2 else 0

@pytest.fixture
def aligner():
    return SentenceAligner(simple_similarity)

def test_init():
    aligner = SentenceAligner(simple_similarity)
    assert aligner.similarity_function == simple_similarity

def test_similarity_caching(aligner: SentenceAligner):
    # Test that the _similarity method is correctly cached
    assert aligner.similarity_function("word", "word") == 1
    assert aligner.similarity_function("word", "other") == 0
    
    # Call it again to ensure it's cached
    assert aligner.similarity_function("word", "word") == 1
    assert aligner.similarity_function("word", "other") == 0

def test_align_identical_sentences(aligner: SentenceAligner):
    list1 = ["The", "cat", "is", "black"]
    list2 = ["The", "cat", "is", "black"]
    alignment, score = aligner.align_sentences(list1, list2)
    assert alignment == [(0, 0), (1, 1), (2, 2), (3, 3)]
    assert score == 4

def test_align_different_sentences(aligner: SentenceAligner):
    list1 = ["The", "cat", "is", "black"]
    list2 = ["A", "dog", "is", "white"]
    alignment, score = aligner.align_sentences(list1, list2)
    assert alignment == [(0,0), (1,1), (2,2), (3,3)]
    assert score == 1

def test_align_with_skips(aligner: SentenceAligner):
    list1 = ["The", "quick", "brown", "fox"]
    list2 = ["The", "fox"]
    alignment, score = aligner.align_sentences(list1, list2)
    assert alignment == [(0, 0), (3, 1)]
    assert score == 2


def test_wer_similarity():
    score = WER_similarity("The cat sat on a mat.", "The cat sat on a mat.")
    assert score == 1.0
    score = WER_similarity("The cat sat on a mat.", "A cat was sitting on a mat.")
    assert score == 0.5
    score = WER_similarity("The cat sat on a mat.", "A cat was sitting on the mat.")
    pytest.approx(score, 0.8333333333333334)

def test_similarity_matrix():
    aligner = SentenceAligner(WER_similarity)
    aligner._get_similarity_matrix(big_list_1, big_list_2)
    sim_matrix = aligner.similarity_matrix
    
    aligner = SentenceAligner(similarity_matrix=sim_matrix)
    alignment, score = aligner.align_sentences(big_list_1, big_list_2)

    assert score == 9
    assert alignment == [(2, 0), (3, 1), (4, 2), (5, 3), (6, 4), (7, 5), (8, 6), (9, 7), (10, 9)]

def test_bigger():
    aligner = SentenceAligner(WER_similarity)
    alignment, score = aligner.align_sentences(big_list_1, big_list_2)
    assert score == 9
    assert alignment == [(2, 0), (3, 1), (4, 2), (5, 3), (6, 4), (7, 5), (8, 6), (9, 7), (10, 9)]


def test_plot():
    aligner = SentenceAligner(WER_similarity)
    aligner.align_sentences(big_list_1, big_list_2)

    # Test that the plot function runs without errors
    aligner.visualize_alignment(big_list_1, big_list_2)