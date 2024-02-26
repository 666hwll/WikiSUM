from wikipedia import summary 
from transformers import pipeline
from tkinter import *

summarizer = pipeline("summarization", model="Falconsai/text_summarization")
question_answerer = pipeline("question-answering", model="Falconsai/question_answering_v2")
results = ""

class corpus:
    def change(self, userin) -> None:
        text.delete(0.0, END)
        text.insert(END, userin)

    def get_sum(self) -> None:
        global results
        query = entrypoint.get()
        if query == "":
            self.change("No text provided")
        else:
            text.delete(0.0, END)
            results = summary(query, auto_suggest=True)
            results_sum = summarizer(results, max_length=1000, do_sample=False)
            readable = str(results_sum[0]['summary_text'])
            text.insert(END, readable)

    def answer_Q(self) -> None:
        global results
        query = str(entrypoint.get())
        if query != "":
            if results == "":
                self.change("No context provided")
            else:
                a = question_answerer(question=query, context=results)
                answer_read = a['answer']
                self.change(answer_read)
        else:
            self.change("No question provided")

window = Tk()
processs = corpus()
window.title("WikiSUM")
window.geometry("800x800")
window.resizable(1,1)
entrypoint = Entry(window, width=20)
text = Text(window, width=40, height=35)

buttonA = Button(window, text="SEARCH", command=processs.get_sum)
buttonB = Button(window, text="ASK", command=processs.answer_Q)
entrypoint.pack()
buttonA.pack()
buttonB.pack()
text.pack()

window.mainloop()