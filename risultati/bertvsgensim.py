### GENSIM ######################################################################################################
import gensim
import gensim.downloader as api

dataset = api.load("text8")
data = [d for d in dataset]

def tagged_document(list_of_list_of_words):
   for i, list_of_words in enumerate(list_of_list_of_words):
      yield gensim.models.doc2vec.TaggedDocument(list_of_words, [i])
data_training = list(tagged_document(data))

model = gensim.models.doc2vec.Doc2Vec(vector_size=768, min_count=2, epochs=30)

model.build_vocab(data_training)
model.train(data_training, total_examples=model.corpus_count, epochs=model.epochs)

def getBertGensim(text):
    return model.infer_vector(text)


### TENSORFLOW ######################################################################################################
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text

bert_preprocess_model = hub.KerasLayer('https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3')
bert_model = hub.KerasLayer('https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-12_H-128_A-2/1')


def getBert(text):
#    text_preprocessed = bert_preprocess_model([normalizeTweet(text)])
    text_preprocessed = bert_preprocess_model([text])
    bert_results = bert_model(text_preprocessed)
    return bert_results["pooled_output"][0, :]


### CONFRONTO ######################################################################################################

start = time.time()
getBert("In 2005, Lionel Messi won the U20 World Cup with Argentina, picking up the Golden Boot and the Golden Ball. In 2022, he won the World Cup with Argentina, picking up the Golden Ball. 17 years is the longest gap between a player winning each tournament.")
print("time elapsed: " + str(time.time()-start))
start = time.time()
getBertGensim("In 2005, Lionel Messi won the U20 World Cup with Argentina, picking up the Golden Boot and the Golden Ball. In 2022, he won the World Cup with Argentina, picking up the Golden Ball. 17 years is the longest gap between a player winning each tournament.".split(" "))
print("time elapsed: " + str(time.time()-start))

### OUTPUT ######################################################################################################
#BERT
time elapsed: 0.2937498092651367
#GENSIM doc2vec
time elapsed: 0.002297639846801758