import os
import clr
import sys
import traceback
clr.AddReference('System')
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')

from System import *
from System.Drawing import *
from System.Windows.Forms import *
from System import ComponentModel
from FeatureExtraction import FeatureExtraction
from Algorithm import Algorithm
from Evaluation import Evaluation
from DocumentRepresentation import DocumentRepresentation
from string import rfind
from string import digits

class MyForm(Form):
    def __init__(self):
        self.current_level = 1
        self._list_of_files = list()
        self._directory_path = String.Empty
        self._file_listing = dict()
        self._similarity_table = list()
        self._cluster_set = list()
        self._unordered_filelist = list()
        self._all_clusters = None
        # Create child controls and initialize form
        self._tstxtPath = ToolStripTextBox()
        self._tsbtnShowSimilarityMatrix = ToolStripButton()
        self._tsbtnPlay = ToolStripButton()
        self._tsbtnNextLevel = ToolStripButton()
        self._tsbtnPreviousLevel = ToolStripButton()
        self._tsMain = ToolStrip()
        self._tsbtnBrowse = ToolStripButton()
        self._rbStemming = RadioButton()
        self._rbLemmantization = RadioButton()
        self._grpPreProcessing = GroupBox()
        self._rbStopWordRemoval = RadioButton()
        self._colHFMeasure = ColumnHeader()
        self._colHEntropy = ColumnHeader()
        self._listView1 = ListView()
        self._colHPurity = ColumnHeader()
        self._imageList1 = ImageList()
        self._treeView1 = TreeView()
        self._radioButton7 = RadioButton()
        self._rbHAC = RadioButton()
        self._grpAlgorithm = GroupBox()
        self._rbVectorSpaceModel = RadioButton()
        self._rbDefault = RadioButton()
        self._grpDocRepresentation = GroupBox()
        self._statusStrip1 = StatusStrip()
        self._sslblPath = ToolStripStatusLabel()
        self._grpFeatureExtraction = GroupBox()
        self._rbFrequentPhrases = RadioButton()
        self._rbCommonWordsRepeat = RadioButton()
        self._rbNounVerbs = RadioButton()
        self.InitializeComponent()

    def InitializeComponent(self):
        
        #
        # tstxtPath
        #
        self._tstxtPath.Alignment = ToolStripItemAlignment.Right
        self._tstxtPath.Name = "tstxtPath"
        self._tstxtPath.Size = Size(320, 31)
        #
        # tsbtnShowSimilarityMatrix
        #
        self._tsbtnShowSimilarityMatrix.DisplayStyle = ToolStripItemDisplayStyle.Image
        self._tsbtnShowSimilarityMatrix.Image = Image.FromFile("grid.ico")
        self._tsbtnShowSimilarityMatrix.ImageTransparentColor = Color.Magenta
        self._tsbtnShowSimilarityMatrix.Name = "tsbtnShowSimilarityMatrix"
        self._tsbtnShowSimilarityMatrix.Size = Size(28, 28)
        self._tsbtnShowSimilarityMatrix.Text = "toolStripButton1"
        self._tsbtnShowSimilarityMatrix.ToolTipText = "Show Similarity Matrix"
        #
        # tsbtnPlay
        #
        self._tsbtnPlay.DisplayStyle = ToolStripItemDisplayStyle.Image
        self._tsbtnPlay.Image = Image.FromFile("play.ico")
        self._tsbtnPlay.ImageTransparentColor = Color.Magenta
        self._tsbtnPlay.Name = "tsbtnPlay"
        self._tsbtnPlay.Size = Size(28, 28)
        self._tsbtnPlay.ToolTipText = "Play"
        self._tsbtnPlay.Click += self.tsbtnPlay_click
        #
        # tsbtnNextLevel
        #
        self._tsbtnNextLevel.DisplayStyle = ToolStripItemDisplayStyle.Image
        self._tsbtnNextLevel.Image = Image.FromFile("next.png")
        self._tsbtnNextLevel.ImageTransparentColor = Color.Magenta
        self._tsbtnNextLevel.Name = "tsbtnNextLevel"
        self._tsbtnNextLevel.Size = Size(28, 28)
        self._tsbtnNextLevel.ToolTipText = "Next"
        self._tsbtnNextLevel.Click += self.tsbtnNextLevel_click
        #
        # tsbtnPreviousLevel
        #
        self._tsbtnPreviousLevel.DisplayStyle = ToolStripItemDisplayStyle.Image
        self._tsbtnPreviousLevel.Image = Image.FromFile("previous.png")
        self._tsbtnPreviousLevel.ImageTransparentColor = Color.Magenta
        self._tsbtnPreviousLevel.Name = "tsbtnPreviousLevel"
        self._tsbtnPreviousLevel.Size = Size(28, 28)
        self._tsbtnPreviousLevel.ToolTipText = "Next"
        self._tsbtnPreviousLevel.Click += self.tsbtnPreviousLevel_click
        #
        # tsMain
        #
        self._tsMain.BackColor = SystemColors.Control
        self._tsMain.ImageScalingSize = Size(24, 24)
        self._tsMain.Items.AddRange(Array[ToolStripItem]([self._tsbtnPlay,
	        self._tsbtnShowSimilarityMatrix,
	        self._tsbtnBrowse,
	        self._tstxtPath,
            self._tsbtnPreviousLevel, 
            self._tsbtnNextLevel]))
        self._tsMain.Location = Point(0, 0)
        self._tsMain.Name = "tsMain"
        self._tsMain.Size = Size(682, 31)
        self._tsMain.Stretch = True
        self._tsMain.TabIndex = 17
        self._tsMain.Text = "toolStrip1"
        #
        # tsbtnBrowse
        #
        self._tsbtnBrowse.Alignment = ToolStripItemAlignment.Right
        self._tsbtnBrowse.DisplayStyle = ToolStripItemDisplayStyle.Image
        self._tsbtnBrowse.Image = Image.FromFile("folder.ico")
        self._tsbtnBrowse.ImageTransparentColor = Color.Magenta
        self._tsbtnBrowse.Margin = Padding(0, 1, 10, 2)
        self._tsbtnBrowse.Name = "tsbtnBrowse"
        self._tsbtnBrowse.Size = Size(28, 28)
        self._tsbtnBrowse.Text = "tsbtnBrowse"
        self._tsbtnBrowse.Click += self.tsbtnBrowse_click
        #
        # rbStemming
        #
        self._rbStemming.AutoSize = True
        self._rbStemming.Location = Point(8, 67)
        self._rbStemming.Name = "rbStemming"
        self._rbStemming.Size = Size(71, 17)
        self._rbStemming.TabIndex = 2
        self._rbStemming.TabStop = True
        self._rbStemming.Text = "Stemming"
        self._rbStemming.UseVisualStyleBackColor = True
        #
        # rbLemmantization
        #
        self._rbLemmantization.AutoSize = True
        self._rbLemmantization.Location = Point(8, 43)
        self._rbLemmantization.Name = "rbLemmantization"
        self._rbLemmantization.Size = Size(98, 17)
        self._rbLemmantization.TabIndex = 1
        self._rbLemmantization.TabStop = True
        self._rbLemmantization.Text = "Lemmantization"
        self._rbLemmantization.UseVisualStyleBackColor = True
        #
        # grpPreProcessing
        #
        self._grpPreProcessing.Controls.Add(self._rbStemming)
        self._grpPreProcessing.Controls.Add(self._rbLemmantization)
        self._grpPreProcessing.Controls.Add(self._rbStopWordRemoval)
        self._grpPreProcessing.Location = Point(12, 44)
        self._grpPreProcessing.Name = "grpPreProcessing"
        self._grpPreProcessing.Size = Size(290, 100)
        self._grpPreProcessing.TabIndex = 12
        self._grpPreProcessing.TabStop = False
        self._grpPreProcessing.Text = "Pre Processing"
        #
        # rbStopWordRemoval
        #
        self._rbStopWordRemoval.AutoSize = True
        self._rbStopWordRemoval.Location = Point(8, 19)
        self._rbStopWordRemoval.Name = "rbStopWordRemoval"
        self._rbStopWordRemoval.Size = Size(121, 17)
        self._rbStopWordRemoval.TabIndex = 0
        self._rbStopWordRemoval.TabStop = True
        self._rbStopWordRemoval.Text = "Stop Word Removal"
        self._rbStopWordRemoval.UseVisualStyleBackColor = True
        #
        # colHFMeasure
        #
        self._colHFMeasure.Text = "F-Measure"
        self._colHFMeasure.Width = 99
        #
        # colHEntropy
        #
        self._colHEntropy.Text = "Entropy"
        self._colHEntropy.Width = 90
        #
        # listView1
        #
        self._listView1.Columns.AddRange(Array[ColumnHeader]([self._colHPurity,
	        self._colHEntropy,
	        self._colHFMeasure]))
        self._listView1.FullRowSelect = True
        self._listView1.HideSelection = False
        self._listView1.Location = Point(12, 435)
        self._listView1.Name = "listView1"
        self._listView1.Size = Size(290, 75)
        self._listView1.TabIndex = 16
        self._listView1.UseCompatibleStateImageBehavior = False
        self._listView1.View = View.Details
        #
        # colHPurity
        #
        self._colHPurity.Text = "Purity"
        self._colHPurity.Width = 92
        #
        # imageList1
        #
        self._imageList1.TransparentColor = Color.Transparent
        self._imageList1.Images.Add("folder",Icon("folder.ico"))
        self._imageList1.Images.Add("grid",Icon("grid.ico"))
        self._imageList1.Images.Add("play",Icon("play.ico"))
        self._imageList1.Images.Add("file",Icon("file.ico"))
        #
        # treeView1
        #
        self._treeView1.FullRowSelect = True
        self._treeView1.HotTracking = True
        self._treeView1.ImageIndex = 0
        self._treeView1.ImageList = self._imageList1
        self._treeView1.Location = Point(327, 44)
        self._treeView1.Name = "treeView1"
        self._treeView1.SelectedImageIndex = 0
        self._treeView1.Size = Size(345, 466)
        self._treeView1.TabIndex = 15
        #
        # radioButton7
        #
        self._radioButton7.AutoSize = True
        self._radioButton7.Location = Point(7, 43)
        self._radioButton7.Name = "radioButton7"
        self._radioButton7.Size = Size(85, 17)
        self._radioButton7.TabIndex = 1
        self._radioButton7.TabStop = True
        self._radioButton7.Text = "radioButton7"
        self._radioButton7.UseVisualStyleBackColor = True
        #
        # rbHAC
        #
        self._rbHAC.AutoSize = True
        self._rbHAC.Location = Point(7, 19)
        self._rbHAC.Name = "rbHAC"
        self._rbHAC.Size = Size(47, 17)
        self._rbHAC.TabIndex = 0
        self._rbHAC.TabStop = True
        self._rbHAC.Text = "HAC"
        self._rbHAC.UseVisualStyleBackColor = True
        #
        # grpAlgorithm
        #
        #self._grpAlgorithm.Controls.Add(self._radioButton7)
        self._grpAlgorithm.Controls.Add(self._rbHAC)
        self._grpAlgorithm.Location = Point(12, 345)
        self._grpAlgorithm.Name = "grpAlgorithm"
        self._grpAlgorithm.Size = Size(289, 71)
        self._grpAlgorithm.TabIndex = 14
        self._grpAlgorithm.TabStop = False
        self._grpAlgorithm.Text = "Algorithm"
        #
        # rbVectorSpaceModel
        #
        self._rbVectorSpaceModel.AutoSize = True
        self._rbVectorSpaceModel.Location = Point(7, 43)
        self._rbVectorSpaceModel.Name = "rbVectorSpaceModel"
        self._rbVectorSpaceModel.Size = Size(122, 17)
        self._rbVectorSpaceModel.TabIndex = 1
        self._rbVectorSpaceModel.TabStop = True
        self._rbVectorSpaceModel.Text = "Vector Space Model"
        self._rbVectorSpaceModel.UseVisualStyleBackColor = True
        #
        # rbDefault
        #
        self._rbDefault.AutoSize = True
        self._rbDefault.Location = Point(7, 20)
        self._rbDefault.Name = "rbDefault"
        self._rbDefault.Size = Size(59, 17)
        self._rbDefault.TabIndex = 0
        self._rbDefault.TabStop = True
        self._rbDefault.Text = "Bag of Words"
        self._rbDefault.UseVisualStyleBackColor = True
        #
        # grpDocRepresentation
        #
        self._grpDocRepresentation.Controls.Add(self._rbVectorSpaceModel)
        self._grpDocRepresentation.Controls.Add(self._rbDefault)
        self._grpDocRepresentation.Location = Point(12, 150)
        self._grpDocRepresentation.Name = "grpDocRepresentation"
        self._grpDocRepresentation.Size = Size(289, 74)
        self._grpDocRepresentation.TabIndex = 13
        self._grpDocRepresentation.TabStop = False
        self._grpDocRepresentation.Text = "Document Representation"
        #
        # statusStrip1
        #
        self._statusStrip1.Items.AddRange(Array[ToolStripItem]([self._sslblPath]))
        self._statusStrip1.Location = Point(0, 515)
        self._statusStrip1.Name = "statusStrip1"
        self._statusStrip1.Size = Size(682, 22)
        self._statusStrip1.TabIndex = 18
        self._statusStrip1.Text = "statusStrip1"
        #
        # sslblPath
        #
        self._sslblPath.Name = "sslblPath"
        self._sslblPath.Size = Size(97, 17)
        self._sslblPath.Text = "No Path Selected"
        #
        # grpFeatureExtraction
        #
        self._grpFeatureExtraction.Controls.Add(self._rbNounVerbs)
        self._grpFeatureExtraction.Controls.Add(self._rbCommonWordsRepeat)
        self._grpFeatureExtraction.Controls.Add(self._rbFrequentPhrases)
        self._grpFeatureExtraction.Location = Point(12, 230)
        self._grpFeatureExtraction.Name = "grpFeatureExtraction"
        self._grpFeatureExtraction.Size = Size(290, 109)
        self._grpFeatureExtraction.TabIndex = 19
        self._grpFeatureExtraction.TabStop = False
        self._grpFeatureExtraction.Text = "Feature Extraction"
        #
        # rbCommonWordsUnique
        #
        self._rbFrequentPhrases.Location = Point(8, 19)
        self._rbFrequentPhrases.Name = "rbFrequentPhrases"
        self._rbFrequentPhrases.Size = Size(176, 24)
        self._rbFrequentPhrases.TabIndex = 0
        self._rbFrequentPhrases.TabStop = True
        self._rbFrequentPhrases.Text = "Frequent Phrases"
        self._rbFrequentPhrases.UseVisualStyleBackColor = True
        #
        # rbCommonWordsRepeat
        #
        self._rbCommonWordsRepeat.Location = Point(8, 49)
        self._rbCommonWordsRepeat.Name = "rbCommonWordsRepeat"
        self._rbCommonWordsRepeat.Size = Size(197, 24)
        self._rbCommonWordsRepeat.TabIndex = 1
        self._rbCommonWordsRepeat.TabStop = True
        self._rbCommonWordsRepeat.Text = "Common Words"
        self._rbCommonWordsRepeat.UseVisualStyleBackColor = True
        #
        # rbNounVerbs
        #
        self._rbNounVerbs.Location = Point(8, 79)
        self._rbNounVerbs.Name = "rbNounVerbs"
        self._rbNounVerbs.Size = Size(176, 24)
        self._rbNounVerbs.TabIndex = 2
        self._rbNounVerbs.TabStop = True
        self._rbNounVerbs.Text = "Nouns and Verbs"
        self._rbNounVerbs.UseVisualStyleBackColor = True
        #
        # MainForm
        #
        self.BackColor = SystemColors.ControlLight
        self.ClientSize = Size(682, 537)
        self.Controls.Add(self._grpFeatureExtraction)
        self.Controls.Add(self._statusStrip1)
        self.Controls.Add(self._tsMain)
        self.Controls.Add(self._grpPreProcessing)
        self.Controls.Add(self._listView1)
        self.Controls.Add(self._treeView1)
        self.Controls.Add(self._grpAlgorithm)
        self.Controls.Add(self._grpDocRepresentation)
        self.FormBorderStyle = FormBorderStyle.FixedDialog
        self.MaximizeBox = False
        self.Name = "MainForm"
        self.Text = "FYPWindowsForms"

    def _populate_tree(self,cluster_list):
        
        node = self._to_tree_nodes(cluster_list)
        self._treeView1.Nodes.Add(node)
        self._treeView1.ExpandAll()
    
    def tsbtnBrowse_click(self,sender,event_args):
        fd = FolderBrowserDialog()
        msg = fd.ShowDialog(self)
        
        self._directory_path = fd.SelectedPath
        self._tstxtPath.Text = self._directory_path
        self._sslblPath.Text = self._tstxtPath.Text

    def tsbtnNextLevel_click(self, sender, event_args):
        self.current_level+=1
        self._treeView1.Nodes.Clear()
        self._populate_tree(self._all_clusters[self.current_level][0])

        purity = str(self._all_clusters[self.current_level][1] )
        entropy = str(self._all_clusters[self.current_level][2])
        self._add_list_items(purity,entropy)
        

    def tsbtnPreviousLevel_click(self, sender, event_args):
        self.current_level-=1
        self._treeView1.Nodes.Clear()
        self._populate_tree(self._all_clusters[self.current_level][0])

        purity = str(self._all_clusters[self.current_level][1] )
        entropy = str(self._all_clusters[self.current_level][2])
        self._add_list_items(purity,entropy)
        

    def tsbtnPlay_click(self, sender, event_args):
        self._treeView1.Nodes.Clear()
        
        del self._list_of_files[0:] #delete all files in list of files

        self._find_files(self._directory_path,self._list_of_files) #finds all files recursively in the given path

        if len(self._list_of_files) == 0: #although doesn't work, but was meant to give an error message if no path selected
            MessageBox.Show("No files were found in the specified directory","Empty Dataset",MessageBoxButtons.OK,MessageBoxIcon.Exclamation)
        else:
            data_type = '' #to pass as an argument, to tell what type of data is in file listing

            #extracting features from the files can be based on 
            #frequent two word phrases
            #only words
            #noun and verbs
            feature_extraction = FeatureExtraction(self._list_of_files)
            if self._rbFrequentPhrases.Checked:
                self._file_listing = feature_extraction.get_bag_of_frequent_phrases()
                data_type = 'frequent_phrases'
            elif self._rbCommonWordsRepeat.Checked:
                self._file_listing = feature_extraction.get_bag_of_words()
                data_type = 'bag_of_words'
            elif self._rbNounVerbs.Checked:
                self._file_listing = feature_extraction.get_bag_of_nouns_verbs()
                data_type = 'noun_verb'

            #for key in self._file_listing:
            #    MessageBox.Show(str(self._file_listing[key]))
            
            document_representation = DocumentRepresentation(self._file_listing)
            if self._rbDefault.Checked:
                self._similarity_table = document_representation.get_similarity_matrix(representation = 'bow', data=data_type)
            elif self._rbVectorSpaceModel.Checked:
                self._similarity_table = document_representation.get_similarity_matrix(representation = 'vsm', data=data_type)

            for key in self._file_listing:
                self._unordered_filelist.append(key)

            algorithm = Algorithm(self._similarity_table,self._unordered_filelist, self._list_of_files)
            if self._rbHAC.Checked:
                self._cluster_set = algorithm.hierarchical_agglomerative_clustering()
            lst = algorithm.get_clusters_by_max_purity()
            #MessageBox.Show(str(self._cluster_set))
            #MessageBox.Show(str(lst))

            self._all_clusters = algorithm.get_clusters_at_all_levels()

            try:
                EvaluationMainObject = Evaluation()
                EvaluationMainObject.SetCluterList(lst)
                EvaluationMainObject.SetValueOfR()
                EvaluationMainObject.SetDocumentDictionary(self._list_of_files)
                EvaluationMainObject.CalculateIndividualPurity()
                purity = EvaluationMainObject.GetTotalPurity()
                EvaluationMainObject.CalculateEntropy()
                entropy = EvaluationMainObject.GetTotalEntropy()

                self._add_list_items(str(purity),str(entropy))
            except DivideByZeroException:
                MessageBox.Show("Division By Zero")
            
            self._populate_tree(lst)
            #MessageBox.Show(str(lst))

    def _add_list_items(self,purity,entropy):
        lvItem = ListViewItem(str(purity))
        lvItem.SubItems.Add(str(entropy))
        self._listView1.Items.Add(lvItem)

    def _find_files(self,path,file_list):
        lst = os.listdir(path)
        for element in lst:
            if os.path.isdir(path + "/" + element):
                self._find_files(path + "/" + element,file_list)
            elif (path + "/" + element) not in file_list:
                file_list.append(path + "/" + element)

    def _to_tree_nodes(self,lst):
        """docs of same cluster are in this dict"""

        nodes = dict()
        for tuple in lst:
            node = TreeNode(str(tuple[0]) + " - " + str(tuple[2]),self._imageList1.Images.IndexOfKey("file"),self._imageList1.Images.IndexOfKey("file"))
            if tuple[1] not in nodes:
                nodes.update({tuple[1]:[node]})
            else:
                nodes[tuple[1]].append(node)

        node = list()    
        for key in nodes:
            node.append( TreeNode("Cluster" + str(key), Array[TreeNode]([x for x in nodes[key]])))
        print node

        root = TreeNode("Clusters",Array[TreeNode]([x for x in node]))

        return root




Application.EnableVisualStyles()
Application.SetCompatibleTextRenderingDefault(False)

form = MyForm()
Application.Run(form)
 