from string import rfind
from string import digits
from Evaluation import Evaluation

class Algorithm:
    """Gives a cluster list after running HAC"""
    def __init__(self,similarity_table,unordered_filelist, list_of_files):

        self._list_of_files = list_of_files

        #given as parameter, this is result of document representation
        self.table=similarity_table

        #the clusters are represented as regular expressions
        #final regular expression is the string representation of cluster_list
        self.cluster_list = list()

        #a cluster is represented as [[1,2],3]
        #all the hierarchy that group at a certain level is maintained in this cluster_dict
        #this keeps height as key and cluster formed at that hieght as its value
        self.cluster_dict = dict()

        #contains the indexed filenames
        #each filename is given a particular id
        self.unordered_filelist = unordered_filelist

        #contains the classes we have in our dataset
        self.classes = list()
        for name in self.unordered_filelist:
            cls = name[:rfind(name, "/")]
            cls = cls[rfind(cls, "/")+1:]
            if cls not in self.classes:
                self.classes.append(cls)
        self.class_count = len(self.classes)


    def hierarchical_agglomerative_clustering(self):
        """ implements hac and returns a regular expression of clustering result"""

        is_done = False #boolean to check if algo has completed
        clust_id = 1; #actually works as cluster height, this is used as key in cluster_dict
        while not is_done:
            #self.print_table()
            largest = -1
            #a tuple contains pair of x, y at which largest value is found
            index=()
            for x in range(len(self.table)):
                for y in range(len(self.table)):
                    #cheks if the two documents are not same
                    #and they have not been checked before
                    #and whether the current number is greater than previous greater (i.e above defined largest)
                    if (self.table[x][y]!=1 and self.table[y][x]!=1) and self.table[x][y] > largest:
                        largest = self.table[x][y]
                        index = (x,y)
            
            #if valid index is available
            if index:

                x,y = index

                #these variables are used to find the clusters uptil now,
                #in which document y and document x exist
                #and store the clust_id in respective variables
                x_index = y_index = -1
                
                #one shows that two docs are now combined as one cluster in table
                self.table[x][y] = self.table[y][x] = 1 
                #finds y in clusters
                for i in range(len(self.cluster_list)):
                    if self._is_value_in_cluster(self.cluster_list[i], index[0]) == True:
                        y_index = i
                        break

                #finds x in clusters
                for i in range(len(self.cluster_list)):
                    if self._is_value_in_cluster(self.cluster_list[i], index[1]) == True:
                        x_index = i
                        break

                #if both documents are still not in the cluster
                #create their cluster and add that to clust_dict
                if y_index == -1 and x_index == -1:
                    self.cluster_list.append([x,y])
                    self.cluster_dict.update({clust_id:[x,y]})
                    clust_id += 1
                
                #x and y are closest docs
                #x is already part of some cluster
                #find that cluster and add y to it at a new height
                elif y_index == -1:
                    self.cluster_list[x_index] = [self.cluster_list[x_index],[x]]
                    self.cluster_dict.update({clust_id:self.cluster_list[x_index]})
                    clust_id += 1

                #y and x are closest docs
                #y is already part of some cluster
                #find that cluster and add x to it at a new height
                elif x_index == -1:
                    self.cluster_list[y_index] = [self.cluster_list[y_index],[y]]
                    self.cluster_dict.update({clust_id:self.cluster_list[y_index]})
                    clust_id += 1

                #if both of them are part of different clusters
                #combine those clusters in one at a new height
                elif not x_index == -1 and not y_index == -1:
                    if not x_index == y_index:
                        #merge the two clusters if both are already selected before
                        a = self.cluster_list[x_index]
                        b = self.cluster_list[y_index]
                        self.cluster_list.remove(a)
                        self.cluster_list.remove(b)
                        self.cluster_list.append([a,b])
                        self.cluster_dict.update({clust_id:[a,b]})
                        clust_id += 1
                
                #makeing all the columns and rows of x,y same
                #so that they can be treated as identical docs
                #becuase they are combined in a single cluster now
                for i in range(len(self.table)):
                    if(self.table[x][i] > self.table[y][i]):
                        if not self.table[y][i] == 1: self.table[y][i] = self.table[x][i]
                        if not self.table[i][y] == 1:self.table[i][y] = self.table[x][i]
                    else:
                        if not self.table[x][i] == 1:self.table[x][i] = self.table[y][i]
                        if not self.table[i][x] == 1:self.table[i][x] = self.table[y][i]
            
            #if no valid index is available then all docs are combined
            else: is_done = True

        #add the final cluster as the last level in the clust_dict
        self.cluster_dict.update({clust_id:self.cluster_list})

        return self.cluster_list

    def get_clusters_by_class_count(self):
        """gets clusters at each level and return the list which maches the number of classes in the dataset"""

        #for every class in classes
        for i in range(self.class_count):
            #cuts the dendrogram at certain level and return the cluster list for that level
            lst = self.get_cluster_list_at_level(i+1)

            #getting the number of different clusters 
            clusters = list()
            for doc in lst:
                if doc[1] not in clusters: clusters.append(doc[1])
            if len(clusters) >= self.class_count: return lst

    def get_clusters_by_max_purity(self):
        purity = 0

        #for every class in classes
        for i in range(len(self.cluster_dict)):
            #cuts the dendrogram at certain level and return the cluster list for that level
            lst = self.get_cluster_list_at_level(i+1)

            EvaluationMainObject = Evaluation()
            EvaluationMainObject.SetCluterList(lst)
            EvaluationMainObject.SetValueOfR()
            EvaluationMainObject.SetDocumentDictionary(self._list_of_files)
            EvaluationMainObject.CalculateIndividualPurity()
            new_purity = EvaluationMainObject.GetTotalPurity()

            if purity < new_purity and purity<1:
                purity = new_purity
                final_list = lst
        return final_list

    def get_clusters_at_all_levels(self):
        "returns a dictionary with level as key, and tuple as value containing clusters, purity and entropy"
        cluster_list = dict()

        for i in range(len(self.cluster_dict)):
            #cuts the dendrogram at certain level and return the cluster list for that level
            lst = self.get_cluster_list_at_level(i+1)

            EvaluationMainObject = Evaluation()
            EvaluationMainObject.SetCluterList(lst)
            EvaluationMainObject.SetValueOfR()
            EvaluationMainObject.SetDocumentDictionary(self._list_of_files)
            EvaluationMainObject.CalculateIndividualPurity()
            purity = EvaluationMainObject.GetTotalPurity()
            EvaluationMainObject.CalculateEntropy()
            entropy = EvaluationMainObject.GetTotalEntropy()

            cluster_list.update({i+1:(lst,purity,entropy)})
        return cluster_list




    def get_cluster_list_at_level(self,level_c):
        #for c in self.cluster_dict:
        #    print str(c) + " " + str(self.cluster_dict[c])
        
        level = level_c
        level = len(self.cluster_dict)-(level-1)
        docs = list()
        #cut at a particular level
        clusters_at_level = list()

        if not isinstance(self.cluster_dict[level][0],list):
            #clusters_at_level.append(self.cluster_dict[level])
            for x in self.cluster_dict[level]:
                clusters_at_level.append([x])
            docs.extend(self.cluster_dict[level])
        else:
            clusters_at_level.extend(self.cluster_dict[level])

        print self._get_docs_in_cluster(self.cluster_list)
        
        for i in range(level-1,0,-1):
            #get all docs at that particular level
            docs = self._get_docs_in_cluster(clusters_at_level)

            #search clusters on levels below
            #if docs in them are not in docs
            #add those clusters in clusters
            new_clust = self.cluster_dict[i+1]
            docs_in_new_clust = self._get_docs_in_cluster(new_clust)
            for doc in docs_in_new_clust:
                if doc not in docs:
                    clusters_at_level.append(new_clust)
                    docs.extend(docs_in_new_clust)

        all_docs = self._get_docs_in_cluster(self.cluster_list)
        for doc in all_docs:
            if doc not in docs:
                docs.append(doc)
                clusters_at_level.append([doc])

        print ""
        lst = []
        cluster_num = 0
        for cluster in clusters_at_level:
            cluster_num += 1
            documents = self._get_docs_in_cluster(cluster)
            for doc in documents:
                name = self.unordered_filelist[int(doc)]
                cls = name[:rfind(name, "/")]
                cls = cls[rfind(cls, "/")+1:]
                name = name[rfind(name, "/")+1:]
                lst.append((name,cluster_num,cls))
        return lst

        

    def _is_value_in_cluster(self, cluster, value):
        ''' function checks whether the current document has already been selected for the cluster set. '''
        if value in cluster:
            return True
        else:
            return any(self._is_value_in_cluster(element,value) for element in cluster if isinstance(element, list))
        
    def _get_docs_in_cluster(self, cluster):
        docs = list()
        reg_ex = str(cluster)
        i = 0
        while i in range(len(reg_ex)):
            if reg_ex[i] in digits:
                index = ""
                while reg_ex[i] in digits:
                    index += reg_ex[i]
                    i+=1
                docs.append(int(index))
            else: i+=1
        return docs