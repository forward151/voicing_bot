from gtts import gTTS

def translate_text(text):
    var = gTTS(text=text, lang='ru')
    var.save('voice.ogg')


