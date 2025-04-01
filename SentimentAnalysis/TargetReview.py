import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
import tkinter as tk
from tkinter import messagebox

def ensure_nltk_resources():
    """
    Ensure necessary NLTK resources are downloaded.
    """
    try:
        nltk.download('vader_lexicon', quiet=True)
        nltk.download('punkt', quiet=True)
    except Exception as e:
        messagebox.showerror("NLTK Error", f"Failed to download NLTK resources: {e}")

# Call this function at the start of the program
ensure_nltk_resources()

def preprocess_review(review):
    """
    Preprocess the review text by tokenizing and cleaning it.
    """
    # Tokenize the review
    tokens = word_tokenize(review)
    # Convert to lowercase and remove non-alphanumeric tokens
    tokens = [token.lower() for token in tokens if token.isalnum()]
    return tokens

def extract_target_context(target, review):
    """
    Extract sentences or phrases containing the target from the review.
    """
    sentences = nltk.sent_tokenize(review)
    target_context = []
    
    for sentence in sentences:
        if target.lower() in sentence.lower():
            # Tokenize the sentence and extract words around the target
            words = word_tokenize(sentence)
            target_index = next((i for i, word in enumerate(words) if word.lower() == target.lower()), None)
            if target_index is not None:
                # Extract a window of words around the target (e.g., 3 words before and after)
                start = max(0, target_index - 3)
                end = min(len(words), target_index + 4)
                target_context.append(" ".join(words[start:end]))
    
    return " ".join(target_context)

def determine_sentiment(target, review):
    """
    Determine the sentiment towards a specific target in a review.
    """
    try:
        # Extract context related to the target
        target_context = extract_target_context(target, review)
        
        if not target_context:
            return f"The target '{target}' is not mentioned in the review."
        
        # Perform sentiment analysis on the extracted context
        sia = SentimentIntensityAnalyzer()
        sentiment_scores = sia.polarity_scores(target_context)
        
        # Determine overall sentiment
        if sentiment_scores['compound'] > 0:
            sentiment = "positive"
        elif sentiment_scores['compound'] < 0:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        return f"The sentiment towards '{target}' is {sentiment}."
    except Exception as e:
        return f"Error during sentiment analysis: {e}"

def analyze_sentiment():
    """
    Analyze sentiment based on user input from the GUI.
    """
    target = target_entry.get()
    review = review_entry.get("1.0", tk.END).strip()
    
    if not target or not review:
        messagebox.showerror("Input Error", "Please provide both target and review.")
        return
    
    result = determine_sentiment(target, review)
    result_label.config(text=result)

# GUI setup
root = tk.Tk()
root.title("Target Review Analyzer")
root.geometry("600x500")

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
tk.Label(root, text="Target Review Analyzer", font=title_font, bg=bg_color).pack(pady=10)

# Target input
tk.Label(root, text="Target:", font=label_font, bg=bg_color).pack(pady=5)
target_entry = tk.Entry(root, width=50, font=("Helvetica", 10))
target_entry.pack(pady=5)

# Review input
tk.Label(root, text="Review:", font=label_font, bg=bg_color).pack(pady=5)
review_entry = tk.Text(root, width=60, height=10, font=("Helvetica", 10))
review_entry.pack(pady=10)

# Analyze button
analyze_button = tk.Button(
    root,
    text="Analyze Sentiment",
    command=analyze_sentiment,
    font=button_font,
    bg=button_color,
    fg=button_text_color
)
analyze_button.pack(pady=10)

# Result display
result_label = tk.Label(
    root,
    text="",
    font=result_font,
    wraplength=500,
    justify="left",
    bg=bg_color
)
result_label.pack(pady=20)

# Run the application
root.mainloop()
