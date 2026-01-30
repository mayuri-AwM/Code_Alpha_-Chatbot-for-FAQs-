"""
FAQ Matcher Module
Uses NLTK for text preprocessing and cosine similarity for matching user questions to FAQs
Model: TF-IDF (Term Frequency-Inverse Document Frequency) + Cosine Similarity
"""

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string
import numpy as np

# Download required NLTK data
def download_nltk_data():
    """Download necessary NLTK resources"""
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
    
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)
    
    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        nltk.download('wordnet', quiet=True)
    
    try:
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        nltk.download('punkt_tab', quiet=True)

# Initialize NLTK components
download_nltk_data()
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

class FAQMatcher:
    """
    FAQ Matching class using TF-IDF and Cosine Similarity
    
    Model Explanation:
    - TF-IDF: Converts text to numerical vectors based on term importance
    - Cosine Similarity: Measures similarity between question vectors (0-1 scale)
    """
    
    def __init__(self, faqs):
        """
        Initialize the FAQ matcher with a list of FAQs
        
        Args:
            faqs: List of tuples (id, question, answer, category)
        """
        self.faqs = faqs
        self.questions = [faq[1] for faq in faqs]  # Extract questions
        self.answers = [faq[2] for faq in faqs]    # Extract answers
        self.categories = [faq[3] for faq in faqs] # Extract categories
        
        # Preprocess all FAQ questions
        self.processed_questions = [self.preprocess_text(q) for q in self.questions]
        
        # Initialize TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.vectorizer.fit_transform(self.processed_questions)
    
    def preprocess_text(self, text):
        """
        Preprocess text using NLTK
        Steps: Lowercase -> Tokenize -> Remove punctuation -> Remove stopwords -> Lemmatize
        
        Args:
            text: Input text string
            
        Returns:
            Preprocessed text string
        """
        # Convert to lowercase
        text = text.lower()
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove punctuation and stopwords, then lemmatize
        processed_tokens = [
            lemmatizer.lemmatize(token) 
            for token in tokens 
            if token not in string.punctuation and token not in stop_words
        ]
        
        # Join tokens back into string
        return ' '.join(processed_tokens)
    
    def find_best_match(self, user_question, threshold=0.3):
        """
        Find the best matching FAQ for a user question using cosine similarity
        
        Args:
            user_question: User's input question
            threshold: Minimum similarity score (0-1) to consider a match
            
        Returns:
            Dictionary with matched FAQ details or None if no good match
        """
        # Preprocess user question
        processed_question = self.preprocess_text(user_question)
        
        # Convert to TF-IDF vector
        question_vector = self.vectorizer.transform([processed_question])
        
        # Calculate cosine similarity with all FAQ questions
        similarities = cosine_similarity(question_vector, self.tfidf_matrix)[0]
        
        # Find the best match
        best_match_idx = np.argmax(similarities)
        best_similarity = similarities[best_match_idx]
        
        # Check if similarity meets threshold
        if best_similarity < threshold:
            return None
        
        # Return matched FAQ details
        return {
            'question': self.questions[best_match_idx],
            'answer': self.answers[best_match_idx],
            'category': self.categories[best_match_idx],
            'similarity_score': round(best_similarity * 100, 2)  # Convert to percentage
        }
    
    def get_all_categories(self):
        """Get unique categories from FAQs"""
        return list(set(self.categories))
    
    def search_by_category(self, category):
        """
        Get all FAQs in a specific category
        
        Args:
            category: Category name
            
        Returns:
            List of FAQs in that category
        """
        return [
            {'question': q, 'answer': a, 'category': c}
            for q, a, c in zip(self.questions, self.answers, self.categories)
            if c.lower() == category.lower()
        ]

def test_matcher():
    """Test function to demonstrate the FAQ matcher"""
    from init_db import get_all_faqs
    
    # Load FAQs from database
    faqs = get_all_faqs()
    
    # Create matcher
    matcher = FAQMatcher(faqs)
    
    # Test questions
    test_questions = [
        "What sizes are available?",
        "How much time for delivery?",
        "Can I get my money back?",
        "What fabric do you use?",
    ]
    
    print("Testing FAQ Matcher:\n")
    for question in test_questions:
        print(f"Q: {question}")
        result = matcher.find_best_match(question)
        if result:
            print(f"   Match: {result['question']}")
            print(f"   Similarity: {result['similarity_score']}%")
            print(f"   Answer: {result['answer'][:80]}...")
        else:
            print("   No good match found")
        print()

if __name__ == "__main__":
    test_matcher()
