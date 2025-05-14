import json
from pathlib import Path
from typing import Dict, Any
import random

STORAGE_PATH = Path(__file__).parent.parent / "storage.json"


def load_data() -> Dict[str, Any]:
    """Загружает данные из storage.json"""
    try:
        with open(STORAGE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "users": {},
            "quizzes": [],
            "facts": [],
            "monthly_theme": ""
        }


def save_data(data: Dict[str, Any]) -> None:
    """Сохраняет данные в storage.json"""
    with open(STORAGE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_random_quiz() -> Dict[str, Any]:
    """Возвращает случайный вопрос викторины"""
    data = load_data()
    return random.choice(data["quizzes"])


def check_answer(user_id: int, answer: str) -> bool:
    """Проверяет правильность ответа пользователя"""
    data = load_data()
    user_id = str(user_id)

    if user_id not in data["users"] or not data["users"][user_id]["current_quiz"]:
        return False

    quiz_id = data["users"][user_id]["current_quiz"]
    quiz = next((q for q in data["quizzes"] if q["id"] == quiz_id), None)

    if not quiz:
        return False

    is_correct = answer == quiz["correct"]

    if is_correct:
        data["users"][user_id]["score"] += 10  # Начисляем 10 очков за правильный ответ
        data["users"][user_id]["current_quiz"] = None  # Сбрасываем текущий вопрос
        save_data(data)

    return is_correct


def get_random_fact() -> Dict[str, Any]:
    """Возвращает случайный исторический факт"""
    data = load_data()
    if not data["facts"]:
        return {"content": "Факты временно отсутствуют", "category": "инфо"}
    return random.choice(data["facts"])


def add_fact(fact_content: str, category: str) -> None:
    """Добавляет новый факт в хранилище"""
    data = load_data()
    new_id = max([f["id"] for f in data["facts"]], default=0) + 1
    data["facts"].append({
        "id": new_id,
        "content": fact_content,
        "category": category
    })
    save_data(data)
