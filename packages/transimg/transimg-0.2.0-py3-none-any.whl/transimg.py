import os
import subprocess
import platform

# Функция для очистки консоли в зависимости от ОС
def clear_console():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

# Функция для получения языка
def get_language():
    while True:
        language = input("Выберите язык / Select language (E/R): ").strip().upper()
        if language in ["E", "R"]:
            return language
        else:
            print("Invalid input. Please enter E or R. / Неверный ввод. Пожалуйста, введите E или R.")

# Функция для получения текста на выбранном языке
def get_text(language):
    if language == "E":
        return {
            "author": "Author: Avinion\nTelegram: @akrim\n",
            "enter_folder": "Enter the path to the folder with images (leave blank to use the current directory): ",
            "enter_format": "Enter the format to convert the images to (e.g., jpg, png, gif, webp, bmp): ",
            "files_not_found": "No files found for conversion.",
            "conversion_progress": "Conversion progress: {:.2f}%",
            "conversion_complete": "Conversion complete.",
            "continue_prompt": "Do you want to continue? (Y/N): ",
            "invalid_input": "Invalid input. Please enter Y or N.",
            "goodbye": "Goodbye!"
        }
    else:
        return {
            "author": "Автор: Avinion\nTelegram: @akrim\n",
            "enter_folder": "Введите путь к папке с изображениями (оставьте пустым для использования текущей директории): ",
            "enter_format": "Введите формат, в который нужно конвертировать изображения (например, jpg, png, gif, webp, bmp): ",
            "files_not_found": "Файлы для конвертации не найдены.",
            "conversion_progress": "Прогресс конвертации: {:.2f}%",
            "conversion_complete": "Конвертация завершена.",
            "continue_prompt": "Хотите продолжить? (Y/N): ",
            "invalid_input": "Неверный ввод. Пожалуйста, введите Y или N.",
            "goodbye": "До свидания!"
        }

def main():
    language = get_language()
    text = get_text(language)

    while True:
        clear_console()

        # Вывод информации об авторе
        print(text["author"])

        # Запрашиваем путь к папке с изображениями
        input_folder = input(text["enter_folder"]).strip()
        if not input_folder:
            input_folder = os.getcwd()

        # Запрашиваем формат, в который нужно конвертировать изображения
        output_format = input(text["enter_format"]).strip()

        # Получаем текущую директорию (где открыто окно консоли)
        output_folder = os.getcwd()

        # Список для хранения имен файлов для конвертации
        files_to_convert = [f for f in os.listdir(input_folder) if f.endswith((".jpg", ".png", ".gif", ".webp", ".bmp"))]
        total_files = len(files_to_convert)

        # Проверяем, есть ли файлы для конвертации
        if total_files == 0:
            print(text["files_not_found"])
        else:
            # Проверяем, одинаковы ли папки
            same_folder = (input_folder == output_folder)

            # Перебираем все файлы в папке с изображениями
            for index, filename in enumerate(files_to_convert, start=1):
                # Формируем полный путь к входному файлу
                input_file = os.path.join(input_folder, filename)

                # Генерируем новое имя файла, если папки одинаковы
                if same_folder:
                    base, ext = os.path.splitext(filename)
                    new_base = f"{base}_converted"
                    output_file = os.path.join(output_folder, new_base + "." + output_format)
                else:
                    output_file = os.path.join(output_folder, os.path.splitext(filename)[0] + "." + output_format)

                # Конвертируем изображение с помощью FFmpeg без вывода в консоль
                subprocess.call(["ffmpeg", "-i", input_file, output_file], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

                # Подсчитываем и выводим общий процесс в процентах
                progress = (index / total_files) * 100
                print(text["conversion_progress"].format(progress))

            print(text["conversion_complete"])

        # Запрос на продолжение работы со скриптом
        while True:
            continue_work = input(text["continue_prompt"]).strip().upper()
            if continue_work in ["Y", "N"]:
                break
            else:
                print(text["invalid_input"])

        if continue_work == "N":
            print(text["goodbye"])
            break

if __name__ == "__main__":
    main()
