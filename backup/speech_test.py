from time import sleep
import speech_recognition as sr

# obtain audio from the microphone
r = sr.Recognizer()
m = sr.Microphone()


def callback(recognizer, audio):
    try:
        print("Google Speech Recognition thinks you said " + recognizer.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


with m as source:
    r.adjust_for_ambient_noise(source)
    print("Ambiance adjusted..")
while True:
    print("Say something!")
    stop_listening = r.listen_in_background(m, callback)
    sleep(1)

# audio = r.listen(source)
# print "audio captured"
# try:
#     print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
# except sr.UnknownValueError:
#     print("Google Speech Recognition could not understand audio")
# except sr.RequestError as e:
#     print("Could not request results from Google Speech Recognition service; {0}".format(e))
