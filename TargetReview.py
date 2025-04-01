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

# Create the main application window
root = tk.Tk()
root.title("Sentiment Analysis Tool")

# Target input
tk.Label(root, text="Target:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
target_entry = tk.Entry(root, width=50)
target_entry.grid(row=0, column=1, padx=10, pady=5)

# Review input
tk.Label(root, text="Review:").grid(row=1, column=0, padx=10, pady=5, sticky="nw")
review_entry = tk.Text(root, width=50, height=10)
review_entry.grid(row=1, column=1, padx=10, pady=5)

# Analyze button
analyze_button = tk.Button(root, text="Analyze Sentiment", command=analyze_sentiment)
analyze_button.grid(row=2, column=0, columnspan=2, pady=10)

# Result display
result_label = tk.Label(root, text="", wraplength=400, justify="left", fg="blue")
result_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Run the application
root.mainloop()
