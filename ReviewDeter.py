import string
from collections import Counter
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
import tkinter as tk
from tkinter import messagebox

def analyze_review():
    reviewText = review_input.get("1.0", tk.END).strip()
    if not reviewText:
        messagebox.showerror("Error", "Please enter a review.")
        return

    lower_case = reviewText.lower()
    clean_text = lower_case.translate(str.maketrans('', '', string.punctuation))

    token_text = word_tokenize(clean_text, "english")

    # Remove stop words from tokenized text
    deter_text = [word for word in token_text if word not in stopwords.words('english')]

    # Lemmatization
    lemma_words = [WordNetLemmatizer().lemmatize(word) for word in deter_text]

    # Emotion analysis
    emotion_list = []
    with open('emotion.txt', 'r') as emofile:
        for line in emofile:
            clear_line = line.replace('\n', '').replace(',', '').replace("'", '').strip()
            word, emotion = clear_line.split(':')
            if word in lemma_words:
                emotion_list.append(emotion)

    emotion_counts = Counter(emotion_list)
     # Debug: Print matched emotions for verification
    print("Matched emotions:", emotion_list)

    # Sentiment analysis
    score = SentimentIntensityAnalyzer().polarity_scores(clean_text)
    neg = score['neg']
    pos = score['pos']
    sentiment = "Neutral Sentiment"
    if neg > pos:
        sentiment = "Negative Sentiment"
    elif pos > neg:
        sentiment = "Positive Sentiment"

    # Display results
    result_text.set(f"Sentiment: {sentiment}\n\nEmotions: {dict(emotion_counts)}")

# GUI setup
root = tk.Tk()
root.title("Review Analyzer")

tk.Label(root, text="Enter your review:").pack(pady=5)
review_input = tk.Text(root, height=10, width=50)
review_input.pack(pady=5)

analyze_button = tk.Button(root, text="Analyze", command=analyze_review)
analyze_button.pack(pady=5)

result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, justify="left", wraplength=400)
result_label.pack(pady=10)

root.mainloop()

