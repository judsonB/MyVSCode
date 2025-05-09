import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel, font
import json
import os # To check if file exists

# --- Constants ---
JSON_FILE = "MyPython/Jeopardy/jeopardy_questions.json"
MAX_CONTESTANTS = 4
DEFAULT_TIMER_SECONDS = 30
BG_COLOR = "#060CE9" # Jeopardy Blue
TEXT_COLOR = "white"
VALUE_COLOR = "#FFCC00" # Jeopardy Yellow
CAT_FONT = ("Arial", 12, "bold")
VAL_FONT = ("Arial", 16, "bold")
QA_FONT = ("Arial", 18)
SCORE_FONT = ("Arial", 12)
TIMER_FONT = ("Arial", 14, "bold")

# --- Utility Functions ---
def load_questions(filename):
    """Loads questions from a JSON file."""
    if not os.path.exists(filename):
        messagebox.showerror("Error", f"Question file not found: {filename}")
        return None
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # Basic validation (check if it's a dict and has list values)
        if not isinstance(data, dict):
            raise ValueError("JSON root must be a dictionary (object).")
        for category, questions in data.items():
            if not isinstance(questions, list):
                 raise ValueError(f"Category '{category}' must contain a list of questions.")
            for q in questions:
                if not all(key in q for key in ['points', 'question', 'answer']):
                    raise ValueError(f"Question in '{category}' is missing 'points', 'question', or 'answer'.")
        return data
    except json.JSONDecodeError as e:
        messagebox.showerror("JSON Error", f"Error decoding {filename}:\n{e}")
        return None
    except ValueError as e:
         messagebox.showerror("Data Error", f"Invalid data structure in {filename}:\n{e}")
         return None
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred loading questions:\n{e}")
        return None

# --- Dialog Classes ---
class SetupDialog(simpledialog.Dialog):
    """Dialog to get contestant names."""
    def __init__(self, parent, title="Setup Contestants"):
        self.contestant_entries = []
        self.result = []
        super().__init__(parent, title)

    def body(self, master):
        tk.Label(master, text=f"Enter contestant names (1 to {MAX_CONTESTANTS}):").grid(row=0, columnspan=2, pady=5)
        for i in range(MAX_CONTESTANTS):
            tk.Label(master, text=f"Contestant {i+1}:").grid(row=i+1, column=0, padx=5, sticky="w")
            entry = tk.Entry(master, width=30)
            entry.grid(row=i+1, column=1, padx=5, pady=2)
            self.contestant_entries.append(entry)
        return self.contestant_entries[0] # Initial focus

    def apply(self):
        self.result = [entry.get().strip() for entry in self.contestant_entries if entry.get().strip()]
        if not self.result:
            messagebox.showwarning("Input Error", "Please enter at least one contestant name.", parent=self)
            self.result = None # Indicate validation failure

class SettingsDialog(simpledialog.Dialog):
    """Dialog for changing game settings."""
    def __init__(self, parent, current_settings, contestant_names):
        self.current_settings = current_settings
        self.contestant_names = contestant_names
        self.result = None
        # --- Widgets ---
        self.timer_var = tk.BooleanVar(value=current_settings['timer_enabled'])
        self.time_limit_var = tk.StringVar(value=str(current_settings['time_limit']))
        self.name_entries = []
        super().__init__(parent, title="Game Settings")


    def body(self, master):
        # Timer settings
        timer_frame = tk.LabelFrame(master, text="Timer Settings", padx=10, pady=10)
        timer_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        tk.Checkbutton(timer_frame, text="Enable Question Timer", variable=self.timer_var).grid(row=0, column=0, sticky='w')
        tk.Label(timer_frame, text="Time Limit (seconds):").grid(row=1, column=0, sticky='w')
        self.time_limit_spinbox = tk.Spinbox(timer_frame, from_=5, to=120, width=5, textvariable=self.time_limit_var)
        self.time_limit_spinbox.grid(row=1, column=1, sticky='w')

        # Contestant Name Correction
        names_frame = tk.LabelFrame(master, text="Contestant Names", padx=10, pady=10)
        names_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        for i, name in enumerate(self.contestant_names):
             tk.Label(names_frame, text=f"Contestant {i+1}:").grid(row=i, column=0, padx=5, sticky="w")
             entry = tk.Entry(names_frame, width=30)
             entry.insert(0, name)
             entry.grid(row=i, column=1, padx=5, pady=2)
             self.name_entries.append(entry)

        return self.time_limit_spinbox # Initial focus

    def validate(self):
        try:
            limit = int(self.time_limit_var.get())
            if limit < 5:
                messagebox.showwarning("Input Error", "Time limit must be at least 5 seconds.", parent=self)
                return 0
            return 1
        except ValueError:
            messagebox.showwarning("Input Error", "Time limit must be a valid number.", parent=self)
            return 0

    def apply(self):
        new_names = [entry.get().strip() for entry in self.name_entries if entry.get().strip()]
        if not new_names:
             messagebox.showwarning("Input Error", "At least one contestant name is required.", parent=self)
             return # Keep dialog open

        self.result = {
            'timer_enabled': self.timer_var.get(),
            'time_limit': int(self.time_limit_var.get()),
            'contestant_names': new_names
        }

# --- Main Application Class ---
class JeopardyApp:
    """Manages the overall Jeopardy game application."""
    def __init__(self, root):
        self.root = root
        self.root.withdraw() # Hide the main empty root window initially

        self.questions_data = load_questions(JSON_FILE)
        if not self.questions_data:
            self.root.destroy() # Exit if questions failed to load
            return
        self.categories = list(self.questions_data.keys())
        # Assuming all categories have the same number of questions for grid layout
        self.num_questions_per_cat = len(self.questions_data[self.categories[0]]) if self.categories else 0

        # Game State
        self.contestants = [] # List of {'name': str, 'score': int}
        self.scores = [] # Parallel list just for scores (might be redundant but simple)
        self.current_question_widget = None # The button widget of the selected question
        self.current_question_data = None # The dict {'points':..., 'question':..., 'answer':...}
        self.last_score_change = None # Tuple (contestant_index, old_score, new_score) for undo

        # Settings State
        self.settings = {
            'timer_enabled': False,
            'time_limit': DEFAULT_TIMER_SECONDS,
        }
        self.timer_id = None
        self.time_remaining = 0
        # Windows
        self.host_window = None
        self.contestant_window = None

        # Run Setup
        if not self._run_setup():
             self.root.destroy()
             return # Exit if setup is cancelled or invalid

        # Initialize Windows
        self._init_windows()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close) # Handle closing the (hidden) root

    def _run_setup(self):
        """Runs the initial contestant setup dialog."""
        dialog = SetupDialog(self.root)
        if dialog.result:
            self.contestants = [{'name': name, 'score': 0} for name in dialog.result]
            self.scores = [0] * len(self.contestants)
            return True
        else:
            return False # Setup cancelled or failed validation


    def _init_windows(self):
        """Creates and configures the Host and Contestant windows."""
        # Host Window (can use the root window or a Toplevel)
        # Using Toplevel to keep root hidden and allow independent closing logic later if needed
        print("Hello")
        self.host_window = HostWindow(self.root, self)
        self.host_window.protocol("WM_DELETE_WINDOW", self._on_close)

        # Contestant Window
        self.contestant_window = ContestantWindow(self.root, self)
        self.contestant_window.protocol("WM_DELETE_WINDOW", self._on_close)

        # Position windows (simple cascade)
        self.root.update_idletasks() # Ensure window sizes are calculated
        host_w = self.host_window.winfo_width()
        host_h = self.host_window.winfo_height()
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        # Place host roughly top-left, contestant top-right
        self.host_window.geometry(f'+{screen_w//20}+{screen_h//20}')
        self.contestant_window.geometry(f'+{screen_w//2 - host_w//2 + screen_w//20}+{screen_h//20}')


    def get_question_data(self, category_index, question_index):
        """Retrieves question data based on indices."""
        category_name = self.categories[category_index]
        # Ensure questions are sorted by points if not already guaranteed by JSON
        sorted_questions = sorted(self.questions_data[category_name], key=lambda q: q['points'])
        if question_index < len(sorted_questions):
            return sorted_questions[question_index]
        return None

    def question_selected(self, cat_index, q_index, widget):
        """Handles logic when a question button is clicked on the host board."""
        if self.current_question_widget:
             # Prevent selecting a new question while one is active
             messagebox.showwarning("Game Flow", "Please resolve the current question first (reveal answer or manually clear).", parent=self.host_window)
             return

        self.current_question_widget = widget # Store the tk.Button
        self.current_question_data = self.get_question_data(cat_index, q_index)

        if not self.current_question_data:
             messagebox.showerror("Error", "Could not retrieve question data.", parent=self.host_window)
             self.current_question_widget = None
             return

        # Disable button on both boards
        widget.config(text="", state=tk.DISABLED, bg='gray')
        self.contestant_window.disable_question_button(cat_index, q_index)

        # Display on host
        self.host_window.display_question(
            self.current_question_data['question'],
            self.current_question_data['answer']
        )
        self.host_window.update_control_state(question_active=True)

        # Display on contestant
        self.contestant_window.display_question(self.current_question_data['question'])

        # Start timer if enabled
        if self.settings['timer_enabled']:
            self.start_timer()

    def reveal_answer(self):
        """Shows the answer on the contestant screen and clears active state."""
        if not self.current_question_data:
            return

        self.stop_timer() # Stop timer if running
        self.contestant_window.display_answer(self.current_question_data['answer'])
        self.host_window.update_control_state(question_active=False) # Enable scoring etc.

        # Allow selecting a new question after revealing
        # self.current_question_widget = None # Keep widget reference until points are awarded? Or clear now? Let's clear.
        # self.current_question_data = None # Keep data needed for scoring until cleared? Let's clear after reveal.

    def clear_current_question(self):
        """Manually clears the question display if needed (e.g., no one answered)."""
        self.stop_timer()
        self.host_window.clear_display()
        self.contestant_window.clear_display()
        self.host_window.update_control_state(question_active=False) # Re-enable controls
        self.current_question_widget = None
        self.current_question_data = None
        self.last_score_change = None # Clear undo state when question clears
        self.host_window.update_undo_button_state()


    def change_score(self, contestant_index, amount):
        """Updates a contestant's score."""
        if 0 <= contestant_index < len(self.scores):
            old_score = self.scores[contestant_index]
            new_score = old_score + amount
            self.scores[contestant_index] = new_score
            self.contestants[contestant_index]['score'] = new_score # Keep dict updated too

            # Store undo information
            self.last_score_change = (contestant_index, old_score, new_score)

            # Update displays
            self.host_window.update_score(contestant_index, new_score)
            self.contestant_window.update_score(contestant_index, new_score)
            self.host_window.update_undo_button_state()


    def undo_last_score_change(self):
        """Reverts the last score modification."""
        if self.last_score_change:
            contestant_index, old_score, _ = self.last_score_change
            self.scores[contestant_index] = old_score
            self.contestants[contestant_index]['score'] = old_score

            # Update displays
            self.host_window.update_score(contestant_index, old_score)
            self.contestant_window.update_score(contestant_index, old_score)

            # Clear undo state after using it
            self.last_score_change = None
            self.host_window.update_undo_button_state()

    def open_settings(self):
        """Opens the settings dialog."""
        initial_names = [c['name'] for c in self.contestants]
        dialog = SettingsDialog(self.host_window, self.settings, initial_names)
        if dialog.result:
            self.settings['timer_enabled'] = dialog.result['timer_enabled']
            self.settings['time_limit'] = dialog.result['time_limit']

            # Update contestant names if they changed
            if initial_names != dialog.result['contestant_names']:
                 new_names = dialog.result['contestant_names']
                 # Rebuild contestants list preserving scores
                 new_contestant_list = []
                 for i, name in enumerate(new_names):
                      # Try to match old score if name is the same or positionally
                      score = 0
                      if i < len(self.contestants):
                           # Heuristic: keep score if name hasn't changed drastically or position matches
                           # A more robust match might be needed for complex cases
                           # For simplicity, we just use the positional score if the list length hasn't shrunk
                           score = self.contestants[i]['score']

                      new_contestant_list.append({'name': name, 'score': score})

                 self.contestants = new_contestant_list
                 self.scores = [c['score'] for c in self.contestants]

                 # Update displays with new names/scores
                 self.host_window.rebuild_scoreboard()
                 self.contestant_window.rebuild_scoreboard()

            # Update timer display/state if needed
            self.host_window.update_timer_display() # Reflect new time limit if timer not running
            print("Settings updated:", self.settings) # Debug print

    def start_timer(self):
        """Starts the question timer."""
        self.stop_timer() # Ensure no duplicate timers
        self.time_remaining = self.settings['time_limit']
        self.host_window.update_timer_display(self.time_remaining)
        self._timer_tick()

    def _timer_tick(self):
        """Called every second by the timer."""
        self.time_remaining -= 1
        if self.time_remaining >= 0:
            self.host_window.update_timer_display(self.time_remaining)
            self.timer_id = self.root.after(1000, self._timer_tick) # Schedule next tick
        else:
            self.host_window.update_timer_display("Time's Up!")
            self.timer_id = None
            # Optional: Automatically reveal answer when time is up?
            # self.reveal_answer()

    def stop_timer(self):
        """Stops the currently running timer."""
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        # Optionally clear the timer display or leave the last value/message
        # self.host_window.update_timer_display() # Clears display

    def _on_close(self):
        """Handles window closing."""
        if messagebox.askokcancel("Quit", "Do you really want to quit the game?"):
            self.stop_timer() # Clean up timer
            self.root.destroy() # Close all windows


# --- Window Classes ---

class BaseWindow(Toplevel):
    """Base class for Host and Contestant windows."""
    def __init__(self, master, app, title):
        super().__init__(master, bg=BG_COLOR)
        self.app = app
        self.title(title)
        # self.geometry("900x700") # Adjust size as needed
        self.resizable(True, True)

        self.grid_frame = tk.Frame(self, bg=BG_COLOR, padx=10, pady=10)
        self.grid_frame.grid(row=0, column=0, sticky="nsew")

        self.display_frame = tk.Frame(self, bg=BG_COLOR, padx=10, pady=10)
        self.display_frame.grid(row=1, column=0, sticky="nsew")

        self.scoreboard_frame = tk.Frame(self, bg=BG_COLOR, padx=10, pady=10)
        self.scoreboard_frame.grid(row=2, column=0, sticky="nsew")

        self.grid_rowconfigure(0, weight=4) # Game board takes most space
        self.grid_rowconfigure(1, weight=2) # Display area
        self.grid_rowconfigure(2, weight=1) # Scoreboard
        self.grid_columnconfigure(0, weight=1)

        self.question_buttons = [[] for _ in self.app.categories] # Store button refs
        self.score_labels = [] # Store score label refs

        self._build_grid()
        self.rebuild_scoreboard()


    def _build_grid(self):
        """Creates the category and question value widgets."""
        for r in range(self.app.num_questions_per_cat + 1):
             self.grid_frame.rowconfigure(r, weight=1)
        for c in range(len(self.app.categories)):
             self.grid_frame.columnconfigure(c, weight=1)

        # Categories
        for c, category_name in enumerate(self.app.categories):
            lbl = tk.Label(self.grid_frame, text=category_name, font=CAT_FONT, bg=BG_COLOR, fg=TEXT_COLOR, wraplength=150, relief=tk.RAISED, borderwidth=2, padx=5, pady=10)
            lbl.grid(row=0, column=c, sticky="nsew", padx=2, pady=2)

        # Question buttons/placeholders will be added by subclasses

    def rebuild_scoreboard(self):
        """Clears and rebuilds the scoreboard display."""
        for widget in self.scoreboard_frame.winfo_children():
            widget.destroy()
        self.score_labels = []

        num_contestants = len(self.app.contestants)
        for i in range(num_contestants):
             self.scoreboard_frame.columnconfigure(i, weight=1) # Equal spacing for scores

        for i, contestant in enumerate(self.app.contestants):
            frame = tk.Frame(self.scoreboard_frame, bg=BG_COLOR)
            frame.grid(row=0, column=i, sticky="nsew", padx=5)

            name_lbl = tk.Label(frame, text=contestant['name'], font=SCORE_FONT, bg=BG_COLOR, fg=TEXT_COLOR)
            name_lbl.pack(pady=(0, 2))

            score_lbl = tk.Label(frame, text=f"${contestant['score']}", font=SCORE_FONT, bg=BG_COLOR, fg=VALUE_COLOR)
            score_lbl.pack()
            self.score_labels.append(score_lbl) # Store reference

    def update_score(self, contestant_index, new_score):
        """Updates the displayed score for a specific contestant."""
        if 0 <= contestant_index < len(self.score_labels):
            # Add $ sign and color based on value
            color = VALUE_COLOR if new_score >= 0 else "red"
            self.score_labels[contestant_index].config(text=f"${new_score}", fg=color)


class HostWindow(BaseWindow):
    """The Host's view of the game."""
    def __init__(self, master, app):
        super().__init__(master, app, "Jeopardy Host")

        self.question_display = None
        self.answer_display = None
        self.reveal_button = None
        self.clear_button = None
        self.undo_button = None
        self.settings_button = None
        self.timer_label = None
        self.score_buttons = [] # Store +/- buttons

        self._build_host_specific_grid()
        self._build_display_area()
        self.rebuild_scoreboard() # Overridden to add buttons
        self._build_control_panel()
        self.update_control_state(question_active=False) # Initial state
        self.update_undo_button_state()
        self.update_timer_display()

    def _build_host_specific_grid(self):
         # Question buttons (Interactive for Host)
         for c, category_name in enumerate(self.app.categories):
            sorted_questions = sorted(self.app.questions_data[category_name], key=lambda q: q['points'])
            col_buttons = []
            for r, q_data in enumerate(sorted_questions):
                points = q_data['points']
                btn = tk.Button(
                    self.grid_frame,
                    text=f"${points}",
                    font=VAL_FONT,
                    bg=BG_COLOR,
                    fg=VALUE_COLOR,
                    activebackground="blue",
                    activeforeground="white",
                    relief=tk.RAISED,
                    borderwidth=3,
                    # Use lambda to capture loop variables correctly
                    command=lambda cat_idx=c, q_idx=r, b=None: self.app.question_selected(cat_idx, q_idx, b)
                )
                 # Assign the button to 'b' in the lambda *after* creation
                btn.configure(command=lambda cat_idx=c, q_idx=r, b=btn: self.app.question_selected(cat_idx, q_idx, b))
                btn.grid(row=r + 1, column=c, sticky="nsew", padx=2, pady=2)
                col_buttons.append(btn)
            self.question_buttons[c] = col_buttons

    def _build_display_area(self):
        self.display_frame.columnconfigure(0, weight=1)
        self.display_frame.rowconfigure(0, weight=1) # Question
        self.display_frame.rowconfigure(1, weight=1) # Answer

        q_frame = tk.Frame(self.display_frame, bg="black", bd=2, relief=tk.SUNKEN)
        q_frame.grid(row=0, column=0, sticky="nsew", pady=5)
        q_frame.rowconfigure(0, weight=1)
        q_frame.columnconfigure(0, weight=1)
        self.question_display = tk.Label(q_frame, text="", font=QA_FONT, bg="black", fg=TEXT_COLOR, wraplength=500, justify=tk.CENTER)
        self.question_display.grid(sticky="nsew", padx=10, pady=10)

        a_frame = tk.Frame(self.display_frame, bg="black", bd=2, relief=tk.SUNKEN)
        a_frame.grid(row=1, column=0, sticky="nsew", pady=5)
        a_frame.rowconfigure(0, weight=1)
        a_frame.columnconfigure(0, weight=1)
        self.answer_display = tk.Label(a_frame, text="", font=QA_FONT, bg="black", fg=TEXT_COLOR, wraplength=500, justify=tk.CENTER)
        self.answer_display.grid(sticky="nsew", padx=10, pady=10)

    def rebuild_scoreboard(self):
        """Adds scoring buttons below the standard scoreboard."""
        super().rebuild_scoreboard() # Build names and score labels first
        self.score_buttons = []

        num_contestants = len(self.app.contestants)
        self.scoreboard_frame.rowconfigure(1, weight=0) # Row for buttons

        button_frame = tk.Frame(self.scoreboard_frame, bg=BG_COLOR)
        button_frame.grid(row=1, column=0, columnspan=num_contestants, pady=5)


        for i in range(num_contestants):
             # Create a sub-frame for each contestant's buttons for centering
            ind_button_frame = tk.Frame(button_frame, bg=BG_COLOR)
            ind_button_frame.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=20)

            add_btn = tk.Button(ind_button_frame, text="+", width=4, command=lambda idx=i: self._change_score_handler(idx, True))
            add_btn.pack(side=tk.LEFT, padx=5)
            sub_btn = tk.Button(ind_button_frame, text="-", width=4, command=lambda idx=i: self._change_score_handler(idx, False))
            sub_btn.pack(side=tk.LEFT, padx=5)
            self.score_buttons.append({'add': add_btn, 'sub': sub_btn})


    def _change_score_handler(self, contestant_index, add):
        """Handles clicks on +/- buttons, determining the amount."""
        if not self.current_question_data and not messagebox.askyesno("Manual Score Change", "No question is active. Manually change score?", parent=self):
            # Allow manual changes only if confirmed when no question is active
            return
        
        # If a question IS active, use its point value. Otherwise prompt? Or fixed amount?
        # Let's use the current question's points if available, otherwise prompt for safety/flexibility.
        points = 0
        if self.current_question_data:
             points = self.current_question_data.get('points', 0)
        else:
            # Prompt for amount for manual adjustment
            prompt_points = simpledialog.askinteger("Manual Score", "Enter points to add/subtract:", parent=self, minvalue=0)
            if prompt_points is None: # User cancelled
                 return
            points = prompt_points
        
        if points == 0: return # No change if points are zero

        amount = points if add else -points
        self.app.change_score(contestant_index, amount)


    def _build_control_panel(self):
         """Builds buttons like Reveal, Clear, Undo, Settings, and Timer display."""
         control_frame = tk.Frame(self, bg=BG_COLOR, pady=10)
         control_frame.grid(row=3, column=0, sticky="ew") # Below scoreboard

         # Make controls spread out
         control_frame.columnconfigure(0, weight=1) # Reveal
         control_frame.columnconfigure(1, weight=1) # Clear
         control_frame.columnconfigure(2, weight=1) # Undo
         control_frame.columnconfigure(3, weight=2) # Timer
         control_frame.columnconfigure(4, weight=1) # Settings


         self.reveal_button = tk.Button(control_frame, text="Reveal Answer", command=self.app.reveal_answer)
         self.reveal_button.grid(row=0, column=0, padx=10, pady=5)

         self.clear_button = tk.Button(control_frame, text="Clear Display", command=self.app.clear_current_question)
         self.clear_button.grid(row=0, column=1, padx=10, pady=5)

         self.undo_button = tk.Button(control_frame, text="Undo Score", command=self.app.undo_last_score_change, state=tk.DISABLED)
         self.undo_button.grid(row=0, column=2, padx=10, pady=5)

         self.timer_label = tk.Label(control_frame, text="", font=TIMER_FONT, bg=BG_COLOR, fg="yellow")
         self.timer_label.grid(row=0, column=3, padx=10, pady=5)

         self.settings_button = tk.Button(control_frame, text="Settings", command=self.app.open_settings)
         self.settings_button.grid(row=0, column=4, padx=10, pady=5)


    def display_question(self, question, answer):
        """Shows the question and answer on the host display."""
        self.question_display.config(text=question)
        self.answer_display.config(text=f"Answer: {answer}")

    def clear_display(self):
        """Clears the Q&A display areas."""
        self.question_display.config(text="")
        self.answer_display.config(text="")

    def update_control_state(self, question_active):
        """Enables/disables buttons based on whether a question is active."""
        if question_active:
            self.reveal_button.config(state=tk.NORMAL)
            self.clear_button.config(state=tk.NORMAL) # Allow clearing an active question
            # Disable scoring buttons while question is live? Maybe enable after reveal?
            # Let's disable them until answer is revealed or timer ends (handled by reveal/clear)
            for btn_pair in self.score_buttons:
                 btn_pair['add'].config(state=tk.DISABLED)
                 btn_pair['sub'].config(state=tk.DISABLED)
        else: # Question not active (either revealed, cleared, or before selection)
            self.reveal_button.config(state=tk.DISABLED)
            self.clear_button.config(state=tk.DISABLED) # Can't clear if nothing is displayed
            # Enable scoring buttons
            for btn_pair in self.score_buttons:
                 btn_pair['add'].config(state=tk.NORMAL)
                 btn_pair['sub'].config(state=tk.NORMAL)

    def update_undo_button_state(self):
        """Enables or disables the Undo button based on game state."""
        if self.app.last_score_change:
             self.undo_button.config(state=tk.NORMAL)
        else:
             self.undo_button.config(state=tk.DISABLED)

    def update_timer_display(self, time_text=None):
         """Updates the timer label. Shows empty if not enabled or no time."""
         if self.app.settings['timer_enabled']:
              if time_text is None: # Timer not running, show limit
                   self.timer_label.config(text=f"Timer: {self.app.settings['time_limit']}s")
              elif isinstance(time_text, int): # Timer running
                   self.timer_label.config(text=f"Time: {time_text}")
              else: # Custom text like "Time's Up!"
                    self.timer_label.config(text=str(time_text))
         else:
              self.timer_label.config(text="") # Hide timer if disabled


class ContestantWindow(BaseWindow):
    """The Contestants' view of the game."""
    def __init__(self, master, app):
        super().__init__(master, app, "Jeopardy Contestant View")
        self.question_display = None
        self.answer_display = None # Will be same label, just changing text

        self._build_contestant_specific_grid()
        self._build_display_area()
        # Scoreboard is built by base class

    def _build_contestant_specific_grid(self):
        # Question value placeholders (Non-interactive for Contestant)
        # Re-use grid built by BaseWindow, just add labels/disabled buttons
        for c, category_name in enumerate(self.app.categories):
            sorted_questions = sorted(self.app.questions_data[category_name], key=lambda q: q['points'])
            col_widgets = []
            for r, q_data in enumerate(sorted_questions):
                points = q_data['points']
                # Using Labels for non-interaction, styled like buttons
                lbl = tk.Label(
                    self.grid_frame,
                    text=f"${points}",
                    font=VAL_FONT,
                    bg=BG_COLOR,
                    fg=VALUE_COLOR,
                    relief=tk.RAISED,
                    borderwidth=3,
                    padx=5, pady=15 # Adjust padding to fill cell like button
                )
                lbl.grid(row=r + 1, column=c, sticky="nsew", padx=2, pady=2)
                col_widgets.append(lbl)
            self.question_buttons[c] = col_widgets # Store refs to update state

    def _build_display_area(self):
        self.display_frame.columnconfigure(0, weight=1)
        self.display_frame.rowconfigure(0, weight=1) # Single area for Q or A

        display_wrapper = tk.Frame(self.display_frame, bg="black", bd=2, relief=tk.SUNKEN)
        display_wrapper.grid(row=0, column=0, sticky="nsew", pady=10)
        display_wrapper.rowconfigure(0, weight=1)
        display_wrapper.columnconfigure(0, weight=1)

        self.question_display = tk.Label(display_wrapper, text="", font=QA_FONT, bg="black", fg=TEXT_COLOR, wraplength=600, justify=tk.CENTER)
        self.question_display.grid(sticky="nsew", padx=20, pady=20)
        # Initially hidden answer display can be the same label

    def disable_question_button(self, cat_index, q_index):
        """Visually disables a question value on the board."""
        if cat_index < len(self.question_buttons) and q_index < len(self.question_buttons[cat_index]):
            widget = self.question_buttons[cat_index][q_index]
            widget.config(text="", bg="gray", relief=tk.SUNKEN) # Change appearance

    def display_question(self, question):
        """Shows the question."""
        self.question_display.config(text=question, fg=TEXT_COLOR) # Ensure text color is standard

    def display_answer(self, answer):
        """Shows the answer (replaces the question)."""
        self.question_display.config(text=f"Answer: {answer}", fg=VALUE_COLOR) # Highlight answer

    def clear_display(self):
        """Clears the Q&A display area."""
        self.question_display.config(text="")


# --- Main Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Jeopardy Game") # Title for the hidden root/app controller
    # root.geometry("100x50") # Make root window small and potentially hide off-screen
    root.withdraw() # Hide the main root window, we only want Host and Contestant visible

    app = JeopardyApp(root)

    # Only run the main loop if the app initialized successfully (questions loaded, setup done)
    if app.host_window and app.contestant_window:
         root.mainloop()
    else:
         print("Application failed to initialize.")