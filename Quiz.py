import random
import time
import threading
import os
import tkinter as tk
from tkinter import messagebox

# Sample Questions and Answers
quiz_data = [
    {
        "question": "What is the largest country in the world?",
        "options": ["1. USA", "2. China", "3. Russia", "4. Canada"],
        "answer": 3
    },
    {
        "question": "What is the capital of Canada?",
        "options": ["1. Toronto", "2. Ottawa", "3. Montreal", "4. Vancouver"],
        "answer": 2
    },
    {
        "question": "Which river is the longest in the world?",
        "options": ["1. Amazon", "2. Nile", "3. Yangtze", "4. Mississippi"],
        "answer": 2
    },
    # Add more questions here based on the provided list...
]


# Timer function
def timeout_input(prompt, timeout):
    """Function to handle input with a timeout."""

    def timeout_handler():
        print(f"\nTime's up! Moving to the next question.")

    timer = threading.Timer(timeout, timeout_handler)
    timer.start()
    try:
        answer = input(prompt)
    except Exception:
        answer = None
    timer.cancel()
    return answer


# Function to run the quiz with a timer for each question
def run_quiz_with_timer(quiz_data, time_limit=10):
    random.shuffle(quiz_data)  # Shuffle questions for each game session
    score = 0
    for question in quiz_data:
        print(question["question"])
        for option in question["options"]:
            print(option)

        # Call the timeout_input with a time limit
        answer = timeout_input(f"Choose the correct option (1-4) in {time_limit} seconds: ", time_limit)

        if answer is None:
            print("No answer given. Moving to the next question...\n")
            continue

        try:
            answer = int(answer)
        except ValueError:
            print("Invalid input. Please enter a number between 1-4.\n")
            continue

        if answer == question["answer"]:
            print("Correct!\n")
            score += 1
        else:
            print(f"Wrong! The correct answer was option {question['answer']}.\n")

    return score


# High Score Functions
def get_high_score():
    """Function to read the high score from a file."""
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as file:
            high_score = int(file.read())
    else:
        high_score = 0
    return high_score


def save_high_score(score):
    """Function to save the high score to a file."""
    high_score = get_high_score()
    if score > high_score:
        with open("highscore.txt", "w") as file:
            file.write(str(score))
        print("New high score!\n")
    else:
        print(f"The current high score is: {high_score}\n")


# Main function to start the quiz with a timer and high score tracking
def main_with_high_score():
    high_score = get_high_score()
    print(f"The current high score is: {high_score}")
    final_score = run_quiz_with_timer(quiz_data)
    print(f"Your final score is: {final_score}/{len(quiz_data)}")
    print(f"You scored {(final_score / len(quiz_data)) * 100:.2f}%")

    save_high_score(final_score)


# GUI Implementation Using tkinter (Optional)
class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Python Quiz")

        self.current_question = 0
        self.score = 0
        self.quiz_data = quiz_data  # Accessing the global quiz data
        random.shuffle(self.quiz_data)

        self.question_label = tk.Label(root, text=self.quiz_data[self.current_question]["question"], font=("Arial", 14))
        self.question_label.pack(pady=20)

        self.var = tk.IntVar()

        self.options = []
        for i in range(4):
            rb = tk.Radiobutton(root, text="", variable=self.var, value=i + 1, font=("Arial", 12))
            rb.pack(anchor="w")
            self.options.append(rb)

        self.submit_button = tk.Button(root, text="Submit", command=self.submit_answer)
        self.submit_button.pack(pady=20)

        self.update_question()

    def update_question(self):
        """Update question and options in the GUI."""
        self.var.set(0)
        self.question_label.config(text=self.quiz_data[self.current_question]["question"])
        for i, option in enumerate(self.quiz_data[self.current_question]["options"]):
            self.options[i].config(text=option)

    def submit_answer(self):
        """Submit the selected answer in the GUI."""
        selected_answer = self.var.get()
        correct_answer = self.quiz_data[self.current_question]["answer"]

        if selected_answer == correct_answer:
            self.score += 1
            messagebox.showinfo("Correct", "That's the correct answer!")
        else:
            messagebox.showinfo("Incorrect", f"Wrong! The correct answer was option {correct_answer}.")

        self.current_question += 1
        if self.current_question >= len(self.quiz_data):
            self.end_quiz()
        else:
            self.update_question()

    def end_quiz(self):
        """End the quiz and display the final score."""
        messagebox.showinfo("Quiz Completed", f"Your final score is {self.score}/{len(self.quiz_data)}")
        self.root.quit()


def run_gui_quiz():
    """Function to run the quiz using the tkinter GUI."""
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()


# Entry point for the command-line version with a timer and high score tracking
if __name__ == "__main__":
    mode = input("Choose mode: (1) Text-based Quiz (2) GUI Quiz: ")

    if mode == "1":
        main_with_high_score()  # Text-based quiz with timer and high score
    elif mode == "2":
        run_gui_quiz()  # GUI version using tkinter
    else:
        print("Invalid choice. Exiting.")
