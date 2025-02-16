import os
import json
import subprocess

def load_config(config_path="config.json"):
    """Завантажує конфігурацію з JSON-файлу."""
    try:
        with open(config_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("❌ Файл config.json не знайдено!")
        exit(1)
    except json.JSONDecodeError:
        print("❌ Помилка у форматі config.json!")
        exit(1)

def run_git_command(command, repo_path):
    """Виконує Git-команду в заданому репозиторії."""
    try:
        result = subprocess.run(command, cwd=repo_path, text=True, check=True, capture_output=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Помилка при виконанні команди {command}: {e.stderr}")
        exit(1)

def check_for_changes(repo_path):
    """Перевіряє, чи є зміни у репозиторії."""
    result = subprocess.run(["git", "status", "--porcelain"], cwd=repo_path, text=True, capture_output=True)
    return bool(result.stdout.strip())  # Якщо є зміни, виведе результат

def push_to_github():
    """Основна функція для пушу змін у GitHub."""
    config = load_config()
    repo_path = config["repo_path"]
    branch = config["branch"]
    commit_message = config["commit_message"]

    if not os.path.exists(repo_path):
        print(f"❌ Шлях до репозиторію не знайдено: {repo_path}")
        exit(1)

    print("📂 Перехід у репозиторій:", repo_path)

    if not check_for_changes(repo_path):
        print("⚠️ Немає змін для пушу.")
        exit(0)

    # Виконуємо команди Git
    run_git_command(["git", "add", "."], repo_path)
    run_git_command(["git", "commit", "-m", commit_message], repo_path)
    run_git_command(["git", "push", "origin", branch], repo_path)

    print("✅ Зміни успішно запушені у GitHub!")

if __name__ == "__main__":
    push_to_github()
