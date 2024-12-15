import gc
import os
import logging
import webbrowser
import tkinter
import torch
from tkinter import messagebox
from tkinter import filedialog
from tkinter import Menu
import transformers
import wikipedia
import gtts
from just_playback import Playback


# todo: caching wikipedia answers and adding more ways to utilize cuda

def checkdevice() -> None:
    logging.info("Device is being Checked...")
    if torch.cuda.is_available():
        device = torch.device("cuda")
        # self.device_name = torch.cuda.get_device_name(0) # the name of the graphic chip
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        device = torch.device("mps")
    else:
        device = torch.device("cpu")
    logging.info(f"Device {device} was found.")
    return device


class programm:

    def __init__(self):
        self.in_s = ""
        self.pipe = ""
        self.results: str = ""
        self.readable: str = ""
        self.results_sum: dict = {}
        self.state: bool = False
        self.pipe_state: bool = False
        self.question_answerer = transformers.pipeline("question-answering", model="Falconsai/question_answering_v2",
                                                       device=device)
        self.summarizer = transformers.pipeline("summarization", model="Falconsai/text_summarization", device=device)
        self.tts = Playback()

    def onclose(self) -> None:
        logging.info("Ask user before quitting...")
        if tkinter.messagebox.askokcancel("Quit", "Do you want to quit?"):
            gc.collect(2)
            window.destroy()

    def close(self, event) -> None:
        logging.info("Destroying Window...")
        window.destroy()

    ### DUMMY FUNCTIONS for Testing Purposes
    def some(self) -> None:
        logging.info('This Element does work!')

    ### Actual Code continues ->>>>>>
    def donate(self) -> None:
        logging.info('Listing Donation Options...')
        self.change("Monero XMR Wallet: 48NYH8WqzWq4ccLLxFFcXM8KNwp4MnkvzJFpB85YeesPTFzAN4cXFaucjjoRXAJoib4yL1NWRh3nMFDaNNgRoV9x6gr16k6", True, True)
    
    def checkcurrtext(self):
        if self.state:
            tex = self.results
        elif self.state is False and self.readable != "":
            tex = self.readable
        else:
            tex = "Did not found valid text"
        return tex

    def open_file(self) -> None:
        logging.info("File Dialog is being startened...")
        p: str = filedialog.askopenfilename()
        with open(p, encoding="utf-8") as f:
            query = f.read()
            self.pipe = str(query)
            self.pipe_state = True

    def save_file(self) -> None:
        logging.info("About to compile the information...")
        txt = ''.join(
            self.results + '\n\n' + str(self.results_sum[0]['summary_text']) + '\n\n' + self.readable + '\n\n')
        p: str = filedialog.asksaveasfile(mode='w')
        p.write(txt)
        logging.info("Data was written to Disk.")

    def rmaudio(self) -> None:
        logging.info("About to clear the Audio Cache...")
        try:
            os.remove('out.mp3')
            self.change('Successfully cleared the Audio Cache!')
        except:
            self.change('No Audio Cache found to clear.', True, True)

    def showvar(self):
        logging.info("User will be shown parameters...")
        var = f"{device}, pipe:{self.pipe_state}"
        self.change(var, True, True)

    def wikifor(self) -> None:
        logging.info("Opening the wiki in the browser...")
        webbrowser.open("https://github.com/666hwll/WikiSUM/wiki")

    def showsource(self) -> None:
        logging.info("Project is opened in the browser.")
        webbrowser.open("https://github.com/666hwll/WikiSUM/")

    def change(self, userin: str, delete_text: bool, insert: bool) -> None:
        if delete_text:
            text.delete(0.0, tkinter.END)
        if insert:
            text.insert(tkinter.END, userin)

    def aboutP(self) -> None:
        logging.info("Revealing information about the Programm...")
        self.change("WikiSUM ALPHA 0.4.5\nby Darwin Zmugg\n Scrape and summarize the Wiki", True, True)

    def view_original(self) -> None:
        self.state = True
        self.change(self.results, True, True)
        gc.collect(0)

    def get_sum(self) -> bool:
        logging.info("Getting input for summary...")
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
        try:
            self.results = wikipedia.summary(query, auto_suggest=True)
        except:
            res = wikipedia.search(query)
            self.change(f"Well, no pages match you inquery; other pages are:{res}",
                        True, True)
            return False

        self.results_sum = self.summarizer(self.results, max_length=1000, do_sample=False)
        self.readable = str(self.results_sum[0]['summary_text'])
        self.state = False
        self.change(self.readable, False, True)
        return True

    def sum(self, event) -> None:
        self.get_sum()

    def answer_Q(self) -> None:
        logging.info("Questions are in process...")
        query = ""
        if self.pipe_state:
            query = self.pipe
            self.pipe_state = False

        else:
            query = entrypoint.get()  #
            if query != "":  #
                if self.results == "":
                    self.change("No context provided", True, True)  #
                else:  #
                    entrypoint.delete(0, tkinter.END)  #

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
        logging.info("Saved the Audio Buffer to Disk. Now it is being loaded and played...")
        self.tts.load_file(f)
        self.tts.play()


def main() -> None:
    global device
    device = checkdevice()
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

    options_menu = Menu(menubar)
    options_menu.add_command(label='Clear Audio Cache', command=processs.rmaudio)
    options_menu.add_command(label='Show Values', command=processs.showvar)
    menubar.add_cascade(label='Options', menu=options_menu)

    help_menu = Menu(menubar)
    help_menu.add_command(label='Source Code', command=processs.showsource)
    help_menu.add_command(label='Wiki', command=processs.wikifor)
    menubar.add_cascade(label='Help', menu=help_menu)

    about_menu = Menu(menubar)
    about_menu.add_command(label='About the Project', command=processs.aboutP)
    about_menu.add_command(label='Contact', command=processs.some)
    about_menu.add_command(label='Donate', command=processs.donate)
    menubar.add_cascade(label='About', menu=about_menu)

    global entrypoint
    entrypoint = tkinter.Entry(window, width=19)
    global text
    text = tkinter.Text(window, width=40, height=35)
    buttonZ = tkinter.Button(window, text="ORIGINAL", command=processs.view_original, underline=7)
    buttonY = tkinter.Button(window, text='SPEAK', command=processs.speak_r, underline=4)
    buttonA = tkinter.Button(window, text="SEARCH", command=processs.get_sum, fg='red', activeforeground='violet',
                             underline=5)
    buttonB = tkinter.Button(window, text="ASK", command=processs.answer_Q, fg='red', activeforeground='violet',
                             underline=2)
    entrypoint.pack(fill='x', expand=True)
    entrypoint.bind("<Return>", processs.sum)

    buttonA.pack(fill='x', expand=True)
    buttonZ.pack(fill='x', expand=True)
    buttonB.pack(fill='x', expand=True)
    buttonY.pack(fill='x', expand=True)
    text.pack(fill='both', expand=True)
    window.mainloop()


if __name__ == '__main__':
    main()
