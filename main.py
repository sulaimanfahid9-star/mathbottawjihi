#!/usr/bin/env python3
"""
Tawjihi Math Bot - Automated Telegram Math Teacher
Posts one math question per day with step-by-step Arabic solutions using Gemini AI
Uses the new google-genai SDK (replaces deprecated google.generativeai)
"""

import json
import os
import sys
import logging
from datetime import datetime
from pathlib import Path
import requests
from google import genai

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
DATABASE_PATH = 'data/questions.json'
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}'

# Initialize Gemini AI with new SDK
client = genai.Client(api_key=GEMINI_API_KEY)


def load_database():
    """Load the questions database from JSON file"""
    try:
        with open(DATABASE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Database file not found: {DATABASE_PATH}")
        sys.exit(1)
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in database file: {DATABASE_PATH}")
        sys.exit(1)


def save_database(data):
    """Save the updated database back to JSON file"""
    try:
        with open(DATABASE_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info("Database saved successfully")
    except Exception as e:
        logger.error(f"Failed to save database: {e}")
        raise


def get_unused_question(questions):
    """Get the first unused question from the database"""
    for question in questions:
        if not question.get('used', False):
            return question
    return None


def generate_solution(question_text, topic):
    """Generate step-by-step Arabic solution using Gemini AI"""
    prompt = f"""أنت معلم رياضيات محترف وخبير في شرح الحلول بطريقة واضحة ومنظمة.

حل المسألة التالية خطوة بخطوة:

المسألة (بالإنجليزية):
{question_text}

الموضوع: {topic}

متطلبات الحل:
1. اكتب الحل بالعربية فقط
2. ابدأ بإعادة صياغة المسألة بوضوح
3. اذكر الخطوات المنطقية والرياضية بشكل منظم
4. استخدم الرموز الرياضية بشكل صحيح
5. اشرح سبب كل خطوة
6. قدم الإجابة النهائية بشكل واضح
7. إذا كانت الإجابة كسر، اكتبها ككسر دقيق وليس عدد عشري
8. تجنب الحسابات الطويلة المعقدة

صيغة الحل:
**المسألة:**
[إعادة صياغة]

**الحل:**
1. [الخطوة الأولى]
2. [الخطوة الثانية]
...

خطوة النتيجة النهائية:
✅ الإجابة: [الإجابة الدقيقة]

ابدأ الآن:"""

    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )
        return response.text
    except Exception as e:
        logger.error(f"Failed to generate solution: {e}")
        return None


def generate_daily_tip(topic):
    """Generate a short daily math tip in Arabic"""
    prompt = f"""أنت معلم رياضيات محترف. قم بكتابة نصيحة تعليمية قصيرة وقيمة عن موضوع: {topic}

المتطلبات:
- النصيحة بالعربية فقط
- سطر واحد أو سطرين فقط
- نصيحة عملية وقيمة
- ابدأ بـ "💡 نصيحة اليوم:"

مثال:
💡 نصيحة اليوم:
عند حل المعادلات، تذكر دائماً تطبيق نفس العملية على الطرفين للحفاظ على التوازن.

ابدأ الآن:"""

    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )
        return response.text
    except Exception as e:
        logger.error(f"Failed to generate tip: {e}")
        return None


def format_telegram_post(question, solution, tip):
    """Format the post for Telegram"""
    post = f"""📚 **Math Question**

**Question (English):**
{question['question']}

**Type:** {question.get('type', 'General')}
**Chapter:** {question.get('chapter', 'Unknown')}

---

**الحل (Arabic Solution):**

{solution}

---

{tip}

---
*Posted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}*
*Question ID: {question['id']}*
"""
    return post


def send_to_telegram(message_text):
    """Send message to Telegram channel"""
    try:
        payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message_text,
            'parse_mode': 'Markdown'
        }
        response = requests.post(
            f'{TELEGRAM_API_URL}/sendMessage',
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            logger.info(f"Message sent successfully to Telegram")
            return True
        else:
            logger.error(f"Failed to send message: {response.text}")
            return False
    except Exception as e:
        logger.error(f"Telegram API error: {e}")
        return False


def generate_question_variant(original_question):
    """Generate a new variant of a question when database is exhausted"""
    prompt = f"""أنت معلم رياضيات محترف. قم بإنشاء متغير جديد من المسألة التالية:

المسألة الأصلية:
{original_question['question']}

المتطلبات:
1. احتفظ بنفس المفهوم الرياضي
2. غير الأرقام والمتغيرات
3. اكتب المسألة بالإنجليزية فقط
4. اجعل المسألة بنفس مستوى الصعوبة
5. اكتب فقط المسألة الجديدة بدون شرح

ابدأ الآن:"""

    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        logger.error(f"Failed to generate variant: {e}")
        return None


def main():
    """Main bot execution function"""
    logger.info("=" * 60)
    logger.info("Tawjihi Math Bot - Starting Daily Post")
    logger.info("=" * 60)
    
    # Validate configuration
    if not all([TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, GEMINI_API_KEY]):
        logger.error("Missing required environment variables")
        logger.error("Required: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, GEMINI_API_KEY")
        sys.exit(1)
    
    # Load database
    logger.info("Loading question database...")
    questions = load_database()
    logger.info(f"Loaded {len(questions)} questions from database")
    
    # Get unused question
    logger.info("Searching for unused question...")
    question = get_unused_question(questions)
    
    if not question:
        logger.warning("All questions have been used. Generating new variants...")
        # Find a random used question and create a variant
        used_questions = [q for q in questions if q.get('used', False)]
        if used_questions:
            import random
            original = random.choice(used_questions)
            logger.info(f"Creating variant of question {original['id']}")
            
            new_question_text = generate_question_variant(original)
            if new_question_text:
                # Create new question object
                new_id = max([q['id'] for q in questions]) + 1
                question = {
                    'id': new_id,
                    'question': new_question_text,
                    'type': original.get('type', 'algebra'),
                    'chapter': original.get('chapter', 'Unknown'),
                    'source': f"{original.get('source', 'Unknown')} - Variant",
                    'used': False
                }
                questions.append(question)
                logger.info(f"Generated variant question {new_id}")
            else:
                logger.error("Failed to generate question variant")
                sys.exit(1)
        else:
            logger.error("No questions available in database")
            sys.exit(1)
    
    logger.info(f"Selected question {question['id']}: {question['question'][:50]}...")
    
    # Generate solution
    logger.info("Generating solution with Gemini AI...")
    solution = generate_solution(question['question'], question.get('type', 'algebra'))
    if not solution:
        logger.error("Failed to generate solution")
        sys.exit(1)
    logger.info("Solution generated successfully")
    
    # Generate daily tip
    logger.info("Generating daily tip...")
    tip = generate_daily_tip(question.get('chapter', 'Mathematics'))
    if not tip:
        logger.warning("Failed to generate tip, continuing without it")
        tip = "💡 نصيحة اليوم:\nاستمر في الممارسة والتركيز على فهم المفاهيم الأساسية."
    logger.info("Daily tip generated")
    
    # Format and send to Telegram
    logger.info("Formatting Telegram post...")
    telegram_post = format_telegram_post(question, solution, tip)
    
    logger.info("Sending to Telegram...")
    if send_to_telegram(telegram_post):
        # Mark question as used
        for q in questions:
            if q['id'] == question['id']:
                q['used'] = True
                break
        
        # Save updated database
        save_database(questions)
        logger.info(f"Question {question['id']} marked as used")
        logger.info("=" * 60)
        logger.info("Daily post completed successfully!")
        logger.info("=" * 60)
    else:
        logger.error("Failed to send message to Telegram")
        sys.exit(1)


if __name__ == '__main__':
    main()
