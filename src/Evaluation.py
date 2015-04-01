# Created by Mohammad Ayub - K102247

from __future__ import division
import string
import unicodedata
import operator
import math
import os

class Evaluation(object):
    """description of class"""
    def __init__(self, **VariablesContainer):
        self.VariablesOfObjectData = VariablesContainer
        self._q = 3 # Saves the total number of classes in the total dataset, right now it is hard coded will be changed
        self._n = list() # It saves total number of documents of "ith" class in "rth" cluster.
                         # Its a list because we have various number of clusters

        self._nr = {} # It saves the number of documents in the rth cluster.
                          # # Its a list because we have various number of clusters

        self._r = list() # Saves the number of clusters. If at the end of the clustering algorithm we got 5 clusters, it
                        # will save 1, 2, 3, 4 & 5.
        self._TotalNumberOfDocuments = 0
        self._individualentropy = list()
        self._totalentropy = 0.0
        self._individualpurity = list()
        self._totalpurity = 0.0
        self._ClusterSet = list()
        self._DocumentDictionary = dict()
        self.NumberOfDocumentsOfParticularClass = dict()
        self.MaxNofDocumentOfIClassInCluster = dict()
        self.ResultOfMultiForSummision = list()
        #self._DocumentCategoryDictionary = dict()
        #self.Counter = {}
        # = self.VariablesOfObjectData.get('cluster_list')
        print 'I am exiting the Constructor'
        #for objects in self:
        #    print objects
        #print(self)
        #print 'The variables of object data printing'
        #for key in self.VariablesOfObjectData:
        #    print(key)
    
    # The function sets the total number of Documents in the dataset
    def SetTotalNumberOfDocuments(self):
        self._q = len(self._DocumentDictionary.keys())

        for ListOfValues in self._DocumentDictionary.values():
            self._TotalNumberOfDocuments += len(ListOfValues)

    ''' This Fubction lets you set the Document Classes and the documents under it '''
    def SetDocumentDictionary(self, ListOfFiles):
        for DocumentPath in ListOfFiles:
            StringPath = ''
            StringPath = DocumentPath.encode('ascii', 'ignore')
            TempVarForStoringPathWithoutSlashes = StringPath.rsplit('/')
            
            if self._DocumentDictionary.get(TempVarForStoringPathWithoutSlashes[-2]) != None:
                self._DocumentDictionary[TempVarForStoringPathWithoutSlashes[-2]].append(TempVarForStoringPathWithoutSlashes[-1])
            else:
                self._DocumentDictionary[TempVarForStoringPathWithoutSlashes[-2]] = [TempVarForStoringPathWithoutSlashes[-1]]
        #print(self._DocumentDictionary)
        self.SetTotalNumberOfDocuments()

    def SetValueOfR(self):
        ClusterNumbers = list()
        
        for ClusterTupple in self._ClusterSet:
            ClusterNumbers.append(ClusterTupple[1])

        for ClusterNumber in ClusterNumbers:
            Present = False
            while not Present:
                try:
                    self._r.index(ClusterNumber)
                    Present = True
                except ValueError:
                    self._r.append(ClusterNumber)

    def SetCluterList(self, List):
        self._ClusterSet = List

    def CalculateIndividualPurity(self):
        count = 0
        #.............................................#
        # ** Calculating NR, number of documents in the Rth cluster ** #
        for ClusterNumber in self._r:
            count = 0
            #print(ClusterNumber)
            for ClusterTupple in self._ClusterSet:
                if ClusterTupple[1] == ClusterNumber:
                    count += 1
                    self._nr[ClusterNumber] = count
        #..............................................#
        # ** END OF FINDING NR ** #

        #..............................................#
        # ** Now Finding N^i`r which is the number of documents of ith class in the Rth cluster ** #
        for ClusterNumber in self._r:
            for DocumentCategoryFromDictionary in self._DocumentDictionary:
                    self.NumberOfDocumentsOfParticularClass[DocumentCategoryFromDictionary] = 0
            for ClusterTupple in self._ClusterSet:
                if ClusterTupple[1] == ClusterNumber:
                    DocumentNameInCluster = ClusterTupple[0]
                    #print(DocumentNameInCluster)
                    ClassOfDocumentInCluster = self.FindClassOfDocument(DocumentNameInCluster)
                    count = self.NumberOfDocumentsOfParticularClass.get(ClassOfDocumentInCluster)
                    #print(count)
                    self.NumberOfDocumentsOfParticularClass[ClassOfDocumentInCluster] = count + 1
            TempKeyValueList = self.NumberOfDocumentsOfParticularClass.values()
            self.MaxNofDocumentOfIClassInCluster[ClusterNumber] = max(TempKeyValueList)
        #..............................................#
        # ** END OF N^i`r ** #

        #..............................................#
        # ** Calculating and setting individual purity values for all clusters ** #
        for ClusterNumber in self._r:
            TempVariableForPurityCalculation = 1 / self._nr.get(ClusterNumber)
            TempVariableForPurityCalculation = TempVariableForPurityCalculation * self.MaxNofDocumentOfIClassInCluster.get(ClusterNumber)
            self._individualpurity.append(TempVariableForPurityCalculation)
        self.CalculateTotalPurity()

    def FindClassOfDocument(self, DocumentName):
        #print("In the Fucntion")
        DocumentNameAscii = DocumentName.encode('ascii', 'ignore')

        for DocumentCategoryFromDictionary, DocumentNameFromDictionary in self._DocumentDictionary.items():
            for DocumentNameTemp in DocumentNameFromDictionary:
                #print("______________")
                #print(DocumentNameTemp)
                if DocumentNameTemp == DocumentNameAscii:
                    #print(DocumentNameTemp)
                    #print(DocumentNameAscii)
                    #print("______________")
                    #print("Got It")
                    return DocumentCategoryFromDictionary

    def CalculateTotalPurity(self):
        #print(self._nr)
        #print(self._r)
        #print(self._individualpurity)
        for ClusterNumber in self._r:
            TempVar = self._nr.get(ClusterNumber) / self._TotalNumberOfDocuments
            TempVar = TempVar * self._individualpurity[ClusterNumber - 1]
            self._totalpurity = self._totalpurity + TempVar
    
        print("--------------------------PURITY RESULT------------------------")
        print("Purity of the Documents Cluster is:")
        print(self._totalpurity)

    def GetTotalPurity(self):
        return self._totalpurity
    
    def GetTotalEntropy(self):
        return self._totalentropy

    def CalculateEntropy(self):
        self.CalculateIndividualEntropy()

    def CalculateIndividualEntropy(self):
        LogOfQ = -1 * (1 / math.log(self._q))
        i = 0
        for ClusterNumber in self._r:
            for DocumentCategoryFromDictionary in self._DocumentDictionary:
                    self.NumberOfDocumentsOfParticularClass[DocumentCategoryFromDictionary] = 0
            for ClusterTupple in self._ClusterSet:
                if ClusterTupple[1] == ClusterNumber:
                    DocumentNameInCluster = ClusterTupple[0]
                    ClassOfDocumentInCluster = self.FindClassOfDocument(DocumentNameInCluster)
                    count = self.NumberOfDocumentsOfParticularClass.get(ClassOfDocumentInCluster)
                    self.NumberOfDocumentsOfParticularClass[ClassOfDocumentInCluster] = count + 1
            for Key in self.NumberOfDocumentsOfParticularClass:
                DivisionResultOfNIRNR = self.NumberOfDocumentsOfParticularClass.get(Key)
                DivisionResultOfNIRNR = DivisionResultOfNIRNR / self._nr.get(ClusterNumber)
                if DivisionResultOfNIRNR > 0:
                    LogOfDivisionResultOfNIRNR = math.log(DivisionResultOfNIRNR)
                else:
                    LogOfDivisionResultOfNIRNR = 0
                MultiplicationOfLogAndDivisionResults = DivisionResultOfNIRNR * LogOfDivisionResultOfNIRNR
                self.ResultOfMultiForSummision.append(MultiplicationOfLogAndDivisionResults)
            #print(self.ResultOfMultiForSummision)
            SummOfNIRandItsLog = sum(self.ResultOfMultiForSummision)
            MultiplicationOfQandSumm = LogOfQ * SummOfNIRandItsLog
            #print(MultiplicationOfQandSumm)
            #print(ClusterNumber)
            #os.system("pause")
            self._individualentropy.append(MultiplicationOfQandSumm)
        print(self._individualentropy)
        self.CalculateTotalEntropy()

    def CalculateTotalEntropy(self):
        for ClusterNumber in self._r:
            self._totalentropy = self._totalentropy + ((self._nr.get(ClusterNumber) / self._TotalNumberOfDocuments) * self._individualentropy[ClusterNumber - 1])
        print("--------------------------ENTROPY RESULT------------------------")
        print("Entropy of the Documents Cluster is:")
        print(self._totalentropy)
            