import editdistance


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
        self.lexicon_dict = lexicon_dict
        self.conf2vec = conf2vec

    @staticmethod
    def average_edit_distance(str1, str2):
        """
        Compute the average edit distance between two words
        """
        distance = editdistance.eval(str1, str2)
        return distance / max(len(str1), len(str2))

    def phoneme_edit_distance(self, word1, word2):
        """
        Compute the phoneme edit distance between two words
        """
        pronunciation1 = self.lexicon_dict[word1]
        pronunciation2 = self.lexicon_dict[word2]
        return SausagesTranscriptAligner.average_edit_distance(pronunciation1, pronunciation2)

    @staticmethod
    def average_sausage_word_edit_distance(edges, word):
        """
        Compute the average edit between a word and list of words in a sausage
        """
        words = [edge[0] for edge in edges]
        return sum([SausagesTranscriptAligner.average_edit_distance(word, w) for w in words]) / len(words)

    @staticmethod
    def weighted_average_sausage_word_edit_distance(edges, word):
        """
        Compute the weighted average edit between a word and list of words in a sausage
        """
        words = [edge[0] for edge in edges]
        weights = [edge[1] for edge in edges]
        return sum([SausagesTranscriptAligner.average_edit_distance(word, w) * w for w in words]) / sum(weights)