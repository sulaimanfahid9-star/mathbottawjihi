#!/usr/bin/env python3.11
"""
Tawjihi Math Bot - Posts daily math questions with AI-generated solutions
Uses Long Cat API for solution generation
"""

import os
import json
import logging
import requests
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/bot.log'),
        logging.StreamHandler()
    ]
)

# Environment variables
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
LONGCAT_API_KEY = os.getenv('LONGCAT_API_KEY')

# Long Cat API configuration
LONGCAT_BASE_URL = "https://api.longcat.chat/openai"
LONGCAT_MODEL = "LongCat-Flash-Chat"

# Ensure directories exist
Path('logs').mkdir(exist_ok=True)
Path('data').mkdir(exist_ok=True)

def load_questions():
    """Load questions from JSON database"""
    try:
        with open('data/questions.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error("Questions database not found!")
        return []

def load_used_questions():
    """Load the set of used question IDs"""
    try:
        with open('data/used_questions.json', 'r', encoding='utf-8') as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()

def save_used_questions(used_ids):
    """Save used question IDs"""
    with open('data/used_questions.json', 'w', encoding='utf-8') as f:
        json.dump(list(used_ids), f)

def get_next_question(questions, used_ids):
    """Get the next unused question"""
    for q in questions:
        if q['id'] not in used_ids:
            return q
    # If all used, reset
    return questions[0] if questions else None

def generate_solution(question_text):
    """Generate solution using Long Cat API"""
    try:
        headers = {
            "Authorization": f"Bearer {LONGCAT_API_KEY}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""You are a professional math teacher. Generate a clear, concise solution for this math question.

Question: {question_text}

Requirements:
1. Use simple, clear Arabic language
2. Show 3-5 key steps only
3. Use numbered steps (1️⃣ 2️⃣ 3️⃣ etc.)
4. No LaTeX or complex symbols
5. End with the final answer
6. Keep it SHORT and student-friendly

Format:
1️⃣ Step name: explanation
2️⃣ Step name: explanation
3️⃣ Step name: explanation
✅ Final Answer: [answer]"""

        data = {
            "model": LONGCAT_MODEL,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 800,
            "temperature": 0.7
        }
        
        response = requests.post(
            f"{LONGCAT_BASE_URL}/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            logging.error(f"Long Cat API error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        logging.error(f"Failed to generate solution: {e}")
        return None

def generate_daily_tip():
    """Generate a daily educational tip using Long Cat API"""
    try:
        headers = {
            "Authorization": f"Bearer {LONGCAT_API_KEY}",
            "Content-Type": "application/json"
        }
        
        prompt = """Generate one short, practical math study tip in Arabic for students.
Keep it to 1-2 sentences max.
Make it motivating and useful.
Format: 💡 نصيحة اليوم: [tip]"""

        data = {
            "model": LONGCAT_MODEL,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 200,
            "temperature": 0.8
        }
        
        response = requests.post(
            f"{LONGCAT_BASE_URL}/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            logging.warning(f"Failed to generate tip: {response.status_code}")
            return "💡 نصيحة اليوم: تذكر أن الممارسة المنتظمة هي مفتاح النجاح في الرياضيات"
    except Exception as e:
        logging.warning(f"Failed to generate tip: {e}")
        return "💡 نصيحة اليوم: تذكر أن الممارسة المنتظمة هي مفتاح النجاح في الرياضيات"

def format_telegram_post(question, solution, tip):
    """Format the post for Telegram"""
    post = f"""📘 Question:
{question['question']}

Type: {question['type']}
Chapter: {question['chapter']}

📝 Solution:
{solution}

{tip}

---
Posted at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC
Question ID: {question['id']}"""
    
    return post

def send_to_telegram(message):
    """Send message to Telegram"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        
        response = requests.post(url, json=data, timeout=30)
        
        if response.status_code == 200:
            logging.info("Message sent successfully to Telegram")
            return True
        else:
            logging.error(f"Telegram error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        logging.error(f"Failed to send to Telegram: {e}")
        return False

def main():
    """Main function"""
    logging.info("=" * 60)
    logging.info("Tawjihi Math Bot - Starting Daily Post")
    logging.info("=" * 60)
    
    # Validate environment variables
    if not all([TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, LONGCAT_API_KEY]):
        logging.error("Missing required environment variables!")
        return
    
    # Load questions
    logging.info("Loading question database...")
    questions = load_questions()
    if not questions:
        logging.error("No questions found!")
        return
    logging.info(f"Loaded {len(questions)} questions from database")
    
    # Get used questions
    used_ids = load_used_questions()
    
    # Select next question
    logging.info("Searching for unused question...")
    question = get_next_question(questions, used_ids)
    if not question:
        logging.error("No questions available!")
        return
    
    logging.info(f"Selected question {question['id']}: {question['question'][:50]}...")
    
    # Generate solution
    logging.info("Generating solution with Long Cat AI...")
    solution = generate_solution(question['question'])
    if not solution:
        logging.error("Failed to generate solution")
        return
    logging.info("Solution generated successfully")
    
    # Generate daily tip
    logging.info("Generating daily tip...")
    tip = generate_daily_tip()
    logging.info("Daily tip generated")
    
    # Format post
    logging.info("Formatting Telegram post...")
    post = format_telegram_post(question, solution, tip)
    
    # Send to Telegram
    logging.info("Sending to Telegram...")
    if send_to_telegram(post):
        # Mark question as used
        used_ids.add(question['id'])
        save_used_questions(used_ids)
        logging.info(f"Question {question['id']} marked as used")
        
        logging.info("=" * 60)
        logging.info("Daily post completed successfully!")
        logging.info("=" * 60)
    else:
        logging.error("Failed to send message to Telegram")

if __name__ == "__main__":
    main()
