#!/usr/bin/env python3
"""
Country Quiz Game

A console-based quiz game about countries in the Americas.
"""

import json
import random
import os
import datetime
from typing import List, Dict, Any, Tuple

# Constants
DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "source", "countries.json")
QUESTIONS = [
    ("capital", "What is the capital of {country}?"),
    ("currency", "What is the currency of {country}?"),
    ("language", "What is the language of {country}?"),
    ("subregion", "In which subregion is {country} located?")
]

class CountryQuiz:
    def __init__(self, data_file: str):
        """Initialize the quiz with country data."""
        self.countries = self._load_data(data_file)
        self.score = 0
        self.total_questions = 4  # Questions per round

    @staticmethod
    def _load_data(file_path: str) -> List[Dict[str, str]]:
        """Load country data from JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Could not find data file at {file_path}")
            return []
        except json.JSONDecodeError:
            print("Error: Invalid JSON data in the file")
            return []

    def get_random_country(self) -> Dict[str, str]:
        """Get a random country from the loaded data."""
        return random.choice(self.countries) if self.countries else {}

    def get_random_choices(self, correct_answer: str, field: str, count: int = 4) -> List[str]:
        """Generate a list of choices including the correct answer."""
        # Get all possible unique values for the field
        all_values = list({c[field] for c in self.countries if c[field]})
        
        # Remove the correct answer to avoid duplicates
        if correct_answer in all_values:
            all_values.remove(correct_answer)
        
        # Select random wrong answers
        wrong_answers = random.sample(all_values, min(count - 1, len(all_values)))
        
        # Combine and shuffle
        choices = [correct_answer] + wrong_answers
        random.shuffle(choices)
        return choices

    def ask_question(self, country: Dict[str, str], field: str, question_text: str) -> bool:
        """Ask a question and return True if the answer was correct."""
        correct_answer = country.get(field, "")
        if not correct_answer:
            return False

        # Get choices and find the correct index
        choices = self.get_random_choices(correct_answer, field)
        correct_index = choices.index(correct_answer) + 1  # 1-based index for user

        # Ask the question
        print(f"\n{question_text.format(country=country['name'])}")
        for i, choice in enumerate(choices, 1):
            print(f"{i}. {choice}")
        
        # Get and validate user input
        while True:
            try:
                user_choice = int(input("\nYour answer (1-4): "))
                if 1 <= user_choice <= 4:
                    break
                print("Please enter a number between 1 and 4.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Check answer
        if user_choice == correct_index:
            print("✅ Correct!")
            return True
        else:
            print(f"❌ Incorrect! The correct answer is: {correct_answer}")
            return False

    def play_round(self) -> None:
        """Play one round of the quiz (4 questions about one country)."""
        country = self.get_random_country()
        if not country:
            print("No country data available. Exiting...")
            return

        print(f"\n{'='*50}")
        print(f"Let's learn about {country['name']}!")
        print(f"{'='*50}")

        # Ask all questions for this country
        round_score = 0
        for field, question in QUESTIONS:
            if field in country and country[field]:  # Only ask if the field exists and is not empty
                if self.ask_question(country, field, question):
                    round_score += 1
        
        # Update total score
        self.score += round_score
        print(f"\nRound complete! You got {round_score} out of {self.total_questions} correct.")

    def save_results(self, score: int) -> None:
        """Save game results to a file with timestamp."""
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output")
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(output_dir, "result.txt")
        
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(f"{datetime.datetime.now()}: Score = {score} points\n")
        
        print(f"\n📊 Results saved to {filename}")

    def run(self) -> None:
        """Run the quiz game."""
        if not self.countries:
            print("No country data available. Exiting...")
            return

        print("\n🌎 Welcome to the Country Quiz Game! 🌎")
        print("You'll be asked questions about countries in the Americas.")
        print("For each question, choose the correct answer from the options provided.\n")
        
        while True:
            self.play_round()
            
            # Ask to play again
            play_again = input("\nWould you like to play another round? (y/n): ").strip().lower()
            if play_again != 'y':
                break
        
        print(f"\n🎉 Game Over! Your total score is {self.score} points. 🎉")
        self.save_results(self.score)


def main():
    """Main function to run the quiz game."""
    quiz = CountryQuiz(DATA_FILE)
    quiz.run()


if __name__ == "__main__":
    main()
