import azure.cognitiveservices.speech as speechsdk

def speech():
    speech_key = "6jsWgCKkyhW26lI4LLPq7Cw4tgAAXaiQ6BNr3WQIhmF5xTj6boWuJQQJ99BJAC5RqLJXJ3w3AAAYACOGRE5p"
    service_region = "westeurope"
    speech_endpoint = "https://westeurope.api.cognitive.microsoft.com/"

    # Speech config oluştur ve Türkçe dilini ayarla
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, endpoint=speech_endpoint)
    speech_config.speech_recognition_language = "tr-TR"  # Türkçe dil desteği

    # Varsayılan mikrofon kullanımını açıkça belirt
    audio_config = speechsdk.AudioConfig(use_default_microphone=True)

    # Speech recognizer'ı audio config ile birlikte oluştur
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config,
        audio_config=audio_config
    )

    # Ses tanıma işlemini başlat
    result = speech_recognizer.recognize_once()

    # Sonucu kontrol et ve döndür
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    else:
        return ""