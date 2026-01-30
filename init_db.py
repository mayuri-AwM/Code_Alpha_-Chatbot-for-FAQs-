"""
Database initialization script for FAQ Chatbot
Creates SQLite database and populates it with clothing brand FAQs
"""

import sqlite3
import os

# Database file path
DB_PATH = "faqs.db"

def create_database():
    """Create the SQLite database and FAQ table"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create FAQs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS faqs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            category TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✓ Database created successfully!")

def populate_faqs():
    """Populate database with clothing brand FAQs"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if FAQs already exist
    cursor.execute("SELECT COUNT(*) FROM faqs")
    if cursor.fetchone()[0] > 0:
        print("✓ FAQs already exist in database")
        conn.close()
        return
    
    # FAQ data for online clothing brand
    faqs = [
        # Sizing Questions
        ("What sizes do you offer?", 
         "We offer sizes from XS to 3XL for most items. Please check individual product pages for specific size availability.", 
         "Sizing"),
        
        ("How do I find my correct size?", 
         "Please refer to our size chart available on each product page. We recommend measuring yourself and comparing with our size guide for the best fit.", 
         "Sizing"),
        
        ("Do your clothes run true to size?", 
         "Yes, our clothes generally run true to size. However, we recommend checking the size chart and customer reviews for specific items.", 
         "Sizing"),
        
        # Shipping Questions
        ("How long does shipping take?", 
         "Standard shipping takes 5-7 business days. Express shipping is available and takes 2-3 business days.", 
         "Shipping"),
        
        ("Do you ship internationally?", 
         "Yes, we ship to over 50 countries worldwide. Shipping costs and delivery times vary by location.", 
         "Shipping"),
        
        ("What are the shipping charges?", 
         "Standard shipping is free for orders over $50. For orders under $50, shipping costs $5.99. Express shipping is $12.99.", 
         "Shipping"),
        
        ("Can I track my order?", 
         "Yes! Once your order ships, you'll receive a tracking number via email to monitor your delivery.", 
         "Shipping"),
        
        # Returns & Exchanges
        ("What is your return policy?", 
         "We accept returns within 30 days of delivery. Items must be unworn, unwashed, and have original tags attached.", 
         "Returns"),
        
        ("How do I return an item?", 
         "Log into your account, go to order history, select the item to return, and follow the instructions. We'll email you a prepaid return label.", 
         "Returns"),
        
        ("Can I exchange an item?", 
         "Yes! You can exchange items for a different size or color within 30 days. The exchange process is similar to returns.", 
         "Returns"),
        
        ("How long does it take to get a refund?", 
         "Refunds are processed within 5-7 business days after we receive your return. It may take an additional 3-5 days to appear in your account.", 
         "Returns"),
        
        # Product Questions
        ("What materials are your clothes made from?", 
         "We use high-quality materials including organic cotton, linen, polyester blends, and sustainable fabrics. Material details are listed on each product page.", 
         "Products"),
        
        ("How do I care for my clothes?", 
         "Care instructions are provided on the label of each garment. Generally, we recommend washing in cold water and air drying to maintain quality.", 
         "Products"),
        
        ("Are your products sustainable?", 
         "Yes! We're committed to sustainability. Many of our products use organic and recycled materials, and we partner with ethical manufacturers.", 
         "Products"),
        
        ("Do you restock sold-out items?", 
         "Popular items are often restocked. You can sign up for restock notifications on the product page to be alerted when items are available again.", 
         "Products"),
        
        # Payment & Orders
        ("What payment methods do you accept?", 
         "We accept all major credit cards (Visa, MasterCard, American Express), PayPal, and digital wallets like Apple Pay and Google Pay.", 
         "Payment"),
        
        ("Is my payment information secure?", 
         "Absolutely! We use industry-standard SSL encryption to protect your payment information. We never store your complete credit card details.", 
         "Payment"),
        
        ("Can I cancel my order?", 
         "You can cancel your order within 2 hours of placement. After that, the order enters processing and cannot be cancelled, but you can return it once received.", 
         "Orders"),
        
        ("How do I use a discount code?", 
         "Enter your discount code at checkout in the 'Promo Code' field before completing your purchase. The discount will be applied to your total.", 
         "Payment"),
        
        # Account Questions
        ("Do I need an account to place an order?", 
         "No, you can checkout as a guest. However, creating an account allows you to track orders, save favorites, and checkout faster.", 
         "Account"),
        
        ("How do I reset my password?", 
         "Click 'Forgot Password' on the login page, enter your email, and we'll send you a password reset link.", 
         "Account"),
        
        # General Questions
        ("Do you have physical stores?", 
         "We're currently an online-only retailer, which allows us to offer better prices and a wider selection.", 
         "General"),
        
        ("How can I contact customer service?", 
         "You can reach us via email at support@clothingbrand.com or through our contact form. We respond within 24 hours on business days.", 
         "General"),
        
        ("Do you offer gift cards?", 
         "Yes! Gift cards are available in denominations from $25 to $500 and can be purchased on our website.", 
         "General"),
    ]
    
    # Insert FAQs into database
    cursor.executemany(
        "INSERT INTO faqs (question, answer, category) VALUES (?, ?, ?)",
        faqs
    )
    
    conn.commit()
    conn.close()
    print(f"✓ Successfully added {len(faqs)} FAQs to database!")

def get_all_faqs():
    """Retrieve all FAQs from database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, question, answer, category FROM faqs")
    faqs = cursor.fetchall()
    
    conn.close()
    return faqs

def search_faq_by_id(faq_id):
    """Get a specific FAQ by ID"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT question, answer FROM faqs WHERE id = ?", (faq_id,))
    result = cursor.fetchone()
    
    conn.close()
    return result

def get_faq_count():
    """Get total number of FAQs in database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM faqs")
    count = cursor.fetchone()[0]
    
    conn.close()
    return count

if __name__ == "__main__":
    print("Initializing FAQ Database...")
    create_database()
    populate_faqs()
    
    # Display summary
    count = get_faq_count()
    print(f"\n📊 Database Summary:")
    print(f"   Total FAQs: {count}")
    print(f"   Database Location: {os.path.abspath(DB_PATH)}")
    print("\n✅ Database initialization complete!")
