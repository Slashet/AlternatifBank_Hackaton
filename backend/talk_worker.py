import azure.cognitiveservices.speech as speechsdk
import json

speech_key = "6jsWgCKkyhW26lI4LLPq7Cw4tgAAXaiQ6BNr3WQIhmF5xTj6boWuJQQJ99BJAC5RqLJXJ3w3AAAYACOGRE5p"
service_region = "westeurope"
speech_endpoint = "https://westeurope.api.cognitive.microsoft.com"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, endpoint=speech_endpoint)

speech_config.speech_synthesis_voice_name = "tr-TR-EmelNeural"

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)



def talk(text):
    result = speech_synthesizer.speak_text_async(text).get()
    
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized to speaker for text [{}]".format(text))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
        print("Did you update the subscription info?")
