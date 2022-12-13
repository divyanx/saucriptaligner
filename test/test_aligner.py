import sys
from colorama import Fore, Back, Style
from saucriptaligner.sau_text_pair import Sausages, Sausage, SausagesTranscriptPair
from saucriptaligner.align_sau_text_pair import SausagesTranscriptAligner
from utils.create_sausages import sausages_from_kaldi_sausages_string

sys.path.append('../')

sausage_text = "[ <eps> 1 ] [ CAPTAIN 0.9996412 CAPT'N 0.0003587823 ] " \
               "[ CAP 0.6 CAPT'N 0.4 ] [ <eps> 1 ] " \
               "[ FREYER 0.4876702 FRERE 0.4565467 FREYR 0.04838405 FREYER'S 0.001971028 FRIAR 0.001843367 FAIR 0.001418993 FRERES 0.001145516 FRERE'S 0.0003576477 FREER 0.0002653127 FRASER 0.0002230197 FARE 0.0001741726 ] " \
               "[ <eps> 1 ] [ SAYS 1 ] [ <eps> 1 ] [ THATS 1 ] [ <eps> 1 ] [ THE 1 ] [ <eps> 1 ] [ SCENERY 1 ] [ <eps> 1 ] [ IS 0.9900833 AS 0.009916699 ] " \
               "[ <eps> 1 ] [ DELIGHTFUL 1 ] [ <eps> 1 ]"
transcript_text_short = "CAPTAIN FREYER SAYS THAT THE SCENERY IS DELIGHTFUL"
transcript_text_long = "CAPTAIN FREYER SAYS THAT THE SCENERY IS DELIGHTFUL" \
                       " CAPTAIN FREYER SAYS THAT THE SCENERY IS DELIGHTFUL" \
                       " CAPTAIN FREYER SAYS THAT THE SCENERY IS DELIGHTFUL "

pronunciation_dict = {
    "CAPTAIN": "K AE P T AH N",
    "CAPT'N": "K AE P T AH N",
    "CAP" : "K AE P",
    "FREYER": "F R IY ER",
    "FRERE": "F R EH R",
    "FREYR": "F R IY ER",
    "FREYER'S": "F R IY ER Z",
    "FRIAR": "F R IY ER",
    "FAIR": "F EH R",
    "FRERES": "F R EH R Z",
    "FRERE'S": "F R EH R Z",
    "FREER": "F R IY ER",
    "FRASER": "F R EY Z ER",
    "FARE": "F EH R",
    "NO" : "N OW",
    "SAYS": "S EY Z",
    "THAT": "DH AE T",
    "THE": "DH AH",
    "SCENERY": "S K EH N EH R IY",
    "IS": "IH Z",
    "AS": "AE Z",
    "DELIGHTFUL": "D IH L AY T F AH L",
    "<eps>": "<eps>"
}


def test_aligned_sausages_word_pair_length():
    sau = sausages_from_kaldi_sausages_string(sausage_text)
    sau_trans_pair_short = SausagesTranscriptPair.create_from_sausages_sentence(sau, transcript_text_short)
    aligner = SausagesTranscriptAligner(lexicon_dict=pronunciation_dict)
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
              "when sausages lenght is less than transcript length")
        return False
    # print test passed from function name

    print(Fore.GREEN + "Test passed: " + sys._getframe().f_code.co_name)
    return True


if __name__ == "__main__":
    test_aligned_sausages_word_pair_length()





