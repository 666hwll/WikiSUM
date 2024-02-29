#!usr/bin/python3.10
import wikipedia 
import transformers
import tkinter 

summarizer = transformers.pipeline("summarization", model="Falconsai/text_summarization")
question_answerer = transformers.pipeline("question-answering", model="Falconsai/question_answering_v2")
results = ""

class corpus:
    def change(self, userin: str, dl:bool, iNs:bool) -> None:
        if dl:
            text.delete(0.0, tkinter.END)
        if iNs:
            text.insert(tkinter.END, userin)

    def get_sum(self) -> None:
        global results
        query = entrypoint.get()
        if query == "":
            self.change("No text provided", True, True)
        else:
            self.change("" ,True, False)
            results = wikipedia.summary(query, auto_suggest=True)
            results_sum = summarizer(results, max_length=1000, do_sample=False)
            readable = str(results_sum[0]['summary_text'])
            self.change(readable, False, True)

    def answer_Q(self) -> None:
        global results
        query = str(entrypoint.get())
        if query != "":
            if results == "":
                self.change("No context provided", True, True)
            else:
                a = question_answerer(question=query, context=results)
                answer_read = a['answer']
                self.change(answer_read, True, True)
        else:
            self.change("No question provided", True, True)

window = tkinter.Tk()
processs = corpus()
window.title("WikiSUM")
window.geometry("800x800")
window.resizable(1,1)
entrypoint = tkinter.Entry(window, width=20)
text = tkinter.Text(window, width=40, height=35)

buttonA = tkinter.Button(window, text="SEARCH", command=processs.get_sum)
buttonB = tkinter.Button(window, text="ASK", command=processs.answer_Q)
entrypoint.pack()
buttonA.pack()
buttonB.pack()
text.pack()

window.mainloop()
