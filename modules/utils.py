# libraries for text to audio 
from gtts import gTTS
import fasttext

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

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline


# Text Lang Detection\
pretrained_lang_model = "lid218e.bin" # Path of model file
modelTextDetection = fasttext.load_model(pretrained_lang_model)

# Language TRanslation

checkpoint = 'facebook/nllb-200-distilled-600M'
# checkpoint = ‘facebook/nllb-200–1.3B’
# checkpoint = ‘facebook/nllb-200–3.3B’
# checkpoint = ‘facebook/nllb-200-distilled-1.3B’

model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)
tokenizer = AutoTokenizer.from_pretrained(checkpoint)


def dectLang(text):
    predictions = model.predict(text, k=1)
    input_lang = predictions[0][0].replace('__label__', '')
    return input_lang

def text2textTranslation(source,target,text):
    translator = pipeline('translation', model=model, tokenizer=tokenizer, src_lang=source, tgt_lang=target, max_length = 400)
    output = translator(text)
    translated_text = output[0]['translation_text']
    return translated_text

def text_audio(translation_text, language , path):
    language_code = {'Bengali': 'bn', 'Gujarati': 'gu', 'Hindi': 'hi', 'Kannada': 'kn', 'Malayalam': 'ml', 'Tamil': 'ta'}
    lan = language_code[language]
    myobj = gTTS(text=translation_text, lang=lan, slow=False)
    myobj.save(path)
    return path


def video_audio(path, filename, folder):
    videoClip = VideoFileClip(os.path.join(path))
    aud_filename = filename.split('.')[0] + '.wav'
    videoClip.audio.write_audiofile(os.path.join(folder, aud_filename))
    aud_filepath = os.path.join(folder, aud_filename)
    return aud_filepath


def combine_audio_video(videopath, audiopath, combinedvideopath):
    videoclip = VideoFileClip(videopath)
    audioclip = AudioFileClip(audiopath)
    video = videoclip.set_audio(audioclip)
    video.write_videofile(combinedvideopath)


def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    r = sr.Recognizer()
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)  
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text
    # return the text for all chunks detected
    return whole_text







