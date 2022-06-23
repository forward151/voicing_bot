from gtts import gTTS


def google_translating(text, filename):
    var = gTTS(text=text, lang='ru')  # берем объект голоса, переведенного из текста
    var.save(filename)  # сохраняем в файл
