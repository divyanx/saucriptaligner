import sys
from saucriptaligner.sau_text_pair import Sausages, SausagesTranscriptPair

sys.path.append('../')



def sausages_from_kaldi_sausages_string(kaldi_sausages_string):
    """
    This function takes a string of sausages in kaldi format and returns a list of sausages
    :param kaldi_sausages_string: a string of sausages in kaldi format
    see test/test_aligner.py for example
    :return: Sausages
    """
    sau = []
    kaldi_sausages_string = kaldi_sausages_string.strip()[1:-2]
    print(kaldi_sausages_string)
    null_symbols = []
    for sausage in kaldi_sausages_string.split("] ["):
        sausage = sausage.strip()
        sausage_words_weights = sausage.split(" ")
        if len(sausage_words_weights) == 2 and sausage_words_weights[0] in null_symbols:
            continue
        word_weight_pair = []
        for i in range(0, len(sausage_words_weights), 2):
            print(sausage_words_weights[i], sausage_words_weights[i + 1])
            word_weight_pair.append((sausage_words_weights[i], float(sausage_words_weights[i + 1])))
        sau.append(word_weight_pair)
    sau = Sausages.create_from_edges_array(sau)
    return sau


def create_sausages_word_pair_from_kaldi_files(sausages_file, transcript_file):
    """
    This function takes a file of sausages and a file of words and returns a list of sausages
    :param sausages_file: a file of sausages in kaldi format
    :param transcript_file: a file of words in kaldi format
    :return: [SausagesTranscriptPair]
    """
    sausages = []
    with open(sausages_file, 'r') as f:
        for line in f:
            sausages.append(sausages_from_kaldi_sausages_string(line))

    texts = []
    with open(transcript_file, 'r') as f:
        for line in f:
            texts.append(line.strip())

    sausage_transcript_pair = []
    for i in range(len(sausages)):
        sausage_transcript_pair.append(SausagesTranscriptPair.create_from_sausages_wordlist(sausages[i], texts[i]))

    return sausage_transcript_pair
