import pandas as pd
import pyphen
#lexicons =  pandas.read_csv('/gdrive/My Drive/GP Training/lexicon.tsv', index_col=1, skiprows=1)


lexicons = {}
with open("/gdrive/My Drive/GP Training/lexicon.tsv") as f:
    for line in f:
        (key, val) = line.split()
        lexicons[key.lower()] = val

dic = pyphen.Pyphen(lang='en')    
print(lexicons)
################################################Train########################
words=[]
labels=[]
features=np.zeros(3)
with open("/gdrive/My Drive/GP Training/cwi_training.txt") as f:
    for line in f:
        sentence,word,number,complexity = line.split("\t")
        word=word.lower()
        if word in lexicons: 
            lexicon=lexicons[word]
        else:
            if complexity==1:
                lexicon=4 
            else:
                 lexicon=1 
          
        letters = len(word)
        syllables = dic.inserted(word).count('-') + 1 
        words.append(word)
        labels.append(complexity)
        features=np.vstack( (features , [ float(lexicon),int(letters),int(syllables) ])  )
        

features=features[1:,:]
print(features)
nnclf = MLPClassifier(solver='sgd', alpha=1e-5, learning_rate='adaptive'  ,activation='tanh', max_iter=1500, random_state=1 , validation_fraction=0.2)
nnclf.fit(features, labels)

svmclf = svm.SVC(gamma='scale')
svmclf.fit(features, labels)

############################################################  TEST #########################################################################33

testfeatures=np.zeros(3)
testlabels=[]
testwords=[]

with open("/gdrive/My Drive/GP Training/cwi_testing_annotated.txt") as f:
    for line in f:
        sentence,word,number,complexity = line.split("\t")
        word=word.lower()
        if word in lexicons: 
            lexicon=lexicons[word]
        else:
            lexicon=2.5
          
        letters = len(word)
        syllables = dic.inserted(word).count('-') + 1 
        testwords.append(word)
        testlabels.append(complexity)
        testfeatures=np.vstack( (testfeatures , [float(lexicon),int(letters),int(syllables)])  )
        
testfeatures=testfeatures[1:,:]       
nnpredictions= nnclf.predict(testfeatures)
print( np.sum(nnpredictions==testlabels)/len(testlabels) )

svmpredictions=svmclf.predict(testfeatures)
print( np.sum(svmpredictions==testlabels)/len(testlabels) )





        
