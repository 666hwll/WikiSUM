import wikipedia
import transformers
import tkinter 
from tkinter import messagebox
import gc
import pyttsx3



class programm:

    def __init__(self):
        self.results: str = ""
        self.readable: str = ""
        self.answer_read: str = ""
        #self.suffVAR = [] # [0] = original; [1] = summarization; [2] = answers
        ## Todo: make a list of values above
        self.state: int = 0


    def onclose(self) -> None:
        if tkinter.messagebox.askokcancel("Quit", "Do you want to quit?"):
            gc.collect(2)
            window.destroy()


    def change(self, userin: str, dl:bool, iNs:bool) -> None:
        if dl:
            text.delete(0.0, tkinter.END)
        if iNs:
            text.insert(tkinter.END, userin)


    def view_original(self) -> None:
        self.state = 0
        self.change(self.results, True, True)
        gc.collect(0)


    def get_sum(self) -> None:
        query = entrypoint.get()
        if query == "":
            self.change("No text provided", True, True)
        else:
            self.change("" ,True, False)
            entrypoint.delete(0, tkinter.END)
            gc.collect(1)
            self.results = wikipedia.summary(query, auto_suggest=True)
            results_sum = summarizer(self.results, max_length=1000, do_sample=False)
            self.readable = str(results_sum[0]['summary_text'])
            self.state = 1
            self.change(self.readable, False, True)


    def answer_Q(self) -> None:
        query = str(entrypoint.get())
        if query != "":
            if self.results == "":
                self.change("No context provided", True, True)
            else:
                entrypoint.delete(0, tkinter.END)
                a = question_answerer(question=query, context=self.results)
                self.answer_read = a['answer']
                self.state = 2
                self.change(self.answer_read, True, True)
        else:
            self.change("No question provided", True, True)
    

    def speak_r(self) -> None:
        text = ""
        if self.state == 0:
            text = self.results
        elif self.state == 1:
            text = self.readable
        elif self.state == 2:
            text = self.answer_read
        else:
            text = "Did not found valid text"
        speech.say(text)
        speech.runAndWait()


def main() -> None:
    #gc.set_debug(True)
    ## Todo: make global tuple to standart values or config values that don't need to change
    global speech, summarizer, question_answerer
    speech = pyttsx3.init()
    summarizer = transformers.pipeline("summarization", model="Falconsai/text_summarization")
    question_answerer = transformers.pipeline("question-answering", model="Falconsai/question_answering_v2")
    gc.disable()
    global window
    window = tkinter.Tk()
    processs = programm()
    window.protocol("WM_DELETE_WINDOW", processs.onclose)
    window.title("WikiSUM")
    window.geometry("800x800")
    window.resizable(1,1)
    global entrypoint
    entrypoint = tkinter.Entry(window, width=19)
    global text
    text = tkinter.Text(window, width=40, height=35)
    buttonZ = tkinter.Button(window, text="ORIGINAL", command=processs.view_original, underline=7)
    buttonY = tkinter.Button(window, text='SPEAK', command=processs.speak_r, underline=4)
    buttonA = tkinter.Button(window, text="SEARCH", command=processs.get_sum, fg='red', activeforeground='violet', underline=5)
    buttonB = tkinter.Button(window, text="ASK", command=processs.answer_Q, fg='red', activeforeground='violet', underline=2)
    entrypoint.pack(fill='x', expand=True)
    buttonA.pack(fill='x', expand=True)
    buttonZ.pack(fill='x', expand=True)
    buttonB.pack(fill='x', expand=True)
    buttonY.pack(fill='x', expand=True)
    text.pack(fill='both', expand=True)
    window.mainloop()


if __name__ == '__main__':
    main()


