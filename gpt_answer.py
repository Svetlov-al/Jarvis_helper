import os
import openai
from dotenv import load_dotenv
from speech_to_text import recognize_from_microphone
from speech_synthesis import from_text_to_speak

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


def listen_for_wake_word(wake_word):
    while True:
        text = recognize_from_microphone()
        if wake_word in text:
            return


chat_log = []  # список для хранения истории общения

# Определение первого сообщения от системы
system_message = {"role": "system", "content": "You are a helpful assistant."}
chat_log.append(system_message)

loop = True


def main():
    global loop
    wake_word = "Jarvis"
    while loop:  # запускаем вечный цикл
        listen_for_wake_word(wake_word)
        print("Wake word detected, starting command loop...")
        # Слушайте команды и обрабатывайте их в этом цикле
        while True:
            text = recognize_from_microphone()
            if text == "Exit":  # Некоторая команда для выхода из цикла команд
                loop = False
                break

            else:
                user_speech = text  # преобразуем речь в текст
                user_message = {"role": "user", "content": user_speech}  # создаем сообщение от пользователя
                chat_log.append(user_message)  # добавляем сообщение от пользователя в список сообщений

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=chat_log
                )

                assistant_message = {"role": "assistant", "content": response['choices'][0]['message']['content']}
                chat_log.append(assistant_message)  # добавляем ответ от ассистента в список сообщений
                from_text_to_speak(assistant_message['content'])  # произносим ответ ассистента


if __name__ == "__main__":
    main()
