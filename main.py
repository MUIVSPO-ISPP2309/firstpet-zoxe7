import secrets
import string
import json
import pyperclip
import os


def generate_password(length=12, use_digits=True, use_special_chars=True):
    characters = string.ascii_letters

    if use_digits:
        characters += string.digits

    if use_special_chars:
        characters += string.punctuation

    password = ''.join(secrets.choice(characters) for _ in range(length)) 
    return password


def check_password_strength(password):
    if len(password) < 8:
        return "Слабый: слишком короткий"
    if not any(char.isdigit() for char in password):
        return "Слабый: нет цифр"
    if not any(char.islower() for char in password):
        return "Слабый: нет строчных букв"
    if not any(char.isupper() for char in password):
        return "Слабый: нет заглавных букв"
    if not any(char in string.punctuation for char in password):
        return "Слабый: нет специальных символов"
    return "Надежный"


def load_passwords_from_file(filename='passwords.json'):

    if not os.path.exists(filename):
        return []
    try:
        with open(filename, 'r') as file:
            try:
                passwords = json.load(file)
                return passwords if isinstance(passwords, list) else [passwords]
            except json.JSONDecodeError:
                print("Ошибка: Файл с паролями поврежден или пуст. Создан новый.")
                return []
    except FileNotFoundError:
        return []


def save_passwords_to_file(passwords, filename='passwords.json'):
    try:
        with open(filename, 'w') as file:
            json.dump(passwords, file, indent=4)
        print("Пароли успешно сохранены в файл.")
    except Exception as e:
        print(f"Ошибка при сохранении паролей: {e}")


def add_password_to_file(password, filename='passwords.json'):
    passwords = load_passwords_from_file(filename)
    passwords.append({"password": password})
    save_passwords_to_file(passwords, filename)


def copy_to_clipboard(password):
    pyperclip.copy(password)
    print("Пароль скопирован в буфер обмена.")


def view_passwords(filename='passwords.json'):
    passwords = load_passwords_from_file(filename)
    if not passwords:
        print("Нет сохраненных паролей.")
        return

    print("Сохраненные пароли:")
    for i, entry in enumerate(passwords):
        print(f"{i+1}: {entry['password']}")

def delete_password(filename='passwords.json'):
    passwords = load_passwords_from_file(filename)
    if not passwords:
        print("Нет сохраненных паролей для удаления.")
        return

    view_passwords(filename)
    try:
        index_to_delete = int(input("Введите номер пароля, который хотите удалить: ")) - 1
        if 0 <= index_to_delete < len(passwords):
            deleted_password = passwords.pop(index_to_delete)
            save_passwords_to_file(passwords, filename)
            print(f"Пароль '{deleted_password['password']}' успешно удален.")
        else:
            print("Неверный номер пароля.")
    except ValueError:
        print("Ошибка: Введите целое число.")



def main():
    while True:
        print("\nГенератор паролей")
        print("1. Сгенерировать пароль")
        print("2. Просмотреть сохраненные пароли")
        print("3. Удалить сохраненный пароль")
        print("4. Выйти")

        choice = input("Выберите действие: ")

        if choice == '1':
            while True:
                try:
                    length = int(input("Введите длину пароля: "))
                    break
                except ValueError:
                    print("Ошибка: Введите целое число для длины пароля.")

            use_digits = input("Использовать цифры? (y/n): ").lower() == 'y'
            use_special_chars = input("Использовать специальные символы? (y/n): ").lower() == 'y'

            password = generate_password(length, use_digits, use_special_chars)
            print(f"Сгенерированный пароль: {password}")
            print(check_password_strength(password))

            save = input("Хотите сохранить пароль в файл? (y/n): ").lower() == 'y'
            if save:
                add_password_to_file(password)

            copy = input("Хотите скопировать пароль в буфер обмена? (y/n): ").lower() == 'y'
            if copy:
                copy_to_clipboard(password)

        elif choice == '2':
            view_passwords()

        elif choice == '3':
            delete_password()

        elif choice == '4':
            break

        else:
            print("Неверный выбор. Пожалуйста, выберите действие из списка.")


if __name__ == "__main__":
    main()
