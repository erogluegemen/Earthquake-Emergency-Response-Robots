import speech_recognition as sr

recognizer = sr.Recognizer()

word_list = ['imdat', 'yardım', 'burdayım', 'kimse yok mu', 'acil', 'yardıma ihtiyacım var', 'sesimi duyan var mı', 'yardım edin', 
             'kurtarın', 'beni kurtarın', 'canım yanıyor', 'acil yardım gerekiyor', 'hemen gelin', 'lütfen yardım edin', 
             'acilen yardıma ihtiyacım var', 'birisi var mı', 'bana yardım edin', 'yardım bekliyorum', 'beni bulun', 
             'sesimi duyun', 'beni kurtarın', 'kurtar beni', 'ben buradayım', 'beni çıkarın', 'bana yardım et',
             'yardımcı olun', 'acilen yardıma ihtiyacım var', 'kurtulun', 'canım yanıyor', 'acil olarak yardıma ihtiyacım var', 
             'lütfen bana yardım edin', 'yardımcı olabilir misiniz', 'sesimi duyan birisi var mı', 'kurtarın beni lütfen', 
             'beni kurtaracak birisi var mı', 'acil durumdayım', 'hemen yardım lazım', 'acilen yardıma ihtiyacım var', 
             'yardıma ihtiyacım var lütfen', 'hemen yardım edin lütfen', 'ben buradayım yardım bekliyorum', 
             'kurtarın beni acil yardıma ihtiyacım var', 'sesimi duyan biri var mı', 'yardım edin beni kurtarın', 
             'beni kurtaracak birisi var mı', 'yardıma ihtiyacım var kimse yok mu', 'yardım edin hemen', 'beni kurtarın yardım edin']

def check_for_help(text:str) -> bool:
    for word in word_list:
        if word in text.lower():
            return True
    return False

with sr.Microphone() as source:
    print("Depremzede aranıyor...")
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)

    try:
        transcription = recognizer.recognize_google(audio, language="tr-TR")
        #print("Algılanan Ses:", transcription)
        if check_for_help(transcription):
            print("İnsan tespit edildi")
    except sr.UnknownValueError:
        print("Ses anlaşılamadı")
    except sr.RequestError as e:
        print("Sonuçlar alınırken hata oluştu; {0}".format(e))
