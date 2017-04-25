import config
import telebot
import urllib.request

import speech_recognition as sr
from pydub import AudioSegment


bot = telebot.TeleBot(config.token)
r = sr.Recognizer()


@bot.message_handler(content_types=['audio', 'voice', ])
def echo_message(message):
    # bot.send_message(message.chat.id, message.text)
    file_id = message.voice.file_id
    voice_id = bot.get_file(file_id).file_path
    voice_link = 'https://api.telegram.org/file/bot{}/{}'.format(config.token, voice_id)
    oga_file_name = '{}.oga'.format(file_id)
    wav_file_name = '{}.oga'.format(file_id)
    urllib.request.urlretrieve(voice_link, oga_file_name)
    oga_version = AudioSegment.from_ogg(oga_file_name)
    oga_version.export(wav_file_name, format="wav")

    with sr.AudioFile(wav_file_name) as source:
        audio = r.record(source)  # read the entire audio file

    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        recognized_text = r.recognize_google(audio, language="ru-RU")
        print("Google Speech Recognition thinks you said " + recognized_text)
        bot.send_message(message.chat.id, recognized_text)

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

if __name__ == '__main__':
    bot.polling(none_stop=True)

