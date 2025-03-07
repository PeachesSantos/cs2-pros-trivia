#Add GUI for TGE Generator
import tkinter as tk
from tkinter import ttk
import os, csv, random

class appGUI:
    def __init__(self, master, csv_file):
        self.master = master
        
        #Set window title
        self.master.title("CS2 Player Trivia")
        #Set size in pixels
        self.master.geometry("500x500")

        self.data = self.load_data(csv_file)
        self.current_question = None
        self.correct_answers = []
        self.user_answers = set()
        self.guesses = 0 #Track number of guesses
        self.max_guesses = 0 #Initialize max guesses
        self.total_guesses = 0 #Initialize total guesses over entire session
        self.total_correct_answers = 0 #Initialize total correct answers over entire session
        self.guess_percentage = 0 #Guess Percentage
        
        #tkinter variables
        #Example Var
        self.string_variable = tk.StringVar()
        self.total_guesses_str = tk.StringVar()
        self.total_correct_answers_str = tk.StringVar()
        
        #font
        default_font_arg = 'Calibri 11 bold'

        #Add Widgets
        #Frame1
        frame1 = tk.Frame(master)
        #Pack and center align
        frame1.pack(pady=5, padx=10, anchor="center")

        #Title
        self.title_label = ttk.Label(frame1, text = "CS2 Pro Player Trivia", font = default_font_arg)
        self.title_label.pack()

        #Frame 2
        frame2 = tk.Frame(master)
        #Pack and center align
        frame2.pack(pady=5, padx=10, anchor="center")
        #Question Label
        self.question_label = ttk.Label(frame2, text = "", font = default_font_arg, justify='center')
        self.question_label.pack()

        # Entry for user input
        self.answer_entry = tk.Entry(frame2, font=default_font_arg)
        self.answer_entry.pack()
        
        # Button to check answer and load next card
        self.check_button = tk.Button(frame2, text="Submit Answer", command=self.check_answer)
        self.check_button.pack()

        # Label for feedback
        self.feedback_label = tk.Label(frame2, text="", font=default_font_arg)
        self.feedback_label.pack()

        # Label to show correct entries so far
        self.correct_label = tk.Label(frame2, text="", font=default_font_arg)
        self.correct_label.pack()

        #Frame 3 - display Guesses
        frame3 = tk.Frame(master)
        frame3.pack()
        # Label to show guesses
        self.guess_label = tk.Label(frame3, text="", font=default_font_arg)
        self.guess_label.pack()

        # Label for feedback
        self.correct_answer_feedback_label = tk.Label(frame3, text="", font=default_font_arg)
        self.correct_answer_feedback_label.pack()
        
        #Frame 4 - display Guesses percentage
        frame4 = tk.Frame(master)
        frame4.pack(side="right")
        # Label to show guesses
        self.total_guesses_label = tk.Label(frame4, textvariable=self.total_guesses_str, font=default_font_arg)
        self.total_guesses_label.pack()
        # Label to show guesses
        self.total_correct_label = tk.Label(frame4, textvariable=self.total_correct_answers_str, font=default_font_arg)
        self.total_correct_label.pack()
        # Label to show guesses
        self.guess_percent_label = tk.Label(frame4, text="", font=default_font_arg)
        self.guess_percent_label.pack()
        
        #Load the first question
        self.next_question()
        
    def load_data(self, csv_file):
        """Load data from CSV into a list of dictionaries."""
        data = []
        with open(csv_file, newline='', encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        return data

    def generate_question(self):
        #Collect all possible question generations and randomly generate a new one
        #questions_list = [generate_question_team_members, generate_question_age, generate_question_position]
        questions_list = [self.generate_question_team_members, self.generate_question_coaches, self.generate_question_roles, self.generate_question_nation]
        question, correct_names = random.choice(questions_list)()
        self.check_button["state"] == "enable"
        return question, correct_names

    def generate_question_team_members(self):
        """Generate a question based on the CSV data."""
        if not self.data:
            return None, []
        
        teams = list(set(person["Team"] for person in self.data))
        selected_team = random.choice(teams)

        correct_names = [person["Player"] for person in self.data if (person["Team"] == selected_team and person["Role"] != "Coach")]
        question = f"Name the current player roster for the following team: \n'{selected_team}'"
        #Set maximum guesses
        self.max_guesses = len(correct_names)
        
        return question, correct_names

    def generate_question_coaches(self):
        """Generate a question based on the CSV data."""
        if not self.data:
            return None, []
        
        teams = list(set(person["Team"] for person in self.data))
        selected_team = random.choice(teams)

        correct_names = [person["Player"] for person in self.data if (person["Team"] == selected_team and person["Role"] == "Coach")]
        question = f"Name the current Coach for the following team: \n'{selected_team}'"
        #Set maximum guesses
        self.max_guesses = len(correct_names)

        return question, correct_names

    def generate_question_roles(self):
        """Generate a question based on the CSV data."""
        if not self.data:
            return None, []
        
        players = list(set(person["Player"] for person in self.data))
        selected_player = random.choice(players)

        #roles = ["Rifler", "AWPer", "IGL", "Coach"]

        correct_names = [person["Role"] for person in self.data if (person["Player"] == selected_player)]
        question = f"Name the role of the following player: \n'{selected_player}' \n (IGL takes priority over Rifler/AWPer)"
        #Set maximum guesses
        self.max_guesses = len(correct_names)

        return question, correct_names
    
    def generate_question_nation(self):
        """Generate a question based on the CSV data."""
        if not self.data:
            return None, []
        
        players = list(set(person["Player"] for person in self.data))
        selected_player = random.choice(players)

        #roles = ["Rifler", "AWPer", "IGL", "Coach"]

        correct_names = [person["Native Land"] for person in self.data if (person["Player"] == selected_player)]
        question = f"Name the native land of the following player: \n'{selected_player}'"
        #Set maximum guesses
        self.max_guesses = len(correct_names)

        return question, correct_names

    def next_question(self):
        """Load a new question."""
        self.current_question, self.correct_answers = self.generate_question()
        self.user_answers.clear()
        self.guesses = 0 #reinitialize guess counter
        self.question_label.config(text=self.current_question)
        self.answer_entry.delete(0, tk.END)
        self.feedback_label.config(text="")
        self.guess_label.configure(text=f"Guesses: {self.guesses}/{self.max_guesses}")

        #Clear the previous question answer if desired
        #self.correct_answer_feedback_label.config(text="", fg="green")

    def check_answer(self):
        """Check if the user's entered name is correct."""
        user_input = self.answer_entry.get().strip()

        if not user_input:
            return
        
        #Get number of guesses
        self.guesses += 1
        self.total_guesses += 1
        self.guess_label.configure(text=f"Guesses: {self.guesses}/{self.max_guesses}")
        self.guess_percentage = 100*(self.total_correct_answers / self.total_guesses)
        self.guess_percent_label.configure(text=f"Accuracy: {self.guess_percentage}%")
            
        user_input_lower = user_input.lower()
        correct_lower = {name.lower() for name in self.correct_answers}

        if user_input_lower in correct_lower and user_input_lower not in {name.lower() for name in self.user_answers}:
            self.user_answers.add(user_input)
            self.feedback_label.config(text="Correct!", fg="green")
            self.total_correct_answers += 1

        else:
            self.feedback_label.config(text="Incorrect or already entered.", fg="red")

        # Update correct answers display
        self.correct_label.config(text=f"Correct answers: {', '.join(self.user_answers)}")

        # Clear entry field
        self.answer_entry.delete(0, tk.END)

        # Check if the user has provided enough correct answers
        if len(self.user_answers) >= self.max_guesses:
            self.feedback_label.config(text=f"You got all {self.max_guesses} correct! Moving to next question...", fg="green")
            self.master.after(2000, self.next_question)
        elif self.guesses >= self.max_guesses:
            self.feedback_label.config(text="Out of guesses! Moving to next question...", fg="gray")
            self.check_button["state"] == "disable"
            self.correct_answer_feedback_label.config(text=f"The correct answer was:\n {self.correct_answers}", fg="green")
            self.master.after(5000,self.next_question)
