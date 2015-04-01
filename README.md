# Document Clustering
Document Clustering, implemented a hierarchical agglomerative clustering approach, a machine learning approach which groups similar documents based on their context.

#How It Works
The Urdu Document Clustering system works in layers.

####Feature Extraction
In the first layer features are extracted from the data set. These features include (i) Common words, (ii) Frequent Phrases and (iii) Common nouns and Common verbs. The extracted features are then represented in the second layer.

####Feature Representation
The second layer documents are represented in one of two methods.
I.	Vector Space Model:
Document are represented as vectors and every word is considered as a dimension of the vector.
II.	Bag of Words:
The words of the documents are stored in a list with a list of words against every document. The list also contains the number of times each word occurs in the document.

####Algorithm
Similarity is generated according to the above mentioned which is then passed on to the main algorithm for clustering.
The main clustering algorithm works on the third layer. The algorithm we used is the Hierarchical Agglomerative Clustering (HAC). This algorithm works in a hierarchical fashion. There are two approaches in the Hierarchical Clustering Algorithms.
i.	Top Down:
This approach considers the whole data set as one single cluster and splits clusters recursively until individual documents are reached
ii.	Bottom up:
This approach considers every document as a single cluster and successively merges (or Agglomerates) pairs of clusters until they all are clustered into one single cluster that contains all the documents.
We have use the Bottom up approach which is actually called the Hierarchical Agglomerative Clustering in our project.

####Evaluation
The fourth layer evaluates the quality of the clusters produced by the third layer. We used entropy and purity as the quality measures of the clusters produced in third layer.

###Technologies Used
*Python 2.7
*Iron Python 2.7
