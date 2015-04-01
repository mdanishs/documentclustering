from os import listdir, makedirs
from os.path import join, isfile
from unicodedata import normalize
from collections import Counter
import codecs

class FeatureExtraction(object):
    """Gets features from the list of files and returns the required format"""
    """which is a dictionary of files and their bag of words"""

    def __init__(self, list_of_files):
        self.list_of_files = list_of_files
        self._file_listing = dict()

    def get_bag_of_half_sentences():
        self._file_listing.clear()
        
        

    def get_bag_of_frequent_phrases(self):
        """Gives a dictionary containing list of files and its 10 most common phrases"""

        #list will contain all the files and there phrases
        self._file_listing.clear()

        for f in self.list_of_files:
            all_words_in_file=[]
            for line in self._lines_in_file(f): #for every line in file
                words = line.split()
                for word in words:
                     if len(word.split("/")) > 1:
                        if word.split("/")[1] != 'PU' and word.split("/")[1] != 'PSP':
                            all_words_in_file.append(word) 

            #normalizes the strings i.e. all extracted words in the list
            normal_list = [normalize('NFKC',word) for word in all_words_in_file]

            two_phrases = list() #contains all the possible two consecutive word phrases
            for i in range(len(normal_list)-1):
                two_phrases.append(normal_list[i] + normal_list[i+1]) #gets every next tw word phrase and appends to the list
            
            three_phrases = list() #contains all the possible three consecutive word phrases
            for i in range(len(normal_list)-2):
                three_phrases.append(normal_list[i] + normal_list[i+1]+ normal_list[i+2]) #gets every next three word phrase and appends to the list

            #counts the occurence of each phrase and returns a dictionary of (phrase: count)
            twoc = Counter(two_phrases)
            #gets the 10 most common phrases
            common = twoc.most_common(50)

            #counts the occurence of each phrase and returns a dictionary of (phrase: count)
            threec = Counter(three_phrases)
            #gets the 10 most common phrases
            common.extend(threec.most_common(50))

            #creats a list of words and add them acc to their count in dictionary
            final_phrases = list()
            for i in range(len(common)): #for the number of unique common phrases
                for j in range(common[i][1]): #for i=0 to count of that phrase
                    final_phrases.append(common[i][0]) #add that phrase into the list

            self._file_listing.update({f:final_phrases})

        return self._file_listing

    def get_bag_of_words(self):
        """Gives a dictionary containing list of files and its words"""

        #clear the list of containing files and their counts
        self._file_listing.clear()

        #for all the files in list
        for f in self.list_of_files:
            all_words_in_file=[]
            for line in self._lines_in_file(f): #for every line in file
                words = line.split()
                for word in words:
                    if len(word.split("/")) > 1:
                        if word.split("/")[1] != 'PU' and word.split("/")[1] != 'PSP' and word.split("/")[1] != 'PRP':
                            all_words_in_file.append(word) 

            #normalize the words in the file
            normal_list = [normalize('NFKC',word) for word in all_words_in_file]
                    
            self._file_listing.update({f:normal_list})
        return self._file_listing

    def get_bag_of_nouns_verbs(self):
        """Gives a dictionary containing two list againt every file name
           first containing nouns and second containing verbs"""

        self._file_listing.clear()

        pos_tags_nouns = ['NN', 'NNS', 'NNP', 'NNPS', 'PRP', 'PRP$', 'WP$', 'WP']
        pos_tags_verbs = ['VBF','VBI', 'VBG','VBN', 'VBP', 'VBZ']

        for f in self.list_of_files:
            all_words_in_file=[]
            for line in self._lines_in_file(f): #for every line in file
                words = line.split()
                for word in words:
                     if len(word.split("/")) > 1:
                        if word.split("/")[1] != 'PU' and word.split("/")[1] != 'PSP':
                            all_words_in_file.append(word) 
            
            noun_list = list()
            verb_list = list()
            for word in all_words_in_file:
                parts = word.split("/")
                if len(parts) > 1 :
                    if parts[1] in pos_tags_nouns:
                        word = normalize('NFKC',word)
                        noun_list.append(word)
                    elif parts[1] in pos_tags_verbs:
                        word = normalize('NFKC',word)
                        verb_list.append(word)
            
                    
            self._file_listing.update({f:[noun_list,verb_list]})
        return self._file_listing


    def _lines_in_file(self,filename):
        f = open(filename, "rb")
        for line in f:
            yield line.strip().decode("utf-8")
        f.close()