import pandas as pd
import nltk,pickle
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
		dist = self.classifier.prob_classify(process_sentence(input_sent))
		for label in dist.samples():
		    print("%s: %f" % (label, dist.prob(label)))

	def intent(self,input_sent):
		dist = self.classifier.classify(self.process_sentence(input_sent))
		return dist

if __name__ == "__main__":
	var=apiextraction("dataset.csv")
	input_sent="what is the placement in VIT"
	print(var.intent(input_sent))
