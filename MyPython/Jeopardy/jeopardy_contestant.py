import tkinter as tk

class JeopardyContestant:
    def __init__(self, master):
        self.master = master
        master.title("Jeopardy Contestant Screen")
        self.question_label = tk.Label(master, text="Please wait for the host to select a question...", font=('Arial', 16), wraplength=800, justify='center')
        self.question_label.pack(pady=50)
        self.answer_label = tk.Label(master, text="", font=('Arial', 14, 'italic'), wraplength=800, justify='center')
        self.answer_label.pack(pady=20)
        self.reveal_answer_button = tk.Button(master, text="Reveal Answer", font=('Arial', 12), command=self._reveal_answer)
        self.reveal_answer_button.pack(pady=10)
        self.reveal_answer_button.config(state=tk.DISABLED) # Initially disabled

    def display_question(self, question_text):
        self.question_label.config(text=question_text)
        self.answer_label.config(text="") # Clear any previous answer
        self.reveal_answer_button.config(state=tk.NORMAL) # Enable the reveal button

    def display_answer(self, answer_text):
        self.answer_label.config(text=f"Answer: {answer_text}")
        self.reveal_answer_button.config(state=tk.DISABLED) # Disable after revealing

    def _reveal_answer(self):
        # This will eventually be triggered by the host
        print("Reveal Answer button pressed (contestant screen)")
        # For now, we'll just show a placeholder if the answer isn't being sent from the host yet.
        if hasattr(self, 'current_answer'):
            self.display_answer(self.current_answer)
        else:
            self.display_answer("Answer will be shown by the host.")

    def set_current_answer(self, answer):
        self.current_answer = answer

def main_contestant():
    root = tk.Tk()
    contestant_screen = JeopardyContestant(root)
    root.mainloop()

if __name__ == "__main__":
    # You can run this to see the contestant screen independently
    # main_contestant()
    pass