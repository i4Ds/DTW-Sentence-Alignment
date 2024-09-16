from jiwer import wer

def WER_similarity(sentence1, sentence2):
    return 1 - wer(sentence1, sentence2)