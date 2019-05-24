import nltk
#nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from allennlp.data.tokenizers.word_tokenizer import WordTokenizer
from allennlp.data.tokenizers.word_filter import WordFilter, StopwordFilter
from allennlp.data.tokenizers.word_stemmer import WordStemmer, PorterStemmer
from allennlp.data.tokenizers.token import Token
import allennlp.data.dataset_readers.semantic_dependency_parsing as sdp
from allennlp.predictors.predictor import Predictor

sid = SentimentIntensityAnalyzer()
ps = PorterStemmer()

for line in open('drive/My Drive/Chatbot/food.txt'):
  food = line.rstrip('\n')
  food_list.append(food)
  food_list.append(food+"s")
  
predictor = Predictor.from_path("drive/My Drive/Chatbot/srl-model-2018.05.25.tar.gz")
dependency_predictor = Predictor.from_path("drive/My Drive/Chatbot/biaffine-dependency-parser-ptb-2018.08.23.tar.gz")
items = []

class FoodItem:
  def __init__(self, name, quantity, attributes):
    self.name = name
    self.quantity = quantity
    self.attributes = attributes
  def to_string(self):
    string = str(self.quantity)
    for a in self.attributes:
      string += " "
      string += a
    for n in self.name:
      string += " "
      string += n
    return string
   

def filter_for_food(string):
  global food_list, dependency_predictor, items
  result = dependency_predictor.predict(sentence=string)
  words = result['words']
  part_of_speech = result ['pos']
  attributes = []
  name = []
  for index in range(len(words)):
    pos = part_of_speech[index]
    if pos == "DT":
      if words[index] == "a" or words[index] == "an":
        quantity = 1
    if pos == "CD":
      quantity = words[index]
    if pos == "JJ" or pos == "JJR" or pos == "JJS":
      attributes.append(words[index])
    if pos == "NN" or pos == "NNS" or pos == "NNP" or pos == "NNPS":
      name.append(words[index])
    if pos == "," or pos == "." or pos == "CC":
      if len(name) != 0:
        for n in name:
          if n in food_list:
            item = FoodItem(name,quantity,attributes)
            items.append(item)
            attributes = []
            name = []
            break
  for n in name:
    if n in food_list:
      item = FoodItem(name,quantity,attributes)
      items.append(item)
      attributes = []
      name = []
      break
    
def process():
  global command, partial_response, ss, sid, predictor, items
  ss = sid.polarity_scores(command)
  response = ""
  if partial_response == False:
      result=predictor.predict(command)
      for dictionary in result['verbs']:
        verb = dictionary['verb']
        token = Token(text=verb)
        token=ps.stem_word(token)
        if token.text == 'order':
          if ss['compound'] >= 0.0 and ss['compound'] <= 0.5 and ss['neu'] > ss['pos']:
            try:
              response = dictionary['description']
              response=response.split('ARG1: ')[1].split(']')[0]
              filter_for_food(response)
              partial_order = ""
              for item in items:
                partial_order += " "
                partial_order += item.to_string()
                partial_order += ","
              response="Would you like me to order: "+partial_order.rstrip(",")+"? <Yes/No/I also want to order...>"
              partial_response = True
            except:
              print("We did an oopsie here")
          else:
            response="If you want me to order some food, try: @Starter Bot I want to order <<food>>"
  else:
      if "Yes" in command:
        response="I will order then: "+partial_order
      elif "No" in command:
        response="Order canceled"
      else:
        result=predictor.predict(command)
        for dictionary in result['verbs']:
          verb = dictionary['verb']
          token = Token(text=verb)
          token=ps.stem_word(token)
          if token.text == 'order':
            if ss['compound'] >= 0.0 and ss['compound'] <= 0.5 and ss['neu'] > ss['pos']:
              try:
                response = dictionary['description']
                response=response.split('ARG1: ')[1].split(']')[0]
                filter_for_food(response)
                partial_order = ""
                for item in items:
                  partial_order += " "
                  partial_order += item.to_string()
                  partial_order += ","
                response="Would you like me to order: "+partial_order.rstrip(",")+"? <Yes/No/I also want to order...>"
              except:
                print("We did an oopsie here")
            else:
              response="If you want me to order some more, try: @Starter Bot I want to order <<food>>"
  return response

partial_response = False
command="I want to order a pizza and tell me how is the weather"
result=process()
print(result)

command="I would like to order 3 cats"
result=process()
print(result)

command="I would also like to order 4 large portions of french fries, 2 hot coffees and two cheeseburgers"
result=process()
print(result)
