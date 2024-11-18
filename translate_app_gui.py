import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledText
from ttkbootstrap.toast import ToastNotification
from tkinter.messagebox import showerror
import googletrans
from googletrans import Translator
import pyperclip
from gtts import gTTS
import os

translator = Translator()

class LanguageTranslator:
    def __init__(self, master):
        self.master = master
        self.MainWindow()
        self.Widgets()

    def MainWindow(self):
        self.master.geometry('800x430+350+250')
        self.master.title('Translator App Kelompok')
        self.master.resizable(width=0, height=0)
        icon = ttk.PhotoImage(file='icon.png')
        self.master.iconphoto(False, icon)

    def Widgets(self):
        self.canvas = ttk.Canvas(self.master, width=800, height=400)
        self.canvas.pack()
        self.logo = ttk.PhotoImage(file='logo.png').subsample(5, 5)
        self.canvas.create_image(75, 50, image=self.logo)

        language_data = googletrans.LANGUAGES
        self.language_codes = list(language_data.keys())
        languages = list(language_data.values())

        
        # Translate Kiri
        self.from_language = ttk.Combobox(self.canvas, width=36, bootstyle='primary', values=languages)
        self.from_language.current(0)
        self.canvas.create_window(200, 120, window=self.from_language)
        
        # Translate Swipe Icon Arrow
        self.arrow_icon = ttk.PhotoImage(file='arrows.png').subsample(15, 15)
        self.image_label = ttk.Label(self.master, image=self.arrow_icon, cursor="hand2")
        self.image_label.bind("<Button-1>", self.swap_languages)
        self.canvas.create_window(390, 120, window=self.image_label)

        # Translate Kanan
        self.to_language = ttk.Combobox(self.canvas, width=36, bootstyle='primary', values=languages)
        self.to_language.current(21)
        self.canvas.create_window(570, 120, window=self.to_language)
        
        # Scrolled Text 1
        self.from_text = ScrolledText(self.master, font=("Dotum", 10), width=33, height=10)
        self.canvas.create_window(195, 250, window=self.from_text)
        
        # Scrolled Text 2
        self.to_text = ScrolledText(self.master, font=("Dotum", 10), width=33, height=10)
        self.canvas.create_window(565, 250, window=self.to_text)
        
        self.speaker_icon = ttk.PhotoImage(file='speaker.png').subsample(5, 4)
        self.copy_icon = ttk.PhotoImage(file='copy.png').subsample(5, 4)
        
        self.speak_button = ttk.Button(self.master, image=self.speaker_icon, bootstyle='primary', state=ttk.DISABLED, command=self.speak)
        self.canvas.create_window(420, 355, window=self.speak_button)
        
        self.copy_button = ttk.Button(self.master, image=self.copy_icon, bootstyle='primary', state=ttk.DISABLED, command=self.copy_to_clipboard)
        self.canvas.create_window(460, 355, window=self.copy_button)
        
        self.translate_button = ttk.Button(self.master, text='Translate', width=20, bootstyle='primary', command=self.translate)
        self.canvas.create_window(370, 400, window=self.translate_button)

    def swap_languages(self):
        from_lang = self.from_language.get()
        to_lang = self.to_language.get()
        self.from_language.set(to_lang)
        self.to_language.set(from_lang)

    def translate(self):
        try:
            source_lang = self.language_codes[self.from_language.current()]
            destination_lang = self.language_codes[self.to_language.current()]
            text = self.from_text.get(1.0, ttk.END).strip()
            
            if text:
                translation = translator.translate(text, src=source_lang, dest=destination_lang)
                self.to_text.delete(1.0, ttk.END)
                self.to_text.insert(ttk.END, translation.text)
                
                self.speak_button.configure(state=ttk.ACTIVE)
                self.copy_button.configure(state=ttk.ACTIVE)
            else:
                showerror(title='Invalid Input', message='Please enter text to translate!')
        except Exception as e:
            showerror(title='Translation Error', message='Error occurred: ' + str(e))

    def speak(self):
        text = self.to_text.get(1.0, ttk.END).strip()
        lang_code = self.language_codes[self.to_language.current()]
        
        if text:
            try:
                tts = gTTS(text=text, lang=lang_code)
                tts.save("hasilTranslate.mp3")
                os.system("start hasilTranslate.mp3" if os.name == 'nt' else "hasilTranslate.mp3")
            except Exception as e:
                showerror(title="Speech Error", message="Error in speaking text: " + str(e))
        else:
            showerror(title="No Text", message="No text to speak!")

    def copy_to_clipboard(self):
        toast = ToastNotification(
            title='Clipboard',
            message='Teks Berhasil di Copy',
            duration=3000,
        )
        toast.show_toast()
        
        text = self.to_text.get(1.0, ttk.END).strip()
        pyperclip.copy(text)

root = ttk.Window(themename="cosmo")
application = LanguageTranslator(root)
root.mainloop()
