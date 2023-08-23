# libraries for text to audio 
from gtts import gTTS
import fasttext
import pytube

# libraries for extract a audio from video and merge audio to video
# https://www.codespeedy.com/extract-audio-from-video-using-python/
# pip install ffmpeg moviepy
from moviepy.editor import *
import os

# libraries for audio to english text
# https://www.thepythoncode.com/article/using-speech-recognition-to-convert-speech-to-text-python
# pip3 install SpeechRecognition pydub
# https://www.arxiv-vanity.com/papers/1710.08969/

import speech_recognition as sr 
from pydub import AudioSegment
from pydub.silence import split_on_silence

# libraries for multilanguage translation
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# libraries for extract transcript from youtube link
from youtube_transcript_api import YouTubeTranscriptApi

# library for transliteration
from ai4bharat.transliteration import XlitEngine

# load a transliteration models
english2vernacular = XlitEngine(src_script_type="roman", beam_width=10, rescore=False)
vernacular2english = XlitEngine(src_script_type="indic", beam_width=10, rescore=False)

# Text Lang Detection
pretrained_lang_model = "modules/supportFile/lid218e.bin" # Path of model file
modelTextDetection = fasttext.load_model(pretrained_lang_model)

# Language TRanslation

checkpoint = 'facebook/nllb-200-distilled-600M'
# checkpoint = ‘facebook/nllb-200–1.3B’
# checkpoint = ‘facebook/nllb-200–3.3B’
# checkpoint = ‘facebook/nllb-200-distilled-1.3B’

model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)
tokenizer = AutoTokenizer.from_pretrained(checkpoint)

captioner = pipeline("image-to-text",model="Salesforce/blip-image-captioning-base")

def imageCaptioning(path):
    result = captioner(path)
    return result

common_language = {
    "Bengali": "ben_Beng",
    "Gujarati": "guj_Gujr",
    "Hindi": "hin_Deva",
    "Kannada": "kan_Knda",
    "Malayalam": "mal_Mlym",
    "Marathi": "mar_Deva",
    "Nepali": "npi_Deva",
    "Sinhala": "sin_Sinh",
    "Tamil": "tam_Taml",
    "Telugu": "tel_Telu",
    "Urdu": "urd_Arab",
    "English": "eng_Latn"
}

def dectLang(text):
    predictions = modelTextDetection.predict(text, k=1)
    input_lang = predictions[0][0].replace('__label__', '')
    return input_lang

def text2textTranslation(source,target,text):
    translator = pipeline('translation', model=model, tokenizer=tokenizer, src_lang=source, tgt_lang=target, max_length = 400)
    output = translator(text)
    translated_text = output[0]['translation_text']
    print(translated_text)
    return translated_text

# print(dectLang("صباح الخير، الجو جميل اليوم والسماء صافية."))
# print(text2textTranslation(source='arb_Arab',target='eng_lat', text="صباح الخير، الجو جميل اليوم والسماء صافية."))