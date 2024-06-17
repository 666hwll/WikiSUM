import gc
import wikipedia
import gtts
import transformers
import tkinter
from tkinter import messagebox
from tkinter import filedialog
from just_playback import Playback
from tkinter import Menu


class programm:

    def __init__(self):
        self.pipe = ""
        self.results: str = ""
        self.readable: str = ""
        self.results_sum: dict = {}
        self.state: bool = False
        self.pipe_state: bool = False
        self.question_answerer = transformers.pipeline("question-answering", model="Falconsai/question_answering_v2")
        self.summarizer = transformers.pipeline("summarization", model="Falconsai/text_summarization")
        self.tts = Playback()

    def onclose(self) -> None:
        if tkinter.messagebox.askokcancel("Quit", "Do you want to quit?"):
            gc.collect(2)
            window.destroy()

    def close(self, event) -> None:
        window.destroy()

    def checkcurrtext(self):
        if self.state:
            tex = self.results
        elif self.state is False and self.readable != "":
            tex = self.readable
        else:
            tex = "Did not found valid text"
        return tex

    def open_file(self) -> None:
        p: str = filedialog.askopenfilename()
        with open(p, encoding="utf-8") as f:
            query = f.read()
            self.pipe = str(query)
            self.pipe_state = True

    def save_file(self) -> None:
        txt = ''.join(self.results + '\n\n' + str(self.results_sum[0]['summary_text']) + '\n\n' + self.readable + '\n\n')
        p: str = filedialog.asksaveasfile(mode='w')
        p.write(txt)

    def change(self, userin: str, dl: bool, iNs: bool) -> None:
        if dl:
            text.delete(0.0, tkinter.END)
        if iNs:
            text.insert(tkinter.END, userin)

    def copytoclip(self, event):
        a = self.checkcurrtext()
        #pyclip.copy(a)

    def view_original(self) -> None:
        self.state = True
        self.change(self.results, True, True)
        gc.collect(0)

    def get_sum(self) -> None:
        query = ""
        if self.pipe_state:
            query = self.pipe

        else:
            query = str(entrypoint.get())
            if query == "":
                self.change("No text provided", True, True)
        self.pipe_state = False

        self.change("", True, False)
        entrypoint.delete(0, tkinter.END)

        gc.collect(1)

        self.results = wikipedia.summary(query, auto_suggest=True)

        self.results_sum = self.summarizer(self.results, max_length=1000, do_sample=False)
        self.readable = str(self.results_sum[0]['summary_text'])
        self.state = False
        self.change(self.readable, False, True)

    def sum(self, event) -> None:
        self.get_sum()

    def answer_Q(self) -> None:
        query = ""
        if self.pipe_state:
            query = self.pipe
            self.pipe_state = False

        else:
            query = entrypoint.get()
            if query != "":
                if self.results == "":
                    self.change("No context provided", True, True)
                else:
                    entrypoint.delete(0, tkinter.END)

                gc.collect(0)
                a = self.question_answerer(question=query, context=self.results)
                self.readable = a['answer']
                self.state = False
                self.change(self.readable, True, True)
            else:
                self.change("No question provided", True, True)

    def speak_r(self) -> None:
        xet = self.checkcurrtext()
        obj = gtts.gTTS(text=xet, lang='en', slow=False)
        f: str = 'out.mp3'
        obj.save(f)
        self.tts.load_file(f)
        self.tts.play()


def main() -> None:
    # gc.set_debug(True)
    gc.disable()
    global window
    window = tkinter.Tk()
    processs = programm()
    window.protocol("WM_DELETE_WINDOW", processs.onclose)
    window.title("WikiSUM")
    window.geometry("800x800")
    window.resizable()
    window.bind("<Control-q>", processs.close)

    menubar = Menu(window)
    window.config(menu=menubar)

    file_menu = Menu(menubar)
    file_menu.add_command(label='Open', command=processs.open_file)
    file_menu.add_command(label='Save as file', command=processs.save_file)
    file_menu.add_command(label='Exit (ctrl-q)', command=window.destroy)
    menubar.add_cascade(label='File', menu=file_menu)

    about_menu = Menu(menubar)
    menubar.add_cascade(label='About', menu=about_menu)


    global entrypoint
    entrypoint = tkinter.Entry(window, width=19)
    global text
    text = tkinter.Text(window, width=40, height=35)
    buttonZ = tkinter.Button(window, text="ORIGINAL", command=processs.view_original, underline=7)
    buttonY = tkinter.Button(window, text='SPEAK', command=processs.speak_r, underline=4)
    buttonA = tkinter.Button(window, text="SEARCH", command=processs.get_sum, fg='red', activeforeground='violet', underline=5)
    buttonB = tkinter.Button(window, text="ASK", command=processs.answer_Q, fg='red', activeforeground='violet', underline=2)
    entrypoint.pack(fill='x', expand=True)
    entrypoint.bind("<Return>", processs.sum)
    entrypoint.bind("<Control-c>", processs.copytoclip)

    buttonA.pack(fill='x', expand=True)
    buttonZ.pack(fill='x', expand=True)
    buttonB.pack(fill='x', expand=True)
    buttonY.pack(fill='x', expand=True)
    text.pack(fill='both', expand=True)
    window.mainloop()


if __name__ == '__main__':
    main()

