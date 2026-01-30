# FAQ Chatbot for Online Clothing Brand

A simple and elegant FAQ chatbot built with Streamlit, NLTK, and SQLite. The chatbot uses natural language processing to match user questions with the most relevant FAQs from a clothing brand's knowledge base.

## 🎯 Features

- **Intelligent Question Matching**: Uses TF-IDF and cosine similarity to find the best matching FAQ
- **Natural Language Processing**: NLTK-powered text preprocessing (tokenization, stopword removal, lemmatization)
- **Vibrant UI**: Beautiful light-mode interface with gradient designs
- **Local Storage**: SQLite database for FAQ management
- **25 Pre-loaded FAQs**: Covering sizing, shipping, returns, products, payment, and account questions

## 🧠 Model Used

**TF-IDF (Term Frequency-Inverse Document Frequency) + Cosine Similarity**

- **TF-IDF**: Converts text into numerical vectors based on term importance across documents
- **Cosine Similarity**: Measures the similarity between the user's question and FAQ questions (0-1 scale)
- **Preprocessing Pipeline**: Lowercase → Tokenization → Stopword Removal → Lemmatization

This approach is simple, efficient, and doesn't require training a machine learning model.

## 📁 Project Structure

```
Code_Alpha_-Chatbot-for-FAQs-/
│
├── app.py              # Streamlit frontend application
├── faq_matcher.py      # NLP matching logic (NLTK + TF-IDF)
├── init_db.py          # Database initialization and FAQ data
├── requirements.txt    # Python dependencies
├── faqs.db            # SQLite database (created on first run)
└── README.md          # This file
```

## 🚀 Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialize Database

```bash
python init_db.py
```

This will create `faqs.db` and populate it with 25 clothing brand FAQs.

### 3. Run the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## 💬 Usage

1. Type your question in the input box (e.g., "What sizes do you offer?")
2. Click the "Ask 🚀" button
3. The chatbot will display the best matching FAQ answer
4. View the similarity score to see how confident the match is
5. Browse available categories at the bottom

## 📊 FAQ Categories

- **Sizing**: Size availability, size charts, fit information
- **Shipping**: Delivery times, international shipping, tracking
- **Returns**: Return policy, refund process, exchanges
- **Products**: Materials, care instructions, sustainability
- **Payment**: Payment methods, security, discount codes
- **Account**: Account creation, password reset
- **General**: Store locations, customer service, gift cards

## 🎨 UI Features

- Gradient backgrounds with vibrant colors
- Animated message bubbles
- Real-time statistics (FAQ count, categories, questions asked)
- Category badges for easy navigation
- Similarity score display for transparency
- Responsive design

## 🔧 Customization

### Adding New FAQs

Edit `init_db.py` and add new entries to the `faqs` list:

```python
("Your question?", "Your answer.", "Category"),
```

Then re-run `python init_db.py` to update the database.

### Adjusting Similarity Threshold

In `app.py`, modify the threshold parameter in `find_best_match()`:

```python
match = matcher.find_best_match(user_question, threshold=0.3)  # Default: 0.3
```

Lower values = more lenient matching, Higher values = stricter matching

## 📝 Technical Details

- **Frontend**: Streamlit with custom CSS
- **Backend**: Python with NLTK
- **Database**: SQLite3
- **NLP Libraries**: NLTK (tokenization, stopwords, lemmatization)
- **ML Libraries**: scikit-learn (TF-IDF, cosine similarity)

## 🎓 Learning Points

This project demonstrates:
- Text preprocessing with NLTK
- TF-IDF vectorization
- Cosine similarity for text matching
- SQLite database operations
- Streamlit UI development
- Session state management

## 📄 License

This project is created for educational purposes as part of Code Alpha internship.

## 👤 Author

Created as part of the Code Alpha NLP Project

---

**Enjoy chatting with the FAQ bot! 🤖👗**
