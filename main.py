import config
import stt
import tts
from fuzzywuzzy import fuzz
import datetime
from num2t4ru import num2text
import webbrowser
import random

# start-up message
print(f"{config.VA_NAME} ({config.VA_VER}) start to work...")
tts.va_speak("Бог начал свою работу!")

def va_respond(voice: str):
    print(voice)

    if voice.startswith(config.VA_ALIAS):
        # contact an assistant
        cmd = recognize_cmd(filter_cmd(voice))

        if cmd['cmd'] not in config.VA_CMD_LIST.keys():
            tts.va_speak("Что?")
        else:
            execute_cmd(cmd['cmd'])


def filter_cmd(raw_voice: str):
    cmd = raw_voice

    for x in config.VA_ALIAS:
        cmd = cmd.replace(x, "").strip()

    for x in config.VA_TBR:
        cmd = cmd.replace(x, "").strip()

    return cmd


def recognize_cmd(cmd: str):
    rc = {'cmd': '', 'percent': 0}
    for c, v in config.VA_CMD_LIST.items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > rc['percent']:
                rc['cmd'] = c
                rc['percent'] = vrt

    return rc


def execute_cmd(cmd: str):
    if cmd == 'help':
        # help
        text = "Я умею: ..."
        text += "произносить время ..."
        text += "рассказывать анекдоты ..."
        text += "и открывать браузер"
        tts.va_speak(text)
        pass


    elif cmd == 'ctime':
        # current time
        now = datetime.datetime.now()
        text = "Сейчас " + num2text(now.hour) + " " + num2text(now.minute)
        tts.va_speak(text)


    elif cmd == 'joke':
        jokes = ['Дай яичницу, да и придумаю что-нибудь! ',
                 'Где моя яичница?! ...Я требую!',
                 'Внимание, анегдот!']

        tts.va_speak(random.choice(jokes))


    elif cmd == 'open_browser':
        webbrowser.open("https://www.google.com")


# start listenning comamnds
stt.va_listen(va_respond)