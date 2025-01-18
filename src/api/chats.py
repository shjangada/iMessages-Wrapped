from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from datetime import datetime
from statistics import mean

# Initialize Flask app
app = Flask(__name__)
sia = SentimentIntensityAnalyzer()
CORS(app, origins="http://localhost:3000")

# Path to the database
username = "shreyajangada"
DB_PATH = f"/Users/{username}/Library/Messages/chat.db"
STOP_WORDS = set(stopwords.words("english"))

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    return set(word for word in tokens if word.isalnum() and word not in STOP_WORDS)

def calculate_jaccard_similarity(my_messages, their_messages):
    my_words = set()
    their_words = set()

    for message in my_messages:
        my_words.update(preprocess_text(message))
    for message in their_messages:
        their_words.update(preprocess_text(message))

    intersection = my_words.intersection(their_words)
    union = my_words.union(their_words)
    return len(intersection) / len(union) if union else 0.0

@app.route('/api/chats', methods=['GET'])
def get_chats():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                handle.id AS id,
                message.text,
                message.is_from_me
            FROM 
                message
            JOIN 
                chat_message_join ON message.rowid = chat_message_join.message_id
            JOIN 
                chat ON chat_message_join.chat_id = chat.rowid
            JOIN 
                handle ON handle.id = chat.chat_identifier
            WHERE 
                message.text IS NOT NULL
        """)

        messages = cursor.fetchall()
        handle_messages = {}

        for handle, text, is_from_me in messages:
            if not text:
                continue
            if handle not in handle_messages:
                handle_messages[handle] = {'messages': [], 'sentiment_scores': []}
            handle_messages[handle]['messages'].append((text, is_from_me))
            sentiment_score = sia.polarity_scores(text)['compound']
            handle_messages[handle]['sentiment_scores'].append(sentiment_score)

        handle_data = []
        for handle, data in handle_messages.items():
            my_messages = [msg[0] for msg in data['messages'] if msg[1] == 1]
            their_messages = [msg[0] for msg in data['messages'] if msg[1] == 0]
            avg_sentiment_score = mean(data['sentiment_scores']) if data['sentiment_scores'] else 0
            positivity = "Positive" if avg_sentiment_score > 0 else "Negative" if avg_sentiment_score < 0 else "Neutral"
            blend_rate = calculate_jaccard_similarity(my_messages, their_messages)
            handle_data.append({
                'id': handle,
                'messages': len(data['messages']),
                'positivity': positivity,
                'blend_rate': blend_rate
            })

        # Sort by number of messages, then by positivity
        handle_data.sort(key=lambda x: (x['messages'], x['blend_rate']), reverse=True)
        handle_data = handle_data[:10] 
        return jsonify(handle_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
