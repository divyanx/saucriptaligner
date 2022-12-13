import shutil
import urllib

import editdistance
import sys
import os
import warnings
import urllib.request
from tqdm.auto import tqdm
from saucriptaligner.sau_text_pair import SausagesTranscriptPair

sys.path.append('../')


class SausagesTranscriptAligner:
    """
    Aligns a pair of transcripts, one from the sausage and one from the
    reference, using the sausage as a guide.
    """

    def __init__(self, lexicon_dict=None, conf2vec=None):
        """
        @param lexicon_dict: a dictionary of lexicon entries
        @type lexicon_dict: dict
        @param conf2vec: a dictionary of confidence scores to vectors
        @type conf2vec: dict
        """
        self.data_dir = "../data"
        self.lexicon_dict = lexicon_dict
        self.conf2vec = conf2vec
        self.score_functions = {
            "1": self.weighted_average_sausage_word_edit_distance
        }

    @staticmethod
    def average_edit_distance(str1: str, str2: str) -> float:
        """
        Compute the average edit distance between two words
        """
        distance = editdistance.eval(str1.split(" "), str2.split(" "))
        return distance / max(len(str1), len(str2))

    def phoneme_edit_distance(self, word1: str | int, word2: str | int) -> float:
        """
        Compute the phoneme edit distance between two words
        """
        try:
            pronunciation1 = self.lexicon_dict[word1]
        except KeyError:
            # print warning
            warnings.warn(f"Word {word1} not found in lexicon continuing with word itself as pronunciation")
            pronunciation1 = word1
        try:
            pronunciation2 = self.lexicon_dict[word2]
        except KeyError:
            # print warning
            warnings.warn(f"Word {word2} not found in lexicon continuing with word itself as pronunciation")
            pronunciation2 = word2

        return SausagesTranscriptAligner.average_edit_distance(pronunciation1, pronunciation2)

    def average_sausage_word_edit_distance(self, edges, word: str) -> float:
        """
        Compute the average edit between a word's phoneme sequence and list of words in a sausage
        """
        words = [edge[0] for edge in edges]
        return sum([self.phoneme_edit_distance(word, w) for w in words]) / len(words)

    def weighted_average_sausage_word_edit_distance(self, edges, word):
        """
        Compute the weighted average edit between a word's phoneme sequence and list of words in a sausage
        """
        words = [edge[0] for edge in edges]
        weights = [edge[1] for edge in edges]
        return sum([self.phoneme_edit_distance(word, w[0]) * w[1] for w in edges]) / sum(weights)

    def align_without_word_repeat(self, sau_and_text: SausagesTranscriptPair, score_func_name: str):

        """
        Align a sausage and a transcript without repeating words in the transcript
        @param sau_and_text: a SausageAndTranscriptPair object
        @type sau_and_text: SausageAndTranscriptPair
        @param score_func_name: function keyword to use score function
        @type score_func_name: str
        @return: a list of tuples of the form (word, sausage)
        """
        score_func = self.score_functions[score_func_name]
        sau, words = sau_and_text.get_sausages_wordlist()
        if len(sau) == 0 or len(words) == 0:
            return []
        # we need custom alignment algorithm which will align words with sausages without repeating words
        # we will use a score calculated by score_func
        # the alignment algorithm will be a dynamic programming algorithm
        # the algorithm with minimum score will be chosen

        # initialize the alignment matrix
        alignment_matrix = [[0. for _ in range(len(words) + 1)] for _ in range(len(sau) + 1)]

        deletion_cost = 1

        # use an iterative dp algorithm to fill the alignment matrix,
        # the algorithm is similar to the one used in the align_with_word_repeat function
        # if length of sausages will be less than length of transcript, we will use deletion_cost
        # deletion will be represented by adding extra sausage in the sausage list
        # substitution cost will be calculated by score_func
        # insertion of null word will be represented by adding "-" in the transcript list
        # cost of insertion will be 1
        # initialize the first row and column

        for i in range(1, len(sau) + 1):
            alignment_matrix[i][0] = alignment_matrix[i - 1][0] + deletion_cost

        for j in range(1, len(words) + 1):
            alignment_matrix[0][j] = alignment_matrix[0][j - 1] + 1

        for i in range(1, len(sau) + 1):
            for j in range(1, len(words) + 1):
                alignment_matrix[i][j] = min(alignment_matrix[i - 1][j] + deletion_cost,
                                             alignment_matrix[i - 1][j - 1] + score_func(sau[i - 1], words[j - 1]),
                                             alignment_matrix[i][j - 1] + 1)

        # now we will use the alignment matrix to get the alignment
        # we will start from the bottom right corner of the matrix
        # we will move to the cell with minimum cost
        # if the cost is same, we will move to the cell with minimum cost

        # initialize the current position
        i = len(sau)
        j = len(words)

        # initialize the current sausage and transcript
        current_sau = []
        current_text = []

        # initialize the current score
        current_score = 0

        # we will move to the cell with minimum cost
        # if the cost is same, we will move to the cell with minimum cost
        while i > 0 and j > 0:
            if alignment_matrix[i][j] == alignment_matrix[i - 1][j] + deletion_cost:
                current_sau.append(sau[i - 1])
                current_text.append("-")
                current_score += deletion_cost
                i -= 1
            elif alignment_matrix[i][j] == alignment_matrix[i - 1][j - 1] + score_func(sau[i - 1], words[j - 1]):
                current_sau.append(sau[i - 1])
                current_text.append(words[j - 1])
                current_score += score_func(sau[i - 1], words[j - 1])
                i -= 1
                j -= 1
            else:
                current_sau.append("-")
                current_text.append(words[j - 1])
                current_score += 1
                j -= 1

        # add the remaining sausages and words to the current sausage and transcript
        while i > 0:
            current_sau.append(sau[i - 1])
            current_text.append("-")
            current_score += deletion_cost
            i -= 1

        while j > 0:
            current_sau.append("-")
            current_text.append(words[j - 1])
            current_score += 1
            j -= 1

        # reverse the current sausage and transcript
        current_sau.reverse()
        current_text.reverse()

        alignment = SausagesTranscriptPair.create_from_sausages_wordlist(current_sau, current_text)

        return alignment

    def set_data_dir(self, data_dir):
        """
        Set the data directory
        @param data_dir: data directory
        @type data_dir: str
        """
        self.data_dir = data_dir

    def load_lexicon_from_cmu_dict(self, cmu_dict_path="http://svn.code.sf.net/p/cmusphinx/code/trunk/cmudict/"):
        """
        Download lexicon from cmu dict
        @param cmu_dict_path: path to cmu dict
        @type cmu_dict_path: str
        """
        # download cmu dict file
        cmu_dict_file = "cmudict-0.7b"
        cmu_dict_file_path = os.path.join(self.data_dir, cmu_dict_file)
        if not os.path.exists(cmu_dict_file_path):
            print("Downloading cmu dict file")

            with tqdm.wrapattr(urllib.request.urlopen(cmu_dict_path + cmu_dict_file), "read", desc=cmu_dict_file,
                               total=int(urllib.request.urlopen(cmu_dict_path + cmu_dict_file).info()['Content-Length'])) as response:
                with open(cmu_dict_file_path, 'wb') as out_file:
                    shutil.copyfileobj(response, out_file)

        # load cmu dict file
        print("Loading cmu dict file")


    def lexicon_dict_from_cmu_file(self):
        """
        Convert cmu dict file to dictionary
        @return: cmu dict dictionary
        @rtype: dict
        """
        cmu_dict_file = "cmudict-0.7b"
        cmu_dict_file_path = os.path.join(self.data_dir, cmu_dict_file)
        cmu_dict = {}
        # check if cmu dict file exists
        if not os.path.exists(cmu_dict_file_path):
            # download cmu dict file
            print("CMU dict file not found.")
            self.load_lexicon_from_cmu_dict()

        with open(cmu_dict_file_path, 'r') as cmu_dict_file:
            for line in cmu_dict_file:
                line = line.strip()
                if line.startswith(";;;"):
                    continue
                word, pron = line.split("  ")
                cmu_dict[word] = pron
        self.lexicon_dict = cmu_dict
        return cmu_dict