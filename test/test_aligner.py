import sys
from colorama import Fore, Back, Style

import data.sample
from saucriptaligner.sau_text_pair import Sausages, Sausage, SausagesTranscriptPair
from saucriptaligner.align_sau_text_pair import SausagesTranscriptAligner
from utils.create_sausages import sausages_from_kaldi_sausages_string

sys.path.append('../')

sausage_text = data.sample.sausage_text
transcript_text_short = data.sample.transcript_text_short
transcript_text_long = data.sample.transcript_text_long


def test_aligned_sausages_word_pair_length():
    sau = sausages_from_kaldi_sausages_string(sausage_text)
    sau_trans_pair_short = SausagesTranscriptPair.create_from_sausages_sentence(sau, transcript_text_short)
    aligner = SausagesTranscriptAligner()
    aligner.get_lexicon_dict_from_cmu_file()
    aligned_short = aligner.align_without_word_repeat(sau_trans_pair_short, "1")
    try:
        assert len(aligned_short.sausages) == len(aligned_short.wordlist)
    except AssertionError:
        print(Fore.RED + "Sausage and transcript are not of same length after alignment"
                         "when sausages length is more than transcript length")
        return False
    print(aligned_short.get_sausages_sentence())
    sau_trans_pair_long = SausagesTranscriptPair.create_from_sausages_sentence(sau, transcript_text_long)
    aligned_long = aligner.align_without_word_repeat(sau_trans_pair_long, "1")
    try:
        assert len(aligned_long.sausages) == len(aligned_long.wordlist)
    except AssertionError:
        print(Fore.RED + "Sausage and transcript are not of same length after alignment"
                         "when sausages length is less than transcript length")
        return False

    print(Fore.GREEN + "Test passed: " + test_aligned_sausages_word_pair_length.__name__)
    return True


if __name__ == "__main__":
    test_aligned_sausages_word_pair_length()
