class SausagesTranscriptPair:
    """
    This class stores sausages and corresponding transcript
    """
    def __init__(self, sausages, wordlist):
        self.sausages = sausages
        self.wordlist = wordlist

    @staticmethod
    def create_from_sausages_wordlist(sausages, wordlist):
        return SausagesTranscriptPair(sausages, wordlist)

    @staticmethod
    def create_from_sausages_sentence(sausages, wordlist):
        wordlist = wordlist.split()
        return SausagesTranscriptPair(sausages, wordlist)


class Sausages:
    """
    Sausages is a linear graph of alternate words.
    Sausage is generated from ASR word lattice
    """

    def __init__(self, edges_array, to_sort=False):
        self.sausages = []
        for edges in edges_array:
            if not to_sort:
                self.sausages.append(Sausage.create_from_edges(edges, is_reverse_sorted=to_sort))

    @staticmethod
    def create_from_edges_array(edges_array, is_edges_reverse_sorted=False):
        """
        Create Sausages from linear graph
        """
        return Sausages(edges_array, to_sort=is_edges_reverse_sorted)

    def __iter__(self):
        return iter(self.sausages)

    def __len__(self):
        return len(self.sausages)

    def __getitem__(self, index):
        return self.sausages[index]

    def __setitem__(self, index, value):
        self.sausages[index] = value

    def __delitem__(self, index):
        del self.sausages[index]

    def __str__(self):
        return str(self.sausages)

    def __repr__(self):
        return repr(self.sausages)

    def __eq__(self, other):
        return self.sausages == other.sausages



class Sausage:
    """
    Edges between two adjacent nodes form a single sausage
    Each edge has a score and a word.
    Sausage is represented as a list of edges
    """

    def __init__(self, edges, to_sort=True):
        # sort edges by weight in descending order
        if to_sort:
            self.edges = sorted(edges, key=lambda x: x.weight, reverse=True)
        self.edges = edges

    @staticmethod
    def create_from_edges(edges: [[str, float]], is_reverse_sorted=True):
        """
        Create a sausage from a list of edges

        @param edges: list of edges in the sausage
        @type edges: [[str, float]]
        @param is_reverse_sorted: whether the edges are sorted in descending order
        @type is_reverse_sorted: bool
        """
        return Sausage(edges, to_sort=not is_reverse_sorted)

    @staticmethod
    def create_from_words_weights(words: [str], weights: [float], is_reverse_sorted=True):
        """
        Create a sausage from a list of words and weights

        @param words: list of words in the sausage
        @type words: [str]
        @param weights: list of weights in the sausage
        @type weights: [float]
        """
        edges = []
        for word, weight in zip(words, weights):
            edges.append([word, weight])
        return Sausage(edges, to_sort=not is_reverse_sorted)

    def get_words(self):
        """
        Get the words in the sausage
        """
        return [edge[0] for edge in self.edges]

    def get_weights(self):
        """
        Get the weights in the sausage
        """
        return [edge[1] for edge in self.edges]

    def get_edges(self):
        """
        Get the edges in the sausage
        """
        return self.edges

    def __iter__(self):
        return iter(self.edges)

    def __len__(self):
        return len(self.edges)

    def __getitem__(self, index):
        return self.edges[index]

    def __str__(self):
        return str(self.edges)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.edges == other.edges

    def __hash__(self):
        return hash(tuple(self.edges))

    def __add__(self, other):
        return Sausage(self.edges + other.edges, to_sort=True)
