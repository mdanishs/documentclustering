from collections import Counter
from math import sqrt

class DocumentRepresentation(object):
    """represents each document in a particular format and returns a similarity table 
        after comparing each document with others for that representation"""


    def __init__(self, file_listing):
        
        #contains list of file and there corresponding features
        self.file_listing = file_listing
        #table to store the values of comparision
        self.table = [[0.0 for j in range(len(self.file_listing))] for i in range(len(self.file_listing))]


    def get_similarity_matrix(self, **kwargs):
        """ Takes data and representation as input parameters 
            data is what type of feature are they
            representation is how to represent those features
            """
        self.table = [[0.0 for j in range(len(self.file_listing))] for i in range(len(self.file_listing))]

        #if frequent phrases or common words are represented as bag of words
        if kwargs['representation'] == 'bow' and (kwargs['data'] == 'bag_of_words' or kwargs['data'] == 'frequent_phrases'):
            for file in self.file_listing:
                self.file_listing[file] = list(set(self.file_listing[file]))
            return self._bag_of_words()

        #if noun and phrases are represented as bag of words
        elif kwargs['representation'] == 'bow' and (kwargs['data'] == 'noun_verb'):
            for file in self.file_listing:
                self.file_listing[file][0] = list(set(self.file_listing[file][0]))
                self.file_listing[file][1] = list(set(self.file_listing[file][1]))
            return self._bag_of_words_nv()

        #if frequent phrases and common words as vectore space model
        elif kwargs['representation'] == 'vsm' and (kwargs['data'] == 'bag_of_words' or kwargs['data'] == 'frequent_phrases'):
            for file in self.file_listing:
                self.file_listing[file] = Counter(self.file_listing[file])
            return self._bag_of_words()

        #if noun verbs are represented as vectore space model
        elif kwargs['representation'] == 'vsm' and (kwargs['data'] == 'noun_verb'):
            for file in self.file_listing:
                self.file_listing[file][0] = Counter(self.file_listing[file][0])
                self.file_listing[file][1] = Counter(self.file_listing[file][1])
            return self._vector_space_model_nv()


        

    def _bag_of_words(self):
        row=0
        for src_file in self.file_listing:
            src_list = self.file_listing[src_file]
            len_src_list = len(src_list)
            col=0
            total_similarity = 0.0
            for cmp_file in self.file_listing:

                if src_file != cmp_file:
                    cmp_list = self.file_listing[cmp_file]
                    same_word_count = 0.0
                    for word in src_list:
                        if word in cmp_list:
                            same_word_count += 1.0
            
                    total_similarity = same_word_count/(len_src_list + len(cmp_list))
                    #print src_file, cmp_file, total_similarity
                    self.table[row][col] = total_similarity
                    #print 'total similarity ' + str(total_similarity) + " | " + str(src_list['total'] + cmp_list['total'])

                else:
                    self.table[row][col] = 1.0
                        
                col += 1
            row += 1
        return self.table

    def _vector_space_model(self):
        row = 0
        for file1 in self.file_listing:

            file1_count = Counter(self.file_listing[file1])

            col = 0
            for file2 in self.file_listing:
                if file1==file2: self.table[row][col]=1
                else:                    
                    file2_count = Counter(self.file_listing[file2])
                    #print file2_count
                    dot = self._dot_product(file1_count, file2_count)
                    similarity = dot/(self._magnitude(file1_count) * self._magnitude(file2_count))
                    self.table[row][col] = similarity
                col+=1
            row+=1
        
        for i in range(len(self.file_listing)):
            for j in range(len(self.file_listing)):
                print self.table[i][j],
            print ""

        return self.table

    def _bag_of_words_nv(self):
        row=0
        for src_file in self.file_listing:
            src_noun_list = list(set(self.file_listing[src_file][0]))
            src_verb_list = list(set(self.file_listing[src_file][1]))

            len_src_noun  = len(src_noun_list)
            len_src_verb  = len(src_verb_list)

            col=0
            
            total_similarity = 0.0
            for cmp_file in self.file_listing:

                if src_file != cmp_file:
                
                    cmp_noun_list = list(set(self.file_listing[cmp_file][0]))
                    cmp_verb_list = list(set(self.file_listing[cmp_file][1]))

                    cmp_src_noun  = len(cmp_noun_list)
                    cmp_src_verb  = len(cmp_verb_list)
                
                    same_noun_count = 0.0
                    same_verb_count = 0.0
                
                    for word in src_noun_list:
                        if word in cmp_noun_list:
                            same_noun_count += 1.0

                    for word in src_verb_list:
                        if word in cmp_verb_list:
                            same_verb_count += 1.0
            
                    noun_similarity = same_noun_count/(len_src_noun + cmp_src_noun)
                    verb_similarity = same_verb_count/(len_src_verb + cmp_src_verb)
                    total_similarity = (noun_similarity+verb_similarity)/2
                    #print src_file, cmp_file, total_similarity
                    self.table[row][col] = total_similarity
                    #print 'total similarity ' + str(total_similarity) + " | " + str(src_list['total'] + cmp_list['total'])
                        
                else:
                    self.table[row][col] = 1.0
                        
                col += 1
            row += 1
        return self.table

    def _vector_space_model_nv(self):
        row = 0
        for file1 in self.file_listing:

            noun_file1_count = Counter(self.file_listing[file1][0])
            verb_file1_count = Counter(self.file_listing[file1][1])

            col = 0
            for file2 in self.file_listing:
                if file1==file2: self.table[row][col]=1
                else:                    
                    noun_file2_count = Counter(self.file_listing[file2][0])
                    #print file2_count
                    noun_dot = self._dot_product(noun_file1_count, noun_file2_count)
                    noun_similarity = noun_dot/(self._magnitude(noun_file1_count) * self._magnitude(noun_file2_count))
                    
                    verb_file2_count = Counter(self.file_listing[file2][1])
                    #print file2_count
                    verb_dot = self._dot_product(verb_file1_count, verb_file2_count)
                    verb_similarity = verb_dot/(self._magnitude(verb_file1_count) * self._magnitude(verb_file2_count))
                    
                    self.table[row][col] = (noun_similarity+verb_similarity)/2
                col+=1
            row+=1
        
        #for i in range(len(self.file_listing)):
        #    for j in range(len(self.file_listing)):
        #        print self.table[i][j],
        #    print ""

        return self.table

    def _dot_product(self, list1,list2):
            dot_product = 0.0
            for feature in list1:
                if feature in list2:
                    dot_product += (list1[feature] * list2[feature])
            return dot_product
    
    def _magnitude(self, vector):
        magnitude = 0.0
        for axes in vector:
            magnitude += vector[axes]**2
        return sqrt(magnitude)

