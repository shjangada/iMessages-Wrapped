from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
from datetime import datetime, timedelta
import nltk
from nltk.corpus import stopwords
import re
import os

app = Flask(__name__)
CORS(app)

stop_words = set(stopwords.words('english'))
stop_words.update([
    "know", "yes", "much", "okay", "right", "thing", "lot",
    "got", "make", "even", "say", "today", "still", "last", "things", "first",
    "makes", "wait", "back", "see", "really", "gonna", "think",
    "need", "wanna", "going", "stuff", "idk", "abt",
    "yeah", "yup"
])

def analyze_messages(chat_id=None):
    DB_PATH = os.path.expanduser("~/Library/Messages/chat.db")
    if not os.path.exists(DB_PATH):
        print(f"Database file not found at {DB_PATH}")
        return {"error": "Database file not found"}
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Base query
        query = """
            SELECT text, date, is_from_me, destination_caller_id, date_delivered, date_read
            FROM message
            WHERE text IS NOT NULL
        """
        
        # Add chat_id filter if provided
        if chat_id:
            query += f" AND chat_id = ?"
            cursor.execute(query, (chat_id,))
        else:
            cursor.execute(query)
        
        messages = cursor.fetchall()
        
        if not messages:
            return {"error": "No messages found"}
        
        # Initialize analysis variables
        total_messages = 0
        from_me = 0
        words_list = []
        time_segments = {
            "Late Night (00:00-03:59)": 0,
            "Early Morning (04:00-07:59)": 0,
            "Morning (08:00-11:59)": 0,
            "Afternoon (12:00-15:59)": 0,
            "Evening (16:00-19:59)": 0,
            "Night (20:00-23:59)": 0
        }
        
        for text, date, is_from_me, _, date_delivered, date_read in messages:
            if text:  # Make sure text is not None
                message_date = datetime(2001, 1, 1) + timedelta(seconds=date / 1e9)
                total_messages += 1
                
                if is_from_me:
                    from_me += 1
                    # Process words for frequency distribution
                    words = text.split()
                    for word in words:
                        word_lower = word.lower()
                        if word_lower not in stop_words and len(word_lower) >= 3:
                            word_clean = re.sub(r'\W+', '', word_lower)
                            if word_clean:
                                words_list.append(word_clean)
                    
                    # Count messages by time segment
                    hour = message_date.hour
                    if 0 <= hour < 4:
                        time_segments["Late Night (00:00-03:59)"] += 1
                    elif 4 <= hour < 8:
                        time_segments["Early Morning (04:00-07:59)"] += 1
                    elif 8 <= hour < 12:
                        time_segments["Morning (08:00-11:59)"] += 1
                    elif 12 <= hour < 16:
                        time_segments["Afternoon (12:00-15:59)"] += 1
                    elif 16 <= hour < 20:
                        time_segments["Evening (16:00-19:59)"] += 1
                    else:
                        time_segments["Night (20:00-23:59)"] += 1
        
        # Calculate word frequency
        fd = nltk.FreqDist(words_list)
        top_words = [(word, count) for word, count in fd.most_common(10)]
        
        # Calculate average message length
        avg_text_length = sum(len(text.split()) for text, *_ in messages if text) / total_messages if total_messages > 0 else 0
        
        # Count curse words
        curse_list = ["fuck", "damn", "shit", "ass", "crap", "bitch", "dumbass", "fucking", "asshole", "bastard", "pissed", "motherfucker"]
        curse_count = sum(fd[word] for word in curse_list if word in fd)
        
        conn.close()
        
        return {
            "totalMessages": total_messages,
            "sentMessages": from_me,
            "sentPercentage": (from_me / total_messages * 100) if total_messages > 0 else 0,
            "frequencyDistribution": top_words,
            "averageLength": round(avg_text_length, 2),
            "curseCount": curse_count,
            "timeSegments": time_segments
        }
    
    except sqlite3.Error as e:
        return {"error": f"Database error: {str(e)}"}
    except Exception as e:
        return {"error": f"Error analyzing messages: {str(e)}"}

@app.route('/api/messages', methods=['GET'])
def get_all_messages():
    analysis = analyze_messages()
    if "error" in analysis:
        return jsonify(analysis), 500
    return jsonify(analysis)

@app.route('/api/word-count', methods=['POST'])
def get_word_count():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.json
    word = data.get('word', '').lower()
    chat_id = data.get('chatId')
    
    if not word:
        return jsonify({"error": "No word provided"}), 400
    
    try:
        conn = sqlite3.connect(os.path.expanduser("~/Library/Messages/chat.db"))
        cursor = conn.cursor()
        
        query = """
            SELECT text
            FROM message
            WHERE text IS NOT NULL AND is_from_me = 1
        """
        if chat_id:
            query += " AND chat_id = ?"
            cursor.execute(query, (chat_id,))
        else:
            cursor.execute(query)
        
        messages = cursor.fetchall()
        word_count = sum(text[0].lower().count(word) for text in messages if text[0])
        
        conn.close()
        
        return jsonify({"count": word_count})
    
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Error counting words: {str(e)}"}), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
