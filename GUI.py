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
        
        #tkinter variables
        #Example Var
        self.string_variable = tk.StringVar()

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
        self.check_button = tk.Button(frame2, text="Check Answer", command=self.check_answer)
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
        self.guess_label.pack(side="right")

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
        questions_list = [self.generate_question_team_members]
        question, correct_names = random.choice(questions_list)()
        return question, correct_names

    def generate_question_team_members(self):
        """Generate a question based on the CSV data."""
        if not self.data:
            return None, []
        
        teams = list(set(person["Team"] for person in self.data))
        selected_team = random.choice(teams)

        correct_names = [person["Player"] for person in self.data if person["Team"] == selected_team and person["Role"] != "Coach"]
        question = f"Name the current player roster for the following team: \n'{selected_team}'"
        #Set maximum guesses
        self.max_guesses = len(correct_names)
        
        return question, correct_names

    def generate_question_coaches(self):
        """Generate a question based on the CSV data."""
        if not self.data:
            return None, []
        #Set maximum guesses to 6
        self.max_guesses = 1
        
        teams = list(set(person["Team"] for person in self.data))
        selected_team = random.choice(teams)

        correct_names = [person["Player"] for person in self.data if person["Team"] == selected_team and person["Role"] != "Coach"]
        question = f"Name the current player roster for the following team: \n'{selected_team}'"
        
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

    def check_answer(self):
        """Check if the user's entered name is correct."""
        user_input = self.answer_entry.get().strip()
        #Get number of guesses
        self.guesses += 1
        self.guess_label.configure(text=f"Guesses: {self.guesses}/{self.max_guesses}")
        
        if not user_input:
            return
        
        user_input_lower = user_input.lower()
        correct_lower = {name.lower() for name in self.correct_answers}

        if user_input_lower in correct_lower and user_input_lower not in {name.lower() for name in self.user_answers}:
            self.user_answers.add(user_input)
            self.feedback_label.config(text="Correct!", fg="green")
        else:
            self.feedback_label.config(text="Incorrect or already entered.", fg="red")

        # Update correct answers display
        self.correct_label.config(text=f"Correct answers: {', '.join(self.user_answers)}")

        # Clear entry field
        self.answer_entry.delete(0, tk.END)

        # Check if the user has provided enough correct answers
        if len(self.user_answers) >= self.max_guesses:
            self.feedback_label.config(text=f"You got all {self.max_guesses} correct! Moving to next question...", fg="blue")
            self.master.after(2000, self.next_question)
        if self.guesses >= self.max_guesses:
            self.feedback_label.config(text="Out of guesses! Moving to next question...", fg="blue")
            self.master.after(2000, self.next_question)
