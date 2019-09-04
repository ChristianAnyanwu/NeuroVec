import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import TruncatedSVD
from sklearn.decomposition import PCA

def distinct_words(corpus):
    """ Determine a list of distinct words for the corpus.
        Params:
            corpus (list of list of strings): corpus of documents
        Return:
            corpus_words (list of strings): list of distinct words across the corpus, sorted (using python 'sorted' function)
            num_corpus_words (integer): number of distinct words across the corpus
    """
    corpus_words = []
    num_corpus_words = -1
    
    # ------------------
    # Write your implementation here.
    corpus_words = [y for x in corpus for y in x]
    corpus_words = sorted(set(corpus_words))
    num_corpus_words = len(corpus_words)
    # ------------------

    return corpus_words, num_corpus_words

def compute_co_occurrence_matrix(corpus, window_size=4):
    """ Compute co-occurrence matrix for the given corpus and window_size (default of 4).
    
        Note: Each word in a document should be at the center of a window. Words near edges will have a smaller
              number of co-occurring words.
              
              For example, if we take the document "START All that glitters is not gold END" with window size of 4,
              "All" will co-occur with "START", "that", "glitters", "is", and "not".
    
        Params:
            corpus (list of list of strings): corpus of documents
            window_size (int): size of context window
        Return:
            M (numpy matrix of shape (number of corpus words, number of corpus words)): 
                Co-occurence matrix of word counts. 
                The ordering of the words in the rows/columns should be the same as the ordering of the words given by the distinct_words function.
            word2Ind (dict): dictionary that maps word to index (i.e. row/column number) for matrix M.
    """
    words, num_words = distinct_words(corpus)
    M = None
    word2Ind = {}
    
    # ------------------
    # Write your implementation here.
    count = 0
    for word in words:
        word2Ind[word] = count
        count += 1
        
    M = np.zeros((num_words,num_words))
    
    for sentence in corpus:
        for x in range(len(sentence)):
            word = sentence[x]
            surroundings = sentence[max(0,x-window_size):min(len(sentence),x+window_size+1)]
            #print(surroundings,max(0,x-window_size),min(x+window_size+1,flatCorpusLen))
            
            for contextWord in surroundings:
                M[word2Ind[word]][word2Ind[contextWord]] +=1

    for word in word2Ind:
        M[word2Ind[word]][word2Ind[word]] = 0
    # ------------------

    return M, word2Ind

def reduce_to_k_dim(M, k=2):
    """ Reduce a co-occurence count matrix of dimensionality (num_corpus_words, num_corpus_words)
        to a matrix of dimensionality (num_corpus_words, k) using the following SVD function from Scikit-Learn:
            - http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.TruncatedSVD.html
    
        Params:
            M (numpy matrix of shape (number of corpus words, number of corpus words)): co-occurence matrix of word counts
            k (int): embedding size of each word after dimension reduction
        Return:
            M_reduced (numpy matrix of shape (number of corpus words, k)): matrix of k-dimensioal word embeddings.
                    In terms of the SVD from math class, this actually returns U * S
    """    
    n_iters = 10     # Use this parameter in your call to `TruncatedSVD`
    M_reduced = None
    print("Running Truncated SVD over %i words..." % (M.shape[0]))
    
    # ------------------
    # Write your implementation here.
    #svd =  TruncatedSVD(n_components=k, n_iter=n_iters, random_state=42)
    svd = PCA(n_components=k, random_state=42)
    M_reduced = svd.fit_transform(M)

    # ------------------

    print("Done.")
    return M_reduced

def plot_embeddings(M_reduced, word2Ind, words):
    """ Plot in a scatterplot the embeddings of the words specified in the list "words".
        NOTE: do not plot all the words listed in M_reduced / word2Ind.
        Include a label next to each point.
        
        Params:
            M_reduced (numpy matrix of shape (number of unique words in the corpus , k)): matrix of k-dimensioal word embeddings
            word2Ind (dict): dictionary that maps word to indices for matrix M
            words (list of strings): words whose embeddings we want to visualize
    """

    # ------------------
    # Write your implementation here.


    for i,word in enumerate(words):
        x = M_reduced[word2Ind[word]][0]
        y = M_reduced[word2Ind[word]][1]
        plt.scatter(x, y, marker='x', color='red')
        plt.text(x, y, word, fontsize=9)
    plt.show()


def readWordFiles(location):
        print("Loading files")
        wordSentences = []
        files = glob.glob(location)
        for file in files:
            with open(file, 'rb') as f:
                x = pickle.load(f)
                wordSentences.extend(x)

        print("Creating Vectors")
        #creating vectors
        M_co_occurrence, word2Ind_co_occurrence = compute_co_occurrence_matrix(wordSentences)
        M_reduced_co_occurrence = reduce_to_k_dim(M_co_occurrence, k=2)

        # Rescale (normalize) the rows to make them each of unit-length
        M_lengths = np.linalg.norm(M_reduced_co_occurrence, axis=1)
        M_normalized = M_reduced_co_occurrence / M_lengths[:, np.newaxis] # broadcasting
        
        print("visualizing words")
        words = list(word2Ind_co_occurrence.keys())[0:30]
        plot_embeddings(M_normalized, word2Ind_co_occurrence, words)