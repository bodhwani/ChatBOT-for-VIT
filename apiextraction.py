import pandas as pd,os
import nltk,pickle
os.chdir(os.getcwd())
class apiextraction():
	def __init__(self,filename="",load=""):
		if load!="":
			self.featuresets=self.load()
		else:
			self.filename=filename
			self.training_data=self.process_dataset()
			self.featuresets = [(self.process_sentence(n), intent) for (n, intent) in self.training_data]
			self.featuresets = [ (n, intent) for (n, intent) in self.featuresets if n]
		self.classifier= nltk.NaiveBayesClassifier.train(self.featuresets)
	def save(self):
		pickle.dump(self.featuresets, open( "featuresets", "wb" ) )
	def load(self):
		return pickle.load( open( "featuresets", "rb" ) )
	def process_dataset(self):
		df = pd.read_csv(self.filename)
#		df['Text'][0]
		training_data = []
		for i in range(len(df)):
			training_data.append((df['Text'][i],df['Category'][i]))
		return training_data

	def bag_of_words(self,words):
		return dict([(word, True) for word in words])


	def process_sentence(self,x):
		words = nltk.tokenize.word_tokenize(x.lower()) 
		postag= nltk.pos_tag(words)
		stopwords = nltk.corpus.stopwords.words('english')
		lemmatizer = nltk.WordNetLemmatizer()
		processedwords=[]    
		#Remove Stop words and lemmatize verbs
		for w in postag:
		    if "VB" in w[1]:
		        processedwords.append(lemmatizer.lemmatize(w[0].lower(),'v'))
		    else:
		        processedwords.append(lemmatizer.lemmatize(w[0],'n').lower())
		l=[]
		for w in processedwords:
		    if w.lower()=="not":
		        l.append(w)
		    elif w not in stopwords:
		        if (len(w)>2):
		            l.append(w)
		return self.bag_of_words(l)
    

	def score(self,input_sent):		
		input_sent = input_sent.lower()
		dist = self.classifier.prob_classify(self.process_sentence(input_sent))
		temp=[]
		for label in dist.samples():
		    temp.append((label, dist.prob(label)))
		return temp

	def intent(self,input_sent):
		dist = self.classifier.classify(self.process_sentence(input_sent))
		prob = self.score(input_sent)
#		print ("this is prob",prob)
		prob = sorted(prob,key=lambda x:(-x[1],x[0]))
		if(prob[0][1]<0.5):
			return  "fallback"
		else:
			return dist
'''
if __name__ == "__main__":
	var=apiextraction("","yes")
	input_sent="what is the placement in VIT"
	print(var.intent(input_sent))
'''
