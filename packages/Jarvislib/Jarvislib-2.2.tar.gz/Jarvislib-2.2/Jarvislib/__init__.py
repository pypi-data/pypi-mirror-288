get_ipython().system('pip install simpleaudio')
get_ipython().system('pip install sounddevice')
get_ipython().system('pip install scipy')
get_ipython().system('pip install wavio')
get_ipython().system('pip install SpeechRecognition')
import simpleaudio as sa
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
import speech_recognition as sr
import webbrowser
import time
import datetime
hi = (["Привет","привет","Добрый вечер","Доброе утро","Доброй ночи","Здорово","Здарова","Здравстуй","Здравствуйте","Привет Джарвис","Джарвис Привет","Добрый вечер Джарвис","Доброе утро Джарвис","Доброй ночи Джарвис","Здорово Джарвис","Здарова Джарвис","Здравстуй Джарвис","Здравствуйте Джарвис"])
text = "пусто"



def pusk():
    global text
    text = "пусто"
    hour = int(datetime.datetime.now().hour)
    slushayu_name = 'slushayu.wav'
    wave_obj = sa.WaveObject.from_wave_file(slushayu_name)
    play = wave_obj.play()
    play.wait_done()
    play.stop()
    recording = sd.rec(int(5 * 44100), samplerate=44100, channels=2)
    sd.wait(2)
    write("recording.wav", 44100, recording)
    wv.write("recording.wav", recording, 44100, sampwidth=2)
    r = sr.Recognizer()
    with sr.AudioFile("recording.wav") as source:
        audio = r.record(source)
    try:
        text = r.recognize_google(audio, language="ru-RU")
        print("Text: "+text)
    except Exception as e:
        print("Exception: "+str(e))



    if hour>=0 and hour<12 and text in hi:
        zvuk = 'morning.wav'
        wave_obj = sa.WaveObject.from_wave_file(zvuk)
        play = wave_obj.play()
        play.wait_done()
        play.stop()
        pusk()
    elif hour>=12 and hour<18 and text in hi:
        zvuk = 'day.wav'
        wave_obj = sa.WaveObject.from_wave_file(zvuk)
        play = wave_obj.play()
        play.wait_done()
        play.stop()
        pusk()
    elif hour>=18 and hour<24 and text in hi:
        zvuk = 'evening.wav'
        wave_obj = sa.WaveObject.from_wave_file(zvuk)
        play = wave_obj.play()
        play.wait_done()
        play.stop()
        pusk()


    elif "погода " in text:
        zvuk = 'open.wav'
        wave_obj = sa.WaveObject.from_wave_file(zvuk)
        play = wave_obj.play()
        play.wait_done()
        play.stop()
        pogoda_fact, city = text.split('погода ')
        webbrowser.open_new_tab('https://yandex.ru/pogoda/search?request=' +city)


    elif "поиск" in text:
        zvuk = 'poisk.wav'
        wave_obj = sa.WaveObject.from_wave_file(zvuk)
        play = wave_obj.play()
        play.wait_done()
        play.stop()
        poisk2, poisk = text.split('поиск ')
        webbrowser.open_new_tab('https://yandex.ru/search/?text=' +poisk)
    elif "Найди" in text:
        zvuk = 'poisk.wav'
        wave_obj = sa.WaveObject.from_wave_file(zvuk)
        play = wave_obj.play()
        play.wait_done()
        play.stop()
        poisk2, poisk = text.split('Найди ')
        webbrowser.open_new_tab('https://yandex.ru/search/?text=' +poisk)
    elif "найти" in text:
        zvuk = 'poisk.wav'
        wave_obj = sa.WaveObject.from_wave_file(zvuk)
        play = wave_obj.play()
        play.wait_done()
        play.stop()
        poisk_fakt, poisk = text.split('найти ')
        webbrowser.open_new_tab('https://yandex.ru/search/?text=' +poisk)


    elif "Включи " in text:
        zvuk = 'on.wav'
        wave_obj = sa.WaveObject.from_wave_file(zvuk)
        play = wave_obj.play()
        play.wait_done()
        play.stop()
        music_fact, music = text.split('Включи ')
        webbrowser.open_new_tab('https://music.yandex.ru/search?text=' + music)
    elif "Включи песню" in text:
        zvuk = 'on.wav'
        wave_obj = sa.WaveObject.from_wave_file(zvuk)
        play = wave_obj.play()
        play.wait_done()
        play.stop()
        music_fact, music = text.split('Включи песню ')
        webbrowser.open_new_tab('https://music.yandex.ru/search?text=' + music)
    elif "песня" in text:
        zvuk = 'on.wav'
        wave_obj = sa.WaveObject.from_wave_file(zvuk)
        play = wave_obj.play()
        play.wait_done()
        play.stop()
        music_fact, music = text.split('песня ')
        webbrowser.open_new_tab('https://music.yandex.ru/search?text=' + music)


    elif "что выгоднее" in text:
        vvod_sravneniya = text
        meaningless, vvod_sravneniya = vvod_sravneniya.split('что выгоднее ')
        tovar1, tovar2 = vvod_sravneniya.split(' или ')
        t1t, t1p = tovar1.split(' за ')
        t2t, t2p = tovar2.split(' за ')
        t1t = int(t1t)
        t1p = int(t1p)
        t2t = int(t2t)
        t2p = int(t2p)
        t1result = t1p / t1t
        t2result = t2p / t2t
        if t1result < t2result:
            zvuk = 'perviy.wav'
            wave_obj = sa.WaveObject.from_wave_file(zvuk)
            play = wave_obj.play()
            play.wait_done()
            play.stop()
        elif t1result > t2result:
            zvuk = 'vtoroy.wav'
            wave_obj = sa.WaveObject.from_wave_file(zvuk)
            play = wave_obj.play()
            play.wait_done()
            play.stop()
        elif t1result == t2result:
            zvuk = 'ravni.wav'
            wave_obj = sa.WaveObject.from_wave_file(zvuk)
            play = wave_obj.play()
            play.wait_done()
            play.stop()


    elif text == "отмена":
        zvuk = 'ponial.wav'
        wave_obj = sa.WaveObject.from_wave_file(zvuk)
        play = wave_obj.play()
        play.wait_done()
        play.stop()


    elif text == "пока":
        zvuk = 'godbie.wav'
        wave_obj = sa.WaveObject.from_wave_file(zvuk)
        play = wave_obj.play()
        play.wait_done()
        play.stop()


    else:
        zvuk = 'neponial.wav'
        wave_obj = sa.WaveObject.from_wave_file(zvuk)
        play = wave_obj.play()
        play.wait_done()
        play.stop()
        pusk()



def potok():
    global text
    while text != "пока" and st_st == True:
        recording = sd.rec(int(5 * 44100), samplerate=44100, channels=2)
        sd.wait(0.7)
        write("recording.wav", 44100, recording)
        wv.write("recording.wav", recording, 44100, sampwidth=2)
        r = sr.Recognizer()
        with sr.AudioFile("recording.wav") as source:
            audio = r.record(source)
        try:
            text = r.recognize_google(audio, language="ru-RU")
            print("Text: "+text)
        except Exception as e:
            print("Exception: "+str(e))
        if text == "Джарвис" or text == "Джар" or text == "джар":
            pusk()
            time.sleep(0.7)
            potok()
        elif text == "пока":
            continue
        else:
            potok()



def status():
    global bt_st
    global st_st
    if bt_st == True:
        metka_1.set("Остановить")
        st_st = True
        bt_st = False
    else:
        metka_1.set("Запустить")
        st_st = False
        bt_st = True