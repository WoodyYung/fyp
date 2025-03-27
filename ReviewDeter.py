import string
from collections import Counter
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer

reviewText = input("Enter review: ") 
lower_case = reviewText.lower() 
clean_text = lower_case.translate(str.maketrans('','',string.punctuation))

token_text = word_tokenize(clean_text,"english")
#print(token_text)

# remove stop words from tokenized text
deter_text = []
for word in token_text:
    if word not in stopwords.words('english'):
        deter_text.append(word)

#print(deter_text)

# emotion analysis
emotion_list = []
with open ('emotion.txt','r') as emofile:
    for line in emofile:
        # remove extra space and puncuations
        clear_line = line.replace('\n','').replace(',','').replace("'",'').strip()
        # store words
        word, emotion = clear_line.split(':')
        #print("Text: "+ word + " " + "Emotion: " + emotion)

        # check if word is present
        if word in deter_text:
            emotion_list.append(emotion)

print(emotion_list)
w = Counter(emotion_list)
print(w)

def sentiment_analyze(sentiment_text):
    score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
    print(score)

sentiment_analyze(clean_text)
# plot emotions on graph

fig , axl = plt.subplots()
axl.bar(w.keys(),w.values())
fig.autofmt_xdate()
plt.savefig('pie.png')
plt.show()