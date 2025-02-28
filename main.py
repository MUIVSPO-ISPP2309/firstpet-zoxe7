import random
import string
import json
import pyperclip


def generate_password(length=12, use_digits=True, use_special_chars=True):
    characters = string.ascii_letters

    if use_digits:
        characters += string.digits

    if use_special_chars:
        characters += string.punctuation

    password = ''.join(random.choice(characters) for _ in range(length))
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


def save_password_to_file(password, filename='passwords.json'):
    try:
        with open(filename, 'a') as file:
            json.dump({"password": password}, file)
            file.write('\n')
        print("Пароль успешно сохранен в файл.")
    except Exception as e:
        print(f"Ошибка при сохранении пароля: {e}")


def copy_to_clipboard(password):
    pyperclip.copy(password)
    print("Пароль скопирован в буфер обмена.")


def main():
    while True:
        print("\nГенератор паролей")
        length = int(input("Введите длину пароля: "))
        use_digits = input("Использовать цифры? (y/n): ").lower() == 'y'
        use_special_chars = input("Использовать специальные символы? (y/n): ").lower() == 'y'

        password = generate_password(length, use_digits, use_special_chars)
        print(f"Сгенерированный пароль: {password}")
        print(check_password_strength(password))

        save = input("Хотите сохранить пароль в файл? (y/n): ").lower() == 'y'
        if save:
            save_password_to_file(password)

        copy = input("Хотите скопировать пароль в буфер обмена? (y/n): ").lower() == 'y'
        if copy:
            copy_to_clipboard(password)

        cont = input("Хотите сгенерировать еще один пароль? (y/n): ").lower()
        if cont != 'y':
            break


if __name__ == "__main__":
    main()
