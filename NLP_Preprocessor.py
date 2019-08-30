from nltk import sent_tokenize, word_tokenize, pos_tag
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

import re


def sentenceSplit(rawText, library = "NLTK"):
    """
    Returns a list of sentences split using the specified library

    @type  rawText: string
    @param rawText: The text string to be seperated into sentences.
    @type  library: string
    @param library: The library to be used to split the sentences

    @rtype:   list(string)
    @return:  list of split sentences 
    """
    sentences = []
    try:
        if library == "NLTK":
            sentences = sent_tokenize(rawText)
        #TODO add in Spacy library
        
        return sentences
    
    except:
        return None
    
    raise Exception("Invalid library condition set")
    


def wordSplit(rawText, library = "NLTK"):
    """
    Returns a list of tokenized words split using the specified library

    @type  rawText: string
    @param rawText: The text string to be seperated into words.
    @type  library: string
    @param library: The library to be used to split the sentences

    @rtype:   list(string)
    @return:  list of split words
    """
    try:
        if library == "NLTK":
            words = word_tokenize(rawText)
        #TODO add in Spacy library
        
        return words
    
    except UnboundLocalError as e:
        raise Exception("Invalid library condition set")
    
    return None
    
def symbolReplacer(rawText,replaceString = "", extraChars = ""):
    """
    Returns text with all non character and non numeric values removed

    @type  rawText: string
    @param rawText: The text string to be cleaned.
    @type  replaceString: string
    @param replaceString: Characters to replace the removed symbols with.
    @type  extraChars: string
    @param extraChars: Extra characters that should not be removed.

    @rtype:   string
    @return:  the text with all symbols removed
    """
    #check for . in the extraChars regex since it causes errors
    if "." in extraChars:
        extraChars = extraChars.replace(".","")
        extraChars = "." + extraChars
        
    regVal = "[^a-zA-Z\d\s" + extraChars + "]"

    text = re.sub(regVal , replaceString, rawText)
    return text
    
    
    
def numberReplacer(rawText,replaceString = "",consecutive = True,extraChars = ""):
    """
    Returns text with all numeric values replaced

    @type  rawText: string
    @param rawText: The text string to be cleaned.
    @type  replaceString: string
    @param replaceString: Characters to replace the removed symbols with.
    @type  consecutive: Boolean
    @param consecutive: Whether to replace consecutive numbers together(True) or seperately (False)
    @type  extraChars: string
    @param extraChars: Extra characters that should not be removed.
    
    @rtype:   string
    @return:  the text with all symbols removed
    """
    
    #check for . in the extraChars regex since it causes errors
    if "." in extraChars:
        extraChars = extraChars.replace(".","")
        extraChars = "." + extraChars
    
    conRegex = ""
    if consecutive:
        conRegex = "+"

    regVal = "[\d" + extraChars + "]" + conRegex

    text = re.sub(regVal,replaceString,rawText)
    
    return text 




def lemmatizeWords(words,utilizeWordType = True):

    """
    Returns text with all numeric values replaced

    @type  rawText: list(string)
    @param rawText: Set of words to be lemmatized.
    @type  consecutive: Boolean
    @param consecutive: Whether to utilize word type (true) or not (false).
    
    @rtype:   list(string)
    @return:  list of words that have been lemmatized
    """

    lemmatizer = WordNetLemmatizer()
    
    if utilizeWordType:
        lemmaWords = [lemmatizer.lemmatize(word, get_wordnet_pos(word)) for word in words]
    else:
        lemmaWords = [lemmatizer.lemmatize(word) for word in words]
    
    return lemmaWords

def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)