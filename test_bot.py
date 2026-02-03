#!/usr/bin/env python3
"""
Tawjihi Math Bot - Test Version (Mock Responses)
Demonstrates bot functionality without API quota limits
"""

import json
import os
import sys
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/bot_test.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

DATABASE_PATH = 'data/questions.json'

# Mock solutions and tips for testing
MOCK_SOLUTIONS = {
    "algebra": """1. المعادلة الأصلية:
{question}

2. الخطوة الأولى: تحديد المتغيرات والثوابت
نقوم بفصل المتغيرات عن الثوابت.

3. الخطوة الثانية: تطبيق العمليات الحسابية
نطبق نفس العملية على الطرفين للحفاظ على التوازن.

4. الخطوة الثالثة: التبسيط
نبسط النتيجة للوصول للشكل النهائي.

✅ النتيجة النهائية:
تم حل المعادلة بنجاح.""",
    
    "calculus": """1. المسألة الأصلية:
{question}

2. الخطوة الأولى: تحديد نوع المشتقة أو التكامل
نحدد ما إذا كنا نتعامل مع مشتقة أو تكامل.

3. الخطوة الثانية: تطبيق القواعس الأساسية
نستخدم قواعس التفاضل والتكامل المناسبة.

4. الخطوة الثالثة: التبسيط والتحقق
نتحقق من صحة النتيجة.

✅ النتيجة النهائية:
تم حل المسألة بنجاح.""",
    
    "geometry": """1. المسألة الأصلية:
{question}

2. الخطوة الأولى: رسم الشكل الهندسي
نرسم الشكل ونحدد المعطيات.

3. الخطوة الثانية: تطبيق النظريات الهندسية
نستخدم النظريات والقوانين الهندسية المناسبة.

4. الخطوة الثالثة: الحساب والتحقق
نحسب النتيجة ونتحقق منها.

✅ النتيجة النهائية:
تم حل المسألة الهندسية بنجاح."""
}

MOCK_TIPS = [
    "💡 نصيحة اليوم:\nعند حل المعادلات، تذكر دائماً تطبيق نفس العملية على الطرفين.",
    "💡 نصيحة اليوم:\nالمشتقة تمثل معدل التغير - فكر فيها كسرعة التغير.",
    "💡 نصيحة اليوم:\nفي الهندسة، رسم الشكل بدقة يساعدك على فهم المسألة بشكل أفضل.",
    "💡 نصيحة اليوم:\nتذكر أن التكامل هو العملية العكسية للمشتقة.",
    "💡 نصيحة اليوم:\nعند حل المسائل المعقدة، قسمها إلى خطوات صغيرة."
]


def load_database():
    """Load the questions database"""
    try:
        with open(DATABASE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Database not found: {DATABASE_PATH}")
        sys.exit(1)


def save_database(data):
    """Save database with updated question"""
    try:
        with open(DATABASE_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info("Database updated successfully")
    except Exception as e:
        logger.error(f"Failed to save database: {e}")
        raise


def get_unused_question(questions):
    """Get first unused question"""
    for question in questions:
        if not question.get('used', False):
            return question
    return None


def generate_mock_solution(question_text, question_type):
    """Generate mock solution"""
    template = MOCK_SOLUTIONS.get(question_type, MOCK_SOLUTIONS["algebra"])
    return template.format(question=question_text)


def generate_mock_tip():
    """Generate mock tip"""
    import random
    return random.choice(MOCK_TIPS)


def format_telegram_post(question, solution, tip):
    """Format post for Telegram"""
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
*[TEST MODE - Mock Solution]*
"""
    return post


def main():
    """Main test function"""
    logger.info("=" * 60)
    logger.info("Tawjihi Math Bot - TEST MODE")
    logger.info("=" * 60)
    
    # Load database
    logger.info("Loading question database...")
    questions = load_database()
    logger.info(f"Loaded {len(questions)} questions")
    
    # Get unused question
    logger.info("Searching for unused question...")
    question = get_unused_question(questions)
    
    if not question:
        logger.warning("All questions used - would generate variant in production")
        return
    
    logger.info(f"Selected question {question['id']}: {question['question'][:50]}...")
    
    # Generate mock solution
    logger.info("Generating mock solution...")
    solution = generate_mock_solution(question['question'], question.get('type', 'algebra'))
    logger.info("Solution generated ✓")
    
    # Generate mock tip
    logger.info("Generating daily tip...")
    tip = generate_mock_tip()
    logger.info("Tip generated ✓")
    
    # Format post
    logger.info("Formatting Telegram post...")
    telegram_post = format_telegram_post(question, solution, tip)
    
    # Display the post
    logger.info("\n" + "=" * 60)
    logger.info("TELEGRAM POST PREVIEW:")
    logger.info("=" * 60)
    print(telegram_post)
    logger.info("=" * 60)
    
    # Mark as used and save
    logger.info("Marking question as used...")
    for q in questions:
        if q['id'] == question['id']:
            q['used'] = True
            break
    
    save_database(questions)
    logger.info(f"Question {question['id']} marked as used ✓")
    
    logger.info("=" * 60)
    logger.info("✅ TEST COMPLETED SUCCESSFULLY!")
    logger.info("=" * 60)
    logger.info("\nIn production:")
    logger.info("- This post would be sent to Telegram")
    logger.info("- Solution would be generated by Gemini AI")
    logger.info("- Tip would be AI-generated")
    logger.info("- Database would be committed to GitHub")


if __name__ == '__main__':
    main()
