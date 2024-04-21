import tkinter
import tkinter.messagebox
import customtkinter as ctk
import threading
from PIL import Image, ImageTk
import g4f
import speech_recognition as sr
import pyttsx3
from gtts import gTTS
from playsound import playsound
import pygame


#AI Bot setup code

def speechrec():
    r = sr.Recognizer()
    
    with sr.Microphone() as source: 
        print('Say something')
        #r.pause_threshold = 0.5
        #r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        recognized_text = r.recognize_google(audio, language = 'uk-UA').lower()
        print(recognized_text)

    except sr.UnknownValueError:
        print('Repeat again, please.')
        recognized_text = speechrec()

    print(recognized_text)  
    return recognized_text

def format_response(response: str, width: int):
    words = response.split()
    formatted_lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 <= width:
            current_line += word + " "
        else:
            formatted_lines.append(current_line)
            current_line = word + " "
    # Добавляем оставшееся слово
    if current_line:
        formatted_lines.append(current_line)

    return "\n".join(formatted_lines).strip()

def ask_gpt(messages: list) -> str:
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_35_turbo,
        messages=messages
    )
    #response = format_response(response, 68)
    print(response)
    return response


def get_recent_messages(messages, max_history=8):
    recent_messages = [messages[0]]
    recent_messages.extend(messages[-max_history:])
    return recent_messages


def startConversation():
    messages = [{"role": "system", "content": "You are a mental therapist named Oasis. You must help people overcome their fears and internal emotional problems. Anwser only using Ukrainian language. Don't take more that 5 seconds for generating anwser and don't write more than 4-5 lines. Help people cope with personal problems such as stress, anxiety, depression, relationship problems, self-esteem issues and others. You must analyze problems and guide people and give the right advice in the situations described. Help people understand and change their thinking, emotions and behavior."}]

    while True:
        question = input()
        messages.append({"role": "user", "content": question})
    
        answer = ask_gpt(messages=get_recent_messages(messages))
        messages.append({"role": "system", "content": answer})

        messages = get_recent_messages(messages)

# Function to switch menus
prevMenu = 0


def switchMenu(menuName):
    global prevMenu
    for fr in [infoMenu, preferencesMenu, startMenu, conversationMenu, soundMenu, practiceMenu]:
        if fr is menuName and (menuName == preferencesMenu or menuName == infoMenu):
            clear_window(app)
            fr.place(relx=0.5, rely=0.5, anchor="center")
            prevMenu = 1
        elif fr is menuName and prevMenu == 1:
            clear_window(app)
            mainMenuInit()
            prevMenu = 2
        elif fr is menuName:
            fr.place(relx=0.687, rely=0.53, anchor="center")
        else:
            fr.place_forget()

    if prevMenu == 2:
        startMenu.place(relx=0.687, rely=0.53, anchor="center")

# Clearing 
def clear_window(root):
    for widget in root.winfo_children():
        widget.place_forget()

def exitApp():
    app.destroy()

app = ctk.CTk()

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

app.geometry(f"{screen_width}x{screen_height}+0+0")
app.title("Oasis")
app.resizable(False, False)


# Start Menu page/frame widgets
startMenu = ctk.CTkFrame(master=app, width=1100, height=800, fg_color="transparent")

frameGreeting = ctk.CTkFrame(master=startMenu, width=500, height=400, corner_radius=30, fg_color="transparent", border_color="grey", border_width=2)
frameGreeting.place(relx=0.5, rely=0.45, anchor="center")
    
textGreeting = ctk.CTkLabel(master=startMenu, text = "Welcome to Oasis,\n a mental caring app\n which would help you\n deal with internal\n worries and problems", font=("Rockwell", 40), width = 300, height = 100, text_color="black", fg_color="transparent")
textGreeting.place(relx=0.5, rely=0.45, anchor="center")


# Conversation Menu page/frame widgets

messages = [{"role": "system", "content": "Привіт, розмовляй тільки українською. Ніколи не називай себе GPT, кажи, що ти психіатр на ім'я Оазис. Ви повинні допомогти людям подолати їхні страхи та внутрішні емоційні проблеми. Не кажи звертатися до інших фахівців або лікарів. Генеруйте швидку, коротку та глибоку відповідь. Не витрачайте більше 3 секунд на створення відповіді та не пишіть більше 4-5 рядків. Допоможіть людям впоратися з особистими проблемами, такими як стрес, тривога, депресія, проблеми у стосунках, проблеми з самооцінкою тощо. Ви повинні аналізувати проблеми, направляти людей і давати правильні поради в описаних ситуаціях. Допоможіть людям зрозуміти та змінити своє мислення, емоції та поведінку."}]
prevMessage = ""

def send_message():
    global messages
    global prevMessage
        
    question = entry_field.get()
    if (question != ""):
        display_message("You", question)
        messages.append({"role": "user", "content": question})
    
        answer = ask_gpt(messages=get_recent_messages(messages))
        messages.append({"role": "system", "content": answer})

        messages = get_recent_messages(messages)

        response = format_response(answer, 64)
        prevMessage = answer
        display_message("Oasis", response)
    entry_field.delete(0, 'end')

def send_speechrec_message():
    global messages
    global prevMessage
    
    question = speechrec()
    if (question != ""):
        display_message("You", question)
        messages.append({"role": "user", "content": question})
    
        answer = ask_gpt(messages=get_recent_messages(messages))
        messages.append({"role": "system", "content": answer})

        messages = get_recent_messages(messages)

        response = format_response(answer, 68)
        prevMessage = answer
        display_message("Oasis", response)
    entry_field.delete(0, 'end')

def display_message(sender, message):
    chatBox.configure(state='normal')
    chatBox.insert('end', f"{sender}: {message}\n")
    chatBox.insert('end', '\n')
    chatBox.configure(state='disabled')

def text_to_speech(text, lang='uk'):
    tts = gTTS(text=text, lang=lang)
    tts.save("temp.mp3")
    playsound("temp.mp3")

conversationMenu = ctk.CTkFrame(master=app, fg_color="transparent", width=1100, height=800)

chatBox = ctk.CTkTextbox(master=conversationMenu, width=1000, height=520, font=("Times New Roman", 30), text_color="black",
                         border_color="grey", border_width=2)
chatBox.configure(state=ctk.DISABLED)
chatBox.place(relx=0.5, rely=0.45, anchor="center")

entry_field = ctk.CTkEntry(master=conversationMenu, width=600, height=40, font=("Times New Roman", 20), text_color="black",
                         border_color="grey", border_width=2)
entry_field.place(relx=0.45, rely=0.8, anchor="center")
textUser = entry_field.get()

sendButton = ctk.CTkButton(master=conversationMenu, text="Send", width=100, height=40, command = send_message)
sendButton.place(relx=0.77, rely=0.8, anchor="center")

SROriginal = Image.open("C:/Users/Sasha/Documents/MAN/App/micro2.png") 
SRResized = SROriginal.resize((50, 50), Image.ANTIALIAS)  

SRButton = ctk.CTkButton(master=conversationMenu, text="", image=ImageTk.PhotoImage(SRResized), width=70, height=100, corner_radius=30,
                    fg_color="transparent", hover_color="#CAA7CD", border_color="black", border_width=2, command = lambda: send_speechrec_message()) 

VEOriginal = Image.open("C:/Users/Sasha/Documents/MAN/App/voiceover3Image.png") 
VEResized = VEOriginal.resize((50, 50), Image.ANTIALIAS)  

VEButton = ctk.CTkButton(master=conversationMenu, text="", image=ImageTk.PhotoImage(VEResized), width=70, height=100, corner_radius=30,
                    fg_color="transparent", hover_color="#CAA7CD", border_color="black", border_width=2, command = lambda: text_to_speech(prevMessage)) 


'''
scrollbar = ctk.CTkScrollbar(master=conversationMenu, width=20, height=100)
scrollbar.place(relx=0.9, rely=0.15)
'''

# Sound Menu page/frame widgets
soundMenu = ctk.CTkFrame(master=app, width=1100, height=800, fg_color="transparent", border_color="black", border_width=2)


sound_playing = False

# Initialize pygame mixer
pygame.mixer.init()

def play_soundForest():
    pygame.mixer.music.load("C:\\Users\\Sasha\\Documents\\MAN\\Sounds\\forestSound.mp3")
    pygame.mixer.music.play()
    
def play_soundWind():
    pygame.mixer.music.load("C:\\Users\\Sasha\\Documents\\MAN\\Sounds\\windSound.mp3")
    pygame.mixer.music.play()
    
def play_soundWaterdrops():
    pygame.mixer.music.load("C:\\Users\\Sasha\\Documents\\MAN\\Sounds\\waterdropsSound.mp3")
    pygame.mixer.music.play()

def play_soundCampfire():
    pygame.mixer.music.load("C:\\Users\\Sasha\\Documents\\MAN\\Sounds\\campfireSound.mp3")
    pygame.mixer.music.play()
    
def play_soundWaves():
    pygame.mixer.music.load("C:\\Users\\Sasha\\Documents\\MAN\\Sounds\\wavesSound.mp3")
    pygame.mixer.music.play()
    
def play_soundRainfall():
    pygame.mixer.music.load("C:\\Users\\Sasha\\Documents\\MAN\\Sounds\\rainfallSound.mp3")
    pygame.mixer.music.play()
    
def play_sound1Rel():
    pygame.mixer.music.load("C:\\Users\\Sasha\\Documents\\MAN\\Sounds\\relaxation1Sound.mp3")
    pygame.mixer.music.play()
    
def play_sound2Rel():
    pygame.mixer.music.load("C:\\Users\\Sasha\\Documents\\MAN\\Sounds\\relaxation2Sound.mp3")
    pygame.mixer.music.play()

def stop_sound():
    pygame.mixer.music.stop()




forestOriginal = Image.open("C:/Users/Sasha/Documents/MAN/App/forestIcon.png") 
forestResized = forestOriginal.resize((120, 120), Image.ANTIALIAS)  

forestRectangle = ctk.CTkFrame(master=soundMenu, width=200, height=300, fg_color="#FBF3D9", bg_color="white",
                              border_color="black", border_width=2)
forestRectangle.place(relx=0.01, rely=0.03, anchor = "nw")

forestSoundButton = ctk.CTkButton(master=soundMenu, text="", image=ImageTk.PhotoImage(forestResized), width=130, height=150, corner_radius=20,
                         bg_color="#FBF3D9", fg_color="white", hover_color="#BABABA", border_color="black", border_width=2, command = lambda: play_soundForest())
forestSoundButton.place(relx=0.1005, rely=0.15, anchor="center") 

forestText = ctk.CTkLabel(master=soundMenu, text="Forest Ambient Noises", font=("Times New Roman", 20), text_color="black", 
                          bg_color="#FBF3D9", fg_color="transparent")
forestText.place(relx=0.1005, rely=0.27, anchor="center")


windOriginal = Image.open("C:/Users/Sasha/Documents/MAN/App/windIcon.png") 
windResized = windOriginal.resize((120, 120), Image.ANTIALIAS)  

windRectangle = ctk.CTkFrame(master=soundMenu, width=200, height=300, fg_color="#FBF3D9", bg_color="transparent",
                            border_color="black", border_width=2)
windRectangle.place(relx=0.28, rely=0.03, anchor = "nw")

windSoundButton = ctk.CTkButton(master=soundMenu, text="", image=ImageTk.PhotoImage(windResized), width=130, height=150, corner_radius=20,
                         bg_color = "#FBF3D9", fg_color="white", hover_color="#BABABA", border_color="black", border_width=2, command = lambda: play_soundWind())
windSoundButton.place(relx=0.371, rely=0.15, anchor="center") 

windText = ctk.CTkLabel(master=soundMenu, text="Wind Blow Sound", font=("Times New Roman", 20), text_color="black", 
                          bg_color="#FBF3D9", fg_color="transparent")
windText.place(relx=0.371, rely=0.27, anchor="center")



waterdropOriginal = Image.open("C:/Users/Sasha/Documents/MAN/App/waterdropIcon.png") 
waterdropResized = waterdropOriginal.resize((120, 120), Image.ANTIALIAS)  

waterdropRectangle = ctk.CTkFrame(master=soundMenu, width=200, height=300, fg_color="#FBF3D9", bg_color="transparent",
                              border_color="black", border_width=2)
waterdropRectangle.place(relx=0.55, rely=0.03, anchor = "nw")

waterdropSoundButton = ctk.CTkButton(master=soundMenu, text="", image=ImageTk.PhotoImage(waterdropResized), width=130, height=150, corner_radius=20,
                         bg_color="#FBF3D9", fg_color="white", hover_color="#BABABA", border_color="black", border_width=2, command = lambda: play_soundWaterdrops())
waterdropSoundButton.place(relx=0.641, rely=0.15, anchor="center") 

waterdropText = ctk.CTkLabel(master=soundMenu, text="Waterdrop Sound", font=("Times New Roman", 20), text_color="black", 
                          bg_color="#FBF3D9", fg_color="transparent")
waterdropText.place(relx=0.641, rely=0.27, anchor="center")


firecampOriginal = Image.open("C:/Users/Sasha/Documents/MAN/App/firecampIcon.png") 
firecampResized = firecampOriginal.resize((120, 120), Image.ANTIALIAS)  

firecampRectangle = ctk.CTkFrame(master=soundMenu, width=200, height=300, fg_color="#FBF3D9", bg_color="transparent",
                              border_color="black", border_width=2)
firecampRectangle.place(relx=0.81, rely=0.03, anchor = "nw")

firecampSoundButton = ctk.CTkButton(master=soundMenu, text="", image=ImageTk.PhotoImage(firecampResized), width=130, height=150, corner_radius=20,
                         bg_color="#FBF3D9", fg_color="white", hover_color="#BABABA", border_color="black", border_width=2, command = lambda: play_soundCampfire())
firecampSoundButton.place(relx=0.901, rely=0.15, anchor="center") 

firecampText = ctk.CTkLabel(master=soundMenu, text="Firecamp Sound", font=("Times New Roman", 20), text_color="black", 
                          bg_color="#FBF3D9", fg_color="transparent")
firecampText.place(relx=0.901, rely=0.27, anchor="center")


wavesOriginal = Image.open("C:/Users/Sasha/Documents/MAN/App/wavesIcon.png") 
wavesResized = wavesOriginal.resize((120, 120), Image.ANTIALIAS)  

wavesRectangle = ctk.CTkFrame(master=soundMenu, width=200, height=300, fg_color="#FBF3D9", bg_color="transparent",
                              border_color="black", border_width=2)
wavesRectangle.place(relx=0.01, rely=0.47, anchor = "nw")

wavesSoundButton = ctk.CTkButton(master=soundMenu, text="", image=ImageTk.PhotoImage(wavesResized), width=130, height=150, corner_radius=20,
                         bg_color="#FBF3D9", fg_color="white", hover_color="#BABABA", border_color="black", border_width=2, command = lambda: play_soundWaves())
wavesSoundButton.place(relx=0.1005, rely=0.59, anchor="center") 

wavesText = ctk.CTkLabel(master=soundMenu, text="Sea Waves Sound", font=("Times New Roman", 20), text_color="black", 
                          bg_color="#FBF3D9", fg_color="transparent")
wavesText.place(relx=0.1005, rely=0.71, anchor="center")


rainfallOriginal = Image.open("C:/Users/Sasha/Documents/MAN/App/rainfallIcon.png") 
rainfallResized = rainfallOriginal.resize((120, 120), Image.ANTIALIAS)  

rainfallRectangle = ctk.CTkFrame(master=soundMenu, width=200, height=300, fg_color="#FBF3D9", bg_color="transparent",
                              border_color="black", border_width=2)
rainfallRectangle.place(relx=0.28, rely=0.47, anchor = "nw")

rainfallSoundButton = ctk.CTkButton(master=soundMenu, text="", image=ImageTk.PhotoImage(rainfallResized), width=130, height=150, corner_radius=20,
                         bg_color="#FBF3D9", fg_color="white", hover_color="#BABABA", border_color="black", border_width=2, command = lambda: play_soundRainfall())
rainfallSoundButton.place(relx=0.371, rely=0.59, anchor="center") 

rainfallText = ctk.CTkLabel(master=soundMenu, text="Rainfall Sound", font=("Times New Roman", 20), text_color="black", 
                          bg_color="#FBF3D9", fg_color="transparent")
rainfallText.place(relx=0.371, rely=0.71, anchor="center")


relaxation1Original = Image.open("C:/Users/Sasha/Documents/MAN/App/relaxation1Icon.png") 
relaxation1Resized = relaxation1Original.resize((120, 120), Image.ANTIALIAS)  

relaxation1Rectangle = ctk.CTkFrame(master=soundMenu, width=200, height=300, fg_color="#FBF3D9", bg_color="transparent",
                              border_color="black", border_width=2)
relaxation1Rectangle.place(relx=0.55, rely=0.47, anchor = "nw")

relaxation1SoundButton = ctk.CTkButton(master=soundMenu, text="", image=ImageTk.PhotoImage(relaxation1Resized), width=130, height=150, corner_radius=20,
                         bg_color="#FBF3D9", fg_color="white", hover_color="#BABABA", border_color="black", border_width=2, command = lambda: play_sound1Rel())
relaxation1SoundButton.place(relx=0.641, rely=0.59, anchor="center") 

relaxation1Text = ctk.CTkLabel(master=soundMenu, text="Relaxation Melody\n for Meditation", font=("Times New Roman", 20), text_color="black", 
                          bg_color="#FBF3D9", fg_color="transparent")
relaxation1Text.place(relx=0.641, rely=0.71, anchor="center")


relaxation2Original = Image.open("C:/Users/Sasha/Documents/MAN/App/relaxationmusicIcon.png") 
relaxation2Resized = relaxation2Original.resize((120, 120), Image.ANTIALIAS)  

relaxation2Rectangle = ctk.CTkFrame(master=soundMenu, width=200, height=300, fg_color="#FBF3D9", bg_color="transparent",
                              border_color="black", border_width=2)
relaxation2Rectangle.place(relx=0.81, rely=0.47, anchor = "nw")

relaxation2SoundButton = ctk.CTkButton(master=soundMenu, text="", image=ImageTk.PhotoImage(relaxation2Resized), width=130, height=150, corner_radius=20,
                         bg_color="#FBF3D9", fg_color="white", hover_color="#BABABA", border_color="black", border_width=2, command = lambda: play_sound2Rel())
relaxation2SoundButton.place(relx=0.901, rely=0.59, anchor="center") 

relaxation2Text = ctk.CTkLabel(master=soundMenu, text="Relaxation & Calming\n Melody", font=("Times New Roman", 20), text_color="black", 
                          bg_color="#FBF3D9", fg_color="transparent")
relaxation2Text.place(relx=0.901, rely=0.71, anchor="center")


stopCBtn = ctk.CTkButton(master=soundMenu, text = "Stop Playing Sound", font=("Bell MT", 20), width=350, height=70, corner_radius=32, text_color="black",
                        fg_color="transparent", hover_color="#CAA7CD", border_color="black", border_width=2, command=lambda: stop_sound())
stopCBtn.place(relx=0.5, rely=0.94, anchor="center")
stopCBtnLine = ctk.CTkFrame(master=soundMenu, width=50, height=1, fg_color="black", bg_color="black", border_color="black")
stopCBtnLine.place(relx=0.5, rely=0.96, anchor="center")   

# Practice Menu page/frame widgets
practiceMenu = ctk.CTkFrame(master=app, fg_color="transparent", width=1100, height=800)


def display_meditation_instructions():
    instructions_text.configure(state=ctk.NORMAL)
    instructions_text.delete("1.0", ctk.END)

    meditation_instructions = """Медитація - це практика, яка спрямована на зосередження розуму, релаксацію та духовний розвиток. Вона може мати багато користей для фізичного та психічного здоров'я. Кожен може знайти свій власний підхід до медитації та вибрати той метод, який найбільше відповідає їхнім потребам і цілям. При практиці медитації важливо дотримуватися регулярності та поступово розвивати свої навички. Користь медитації:"""
    meditation_instructions = format_response(meditation_instructions, 72)  
    instructions_text.insert(ctk.END, meditation_instructions)
    
    meditation_instructions = """
    \nЗниження стресу: Медитація допомагає знизити рівень стресу та \nтривожності. Вона сприяє заспокоєнню нервової системи та підвищує \nстресостійкість.
    \nПокращення концентрації: Практика медитації може покращити здатність \nзосереджуватися та підвищити продуктивність у повсякденній діяльності.
    \nПокращення самопочуття: Медитація може покращити емоційний стан, \nпідвищити відчуття щастя та сприяти психічному здоров'ю.
    \nФізичне здоров'я: Вона може покращити фізичне здоров'я шляхом \nзниження кров'яного тиску, покращення імунної системи та підвищення \nзагальної життєвої енергії.
    \nСпокій та рівновага: Медитація допомагає знайти внутрішній спокій та \nрівновагу в сучасному житті.
    \nІнструкції до основних типів медитації:
    
    1. Стандартна медитація:
        - Сядьте в комфортному положенні.
        - Закрийте очі та розслабтеся.
        - Зосередьте увагу на вашому диханні.
        - Глибоко вдихайте і повільно видихайте.
        - Відчувайте, як повітря входить і виходить з вашого тіла.
        - Якщо ваш розум блукає, поверніть увагу на дихання.
        - Продовжуйте медитувати протягом 10-20 хвилин.    
    
    2. Міндфульність (Mindfulness) або Відчуття дихання:
        - Користь: Покращення уваги, зосередженості та зниження стресу.
        - Інструкція:
          - Сідайте в зручному положенні.
          - Зосередьте увагу на своєму диханні.
          - Спостерігайте, як повітря входить і виходить з легень.
          - При відволіканні, повертайте увагу на дихання.
    
    3. Трансцендентальна медитація (Transcendental Meditation):
        - Користь: Зниження тривожності, збільшення креативності та 
          спрощення розуму.
        - Інструкція:
          - Використовуйте спеціальний мантру (слово або фразу), яку 
            повторюєте у своїх думках.
    
    4. Метафізична медитація (Loving-Kindness Meditation або Metta):
        - Користь: Підвищення рівня доброзичливості, гармонії та 
          внутрішнього спокою.
        - Інструкція:
          - Візьміть уявленням когось, кого ви любите і кому бажаєте 
            щасливості.
          Повторюйте фрази, які виражають щасливі побажання для цієї особи.
    
    5. Динамічна медитація (Vipassana):
        - Користь: Покращення уваги, відчуття свідомості та особистісного 
          розвитку.
        - Інструкція:
          - Спостерігайте власні думки, відчуття та відчуття без оцінки чи 
            судження.
          
    6. Трансцендентальна медитація (TM):
        - Користь: Зниження стресу, збільшення креативності та спрощення 
          розуму.
        - Інструкція:
          - Використовуйте спеціальний мантру (слово або фразу), яку 
            повторюєте у своїх думках.

    Для досягнення максимального ефекту регулярно практикуйте 
    медитацію.
    """
    instructions_text.insert(ctk.END, meditation_instructions)
    
    instructions_text.configure(state=ctk.DISABLED)

def display_breathing_techniques():
    instructions_text.configure(state=ctk.NORMAL)
    instructions_text.delete("1.0", ctk.END)

    breathing_instructions = """Дихальні вправи - це спеціальні техніки дихання, які можуть бути використані для поліпшення фізичного та психічного здоров'я. Вони можуть бути корисними для різних цілей, таких як зниження стресу, поліпшення концентрації, заспокоєння нервової системи, покращення спання та загального самопочуття. Ось деякі загальні користі та інформація про дихальні вправи:"""
    breathing_instructions = format_response(breathing_instructions, 68)  
    instructions_text.insert(ctk.END, breathing_instructions)
    
    breathing_instructions = """
    \nЗниження стресу: Дихальні вправи можуть допомогти знизити рівень \nстресу та тривожності. Коректне дихання сприяє релаксації та заспокоєнню \nнервової системи.
    \nПокращення концентрації: Деякі дихальні техніки сприяють покращенню зосередженості та пам'яті. Вони можуть допомогти підвищити \nпродуктивність та ефективність роботи.
    \nЗагальний стан здоров'я: Правильне дихання сприяє поліпшенню кисневого обміну в організмі, що може покращити загальний стан здоров'я та \nенергії.
    \nКонтроль над емоціями: Дихальні вправи можуть допомогти контролювати емоції, знижувати рівень роздратованості та агресії.
    \nПокращення якості сну: Деякі дихальні техніки можуть бути використані \nдля заспокоєння перед сном та покращення якості сну.
    \nЗниження болю: Дихальні вправи можуть допомогти знизити біль у \nвипадках напруження м'язів або головного болю.
    \nОсновні дихальні вправи:
    1. Дихання "животом":
       - Сідайте або лягайте зручно.
       - Покладіть руку на живіт.
       - Повільно вдихайте через ніс, відчуваючи, як живіт піднімається.
       - Повільно видихайте через рот, відчуваючи, як живіт опускається.

    2. Дихання з рахунком:
       - Сідайте або лягайте зручно.
       - Вдихайте в течії 4 рахунків.
       - Затримайте дихання на 4 рахунки.
       - Видихайте в течії 4 рахунків.
       - Повторюйте протягом 5-10 хвилин.
    
    3. Парні дихальні вправи:
       - Сідайте зручно або лягайте.
       - Закрийте одну нісельницю пальцем.
       - Вдихайте повільно і глибоко через іншу нісельницю на рахунок 
         чотири.
       - Затримайте дихання на рахунок сім.
       - Звільніть першу нісельницю та видихайте на рахунок вісім.
       - Повторюйте це на другу сторону, закривши іншу нісельницю.
       - Повторюйте кілька разів.
    
    4. Дихання за допомогою зірки(Box Breathing):
       - Сідайте або лягайте в зручному положенні.
       - Вдихайте на рахунок чотири.
       - Затримайте дихання на рахунок чотири.
       - Видихайте на рахунок чотири.
       - Затримайте дихання на рахунок чотири.
       - Повторюйте цей цикл кілька разів.
    """
    instructions_text.insert(ctk.END, breathing_instructions)
    instructions_text.configure(state=ctk.DISABLED)


textInstruction = ""

# Створення текстового поля для відображення інструкцій
instructions_text = ctk.CTkTextbox(master=practiceMenu, width=1000, height=620, font=("Times New Roman", 30), text_color="black",
                         border_color="grey", border_width=2)
instructions_text.place(relx=0.5, rely=0.4, anchor="center")
instructions_text.configure(state=ctk.DISABLED)

# Кнопка для відображення інструкцій медитації
meditation_button = ctk.CTkButton(master = practiceMenu, text = "Meditation Instructions", font=("Bell MT", 20), width=250, height=70, corner_radius=32, text_color="black",
                        bg_color="transparent", fg_color="transparent", hover_color="#CAA7CD", border_color="black", border_width=2, command=display_meditation_instructions)
meditation_button.place(relx=0.35, rely=0.9, anchor="center")
meditationBtnLine = ctk.CTkFrame(master=practiceMenu, width=50, height=1, fg_color="black", bg_color="black", border_color="black")
meditationBtnLine.place(relx=0.35, rely=0.92, anchor="center")   

# Кнопка для відображення інструкцій дихальних вправ
breathing_button = ctk.CTkButton(master = practiceMenu, text = "Breathing Techniques", font=("Bell MT", 20), width=250, height=70, corner_radius=32, text_color="black",
                        bg_color="transparent", fg_color="transparent", hover_color="#CAA7CD", border_color="black", border_width=2, command=display_breathing_techniques)
breathing_button.place(relx=0.65, rely=0.9, anchor="center")
breathingBtnLine = ctk.CTkFrame(master=practiceMenu, width=50, height=1, fg_color="black", bg_color="black", border_color="black")
breathingBtnLine.place(relx=0.65, rely=0.92, anchor="center")   



# Preferences Menu page/frame widgest
preferencesMenu = ctk.CTkFrame(master=app, width=1920, height=1080, fg_color="#EBEBEB")

preferencesLabel = ctk.CTkLabel(master=preferencesMenu, text="Preferences", font=("Rockwell", 60), text_color="black")
preferencesLabel.place(relx=0.5, rely=0.1, anchor="center")


def update_volume(value):
    volume = int(value)  
    pygame.mixer.music.set_volume(volume / 100.0)
    soundBar.configure(text=f"Volume: {volume}%")  

    
soundParameter = ctk.CTkLabel(master=preferencesMenu, text="Set Volume", font=("Rockwell", 40), text_color="black")
soundParameter.place(relx=0.3, rely=0.3, anchor="w")

soundBar = ctk.CTkSlider(master=preferencesMenu, from_=0, to=100, width=400, height=30, command=update_volume)
soundBar.place(relx=0.6, rely=0.3, anchor="center")
soundBar.set(50)


SRParameter = ctk.CTkLabel(master=preferencesMenu, text="Speech Recognition", font=("Rockwell", 40), text_color="black")
SRParameter.place(relx=0.35, rely=0.4, anchor="center")

switch_1 = ctk.CTkSwitch(master=preferencesMenu, text = "", height=30, width=50)
switch_1.place(relx=0.59, rely=0.4, anchor="w")

VEParameters = ctk.CTkLabel(master=preferencesMenu, text="Voiceover of the Message", font=("Rockwell", 40), text_color="black")
VEParameters.place(relx=0.35, rely=0.5, anchor="center")

switch_2 = ctk.CTkSwitch(master=preferencesMenu, text = "", height=30, width=50)
switch_2.place(relx=0.59, rely=0.5, anchor="w")


backPBtn = ctk.CTkButton(master = preferencesMenu, text = "Back", font=("Bell MT", 25), width=350, height=70, corner_radius=32, text_color="black",
                        fg_color="transparent", hover_color="#CAA7CD", border_color="black", border_width=2, command=lambda: switchMenu(startMenu))
backPBtn.place(relx=0.65, rely=0.85, anchor="center")
backPBtnLine = ctk.CTkFrame(master=preferencesMenu, width=50, height=1, fg_color="black", bg_color="black", border_color="black")
backPBtnLine.place(relx=0.65, rely=0.87, anchor="center")   

def saveChanges():
    if (switch_1.get() == 1 and switch_2.get() == 1):
        SRButton.place(relx=0.4, rely=0.92, anchor="center")
        VEButton.place(relx=0.6, rely=0.92, anchor="center")  
    elif (switch_1.get() == 1):
        SRButton.place(relx=0.5, rely=0.92, anchor="center") 
    elif (switch_2.get() == 1):
        VEButton.place(relx=0.5, rely=0.92, anchor="center") 
    if (switch_1.get() != 1):
        SRButton.place_forget()
    if (switch_2.get() != 1):
        VEButton.place_forget()

SaveCBtn = ctk.CTkButton(master = preferencesMenu, text = "Save Changes", font=("Bell MT", 25), width=350, height=70, corner_radius=32, text_color="black",
                        fg_color="transparent", hover_color="#CAA7CD", border_color="black", border_width=2, command =lambda: saveChanges())
SaveCBtn.place(relx=0.35, rely=0.85, anchor="center")
SaveCBtnLine = ctk.CTkFrame(master=preferencesMenu, width=50, height=1, fg_color="black", bg_color="black", border_color="black")
SaveCBtnLine.place(relx=0.35, rely=0.87, anchor="center")  



# Info Menu page/frame widgest
infoMenu = ctk.CTkFrame(master=app, width=1920, height=1080, fg_color="#EBEBEB")

infoLabel = ctk.CTkLabel(master=infoMenu, text="Info via Project", font=("Rockwell", 60), text_color="black")
infoLabel.place(relx=0.5, rely=0.1, anchor="center")

frameInfo = ctk.CTkFrame(master=infoMenu, width=900, height=500, corner_radius=30, fg_color="transparent", border_color="grey", border_width=2)
frameInfo.place(relx=0.5, rely=0.475, anchor="center")
    
textInfo = ctk.CTkLabel(master=infoMenu, text = "App version: v1.0\n\n Purpose of the app: the app provides a \n wealth of information and resources to \n help users deal with mental health issues.\n\n App creator: Oleksandr Yelovets", 
                        font=("Rockwell", 40), width = 300, height = 100, text_color="black", fg_color="transparent")
textInfo.place(relx=0.5, rely=0.45, anchor="center")

copyrightInfo = ctk.CTkLabel(master=infoMenu, text = "ⒸCopyright 2024, Oasis Mind. All rights are reserved. 24.01.2023", 
                        font=("Rockwell", 25), width = 300, height = 100, text_color="grey", fg_color="transparent")
copyrightInfo.place(relx=0.5, rely=0.65, anchor="center")

backIBtn = ctk.CTkButton(master = infoMenu, text = "Back", font=("Bell MT", 25), width=350, height=70, corner_radius=32, text_color="black",
                        fg_color="transparent", hover_color="#CAA7CD", border_color="black", border_width=2, command=lambda: switchMenu(startMenu))
backIBtn.place(relx=0.5, rely=0.85, anchor="center")
backIBtnLine = ctk.CTkFrame(master=infoMenu, width=50, height=1, fg_color="black", bg_color="black")
backIBtnLine.place(relx=0.5, rely=0.87, anchor="center")
    
def mainMenuInit():
    # MainMenu Rectangle and Label
    tabClr = "#2D2E43"
    menuTab = ctk.CTkFrame(master=app, width=500, height=1200, corner_radius=0, fg_color=tabClr, border_color="black", border_width=2)
    menuTab.place(relx=0.25, rely = 0.5, anchor="center")

    menuLabel = ctk.CTkLabel(master=app, text="Oasis Mind", font=("Rockwell", 60), text_color="black", fg_color="transparent")
    menuLabel.place(relx = 0.687, rely = 0.1, anchor = "center")

    # MainMenu Buttons
    conversationBtn = ctk.CTkButton(master=app, width=350, height=70, text="Start Conversation With Oasis", font=("Bell MT", 22), corner_radius=32, text_color="black", 
                                    fg_color="#70F2B4", hover_color="#4DCA8E", bg_color=tabClr, border_width=1, border_color="black", command=lambda: switchMenu(conversationMenu))
    conversationBtn.place(relx=0.25, rely=0.3, anchor="center")
    conversationBtnLine = ctk.CTkFrame(master=app, width=50, height=1 , fg_color="black", bg_color="black")
    conversationBtnLine.place(relx=0.25, rely=0.32, anchor = "center")

    soundBtn = ctk.CTkButton(master=app, width=350, height=70, text="Nature/Peaceful Sounds", font=("Bell MT", 22), corner_radius=32, text_color="black", fg_color="#F0A167", 
                             hover_color="#D3874F", bg_color=tabClr, border_width=1, border_color="black", command=lambda: switchMenu(soundMenu))
    soundBtn.place(relx=0.25, rely=0.45, anchor="center")
    soundBtnLine = ctk.CTkFrame(master=app, width=50, height=1, fg_color="black", bg_color="black")
    soundBtnLine.place(relx=0.25, rely=0.47, anchor = "center")
    
    practiceBtn = ctk.CTkButton(master=app, width=350, height=70, text="Practice", font=("Bell MT", 22), corner_radius=32, text_color="black", fg_color="#7370F2", 
                                hover_color="#5A57DE", bg_color=tabClr, border_width=1, border_color="black", command=lambda: switchMenu(practiceMenu))
    practiceBtn.place(relx=0.25, rely=0.60, anchor="center")
    practiceBtnLine = ctk.CTkFrame(master=app, width=50, height=1 , fg_color="black", bg_color="black")
    practiceBtnLine.place(relx=0.25, rely=0.62, anchor = "center")

    exitBtn = ctk.CTkButton(master=app, width=350, height=70, text="Exit", font=("Bell MT", 22), corner_radius=32, text_color="black", fg_color="#E12A56", 
                            hover_color="#BB2247", bg_color=tabClr, border_width=1, border_color="black", command=exitApp)
    exitBtn.place(relx=0.25, rely=0.75, anchor="center")
    exitBtnLine = ctk.CTkFrame(master=app, width=50, height=1, fg_color="white", bg_color="black", border_width=0)
    exitBtnLine.place(relx=0.25, rely=0.77, anchor = "center")
    

    preferencesOriginal = Image.open("C:/Users/Sasha/Documents/MAN/App/parametersImage.png") 
    preferencesResized = preferencesOriginal.resize((90, 90), Image.ANTIALIAS)  
    
    preferencesBtn = ctk.CTkButton(master=app, text="", image=ImageTk.PhotoImage(preferencesResized), width = 100, height = 100, fg_color="transparent", 
                                   hover_color="#CAA7CD", border_color="black", border_width=2, command=lambda: switchMenu(preferencesMenu))
    preferencesBtn.place(relx = 0.06, rely = 0.9, anchor = "center")


    infoOriginal = Image.open("C:/Users/Sasha/Documents/MAN/App/infoImage.png") 
    infoResized = infoOriginal.resize((80, 80), Image.ANTIALIAS)  
   
    infoBtn = ctk.CTkButton(master=app, text="", image=ImageTk.PhotoImage(infoResized), width = 100, height = 100, 
                            fg_color="transparent", hover_color="#CAA7CD", border_color="black", border_width=2, command=lambda: switchMenu(infoMenu))
    infoBtn.place(relx = 0.06, rely = 0.1, anchor = "center")

switchMenu(startMenu)    
mainMenuInit()



app.mainloop()
