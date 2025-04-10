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

    # Sentiment analysis
    score = SentimentIntensityAnalyzer().polarity_scores(clean_text)
    neg = score['neg']
    pos = score['pos']
    neu = score['neu']

    # Determine sentiment
    sentiment = "Neutral Sentiment"
    if neg > pos:
        sentiment = "Negative Sentiment"
    elif pos > neg:
        sentiment = "Positive Sentiment"

    # Map sentiment to basic emotions
    if pos > 0.5:
        emotion = "Overall Satisfied"
    elif neg > 0.5:
        emotion = "Overall Dissatisfied"
    elif neu > 0.5:
        emotion = "Calm Emotions"
    else:
        emotion = "Mixed Emotions"

    # Display results
    result_text.set(f"Sentiment: {sentiment}\n\nEmotion: {emotion}")

# GUI setup
root = tk.Tk()
root.title("Review Analyzer")
root.geometry("600x500")  # Set window size

# Styles
title_font = ("Helvetica", 16, "bold")
label_font = ("Helvetica", 12)
button_font = ("Helvetica", 12, "bold")
result_font = ("Helvetica", 12)
bg_color = "#f0f0f0"
button_color = "#4CAF50"
button_text_color = "white"

root.configure(bg=bg_color)

# Title
tk.Label(root, text="Review Analyzer", font=title_font, bg=bg_color).pack(pady=10)

# Input label and text box
tk.Label(root, text="Enter your review:", font=label_font, bg=bg_color).pack(pady=5)
review_input = tk.Text(root, height=12, width=60, font=("Helvetica", 10))
review_input.pack(pady=10)

# Analyze button
analyze_button = tk.Button(
    root, text="Analyze", font=button_font, bg=button_color, fg=button_text_color, command=analyze_review
)
analyze_button.pack(pady=10)

# Result label
result_text = tk.StringVar()
result_label = tk.Label(
    root, textvariable=result_text, font=result_font, justify="left", wraplength=500, bg=bg_color
)
result_label.pack(pady=20)

root.mainloop()

