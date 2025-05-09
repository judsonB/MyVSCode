import tkinter as tk
import json

def load_questions(filename):
    """Loads Jeopardy questions from a JSON file."""
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON.")
        return []

class JeopardyHost:
    def __init__(self, master, questions):
        self.master = master
        master.title("Jeopardy Host Control")
        self.questions_data = questions
        self.categories = [cat['name'] for cat in self.questions_data]
        self.num_categories = len(self.categories)
        self.questions_per_category = len(self.questions_data[0]['questions']) if self.questions_data else 0 # Assuming all categories have the same number of questions for layout

        self.contestant_names = ["Player 1", "Player 2", "Player 3"] # Initial names, will be configurable
        self.scores = {name: 0 for name in self.contestant_names}

        self.selected_question = None

        self._create_widgets()

    def _create_widgets(self):
        # Game Board (Categories and Point Values)
        for i, category in enumerate(self.categories):
            tk.Label(self.master, text=category, font=('Arial', 14, 'bold'), relief='ridge', width=15).grid(row=0, column=i, padx=5, pady=5)
            for j in range(self.questions_per_category):
                points = self.questions_data[i]['questions'][j]['points']
                button_text = str(points)
                button = tk.Button(self.master, text=button_text, font=('Arial', 12), width=10, command=lambda cat_index=i, q_index=j: self._select_question(cat_index, q_index))
                button.grid(row=j + 1, column=i, padx=5, pady=5)

        # Contestant Scores
        score_frame = tk.Frame(self.master)
        score_frame.grid(row=self.questions_per_category + 1, column=0, columnspan=self.num_categories, pady=10)
        for i, name in enumerate(self.contestant_names):
            tk.Label(score_frame, text=f"{name}:", font=('Arial', 12, 'bold')).grid(row=0, column=i * 2, padx=5)
            tk.Label(score_frame, text=str(self.scores[name]), font=('Arial', 12)).grid(row=0, column=i * 2 + 1, padx=5)

        # Control Buttons (Award/Deduct Points, Undo)
        control_frame = tk.Frame(self.master)
        control_frame.grid(row=self.questions_per_category + 2, column=0, columnspan=self.num_categories, pady=10)
        tk.Button(control_frame, text="Award Points", command=self._award_points).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Deduct Points", command=self._deduct_points).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Undo", command=self._undo_score_change).pack(side=tk.LEFT, padx=5)

        # Settings Button
        tk.Button(self.master, text="Settings", command=self._open_settings).grid(row=self.questions_per_category + 3, column=0, columnspan=self.num_categories, pady=10)

    def _select_question(self, category_index, question_index):
        print(f"Selected: Category {self.categories[category_index]}, Question {self.questions_data[category_index]['questions'][question_index]['points']}")
        self.selected_question = (category_index, question_index)
        # TODO: Display question on host and contestant screens

    def _award_points(self):
        if self.selected_question:
            # TODO: Implement point awarding logic
            print("Awarding points...")
        else:
            print("No question selected.")

    def _deduct_points(self):
        if self.selected_question:
            # TODO: Implement point deduction logic
            print("Deducting points...")
        else:
            print("No question selected.")

    def _undo_score_change(self):
        # TODO: Implement undo logic
        print("Undoing last score change...")

    def _open_settings(self):
        # TODO: Implement settings window
        print("Opening settings...")

def main():
    question_file = 'MyPython/Jeopardy/jeopardy_questions.json'
    questions = load_questions(question_file)
    if questions:
        root = tk.Tk()
        game = JeopardyHost(root, questions)
        root.mainloop()
    else:
        print("Failed to load questions. Cannot start the game.")

if __name__ == "__main__":
    main()