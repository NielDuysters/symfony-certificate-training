import random
import os
import yaml
from dataclasses import dataclass, field
from cli_handler import display_message, display_question, input_message, display_table
from styling import red, yellow, green

@dataclass
class Answer:
    """Represents a possible answer for a question and save state if answer is selected by user."""
    value: str
    correct: bool
    selected: bool = False

    def __hash__(self) -> int:
        return hash(self.value)

@dataclass
class Question:
    """Represents a question with its possible answers."""
    uuid: str
    question: str
    answers: list[Answer] = field(default_factory=list)

    def __eq__(self, other) -> bool:
        return isinstance(other, Question) and self.uuid == other.uuid

    def show_question(self, question_number: int) -> None:
        display_question(self.question, question_number)
        for i, answer in enumerate(self.answers):
            display_message(f'\t[{yellow(i + 1)}] {answer.value}')

    def correct_answers(self) -> list[Answer]:
        """Return a list of correct answers for this question."""
        return [answer for answer in self.answers if answer.correct]

    def selected_answers(self) -> list[Answer]:
        """Return a list of by user selected inputted answers for this question."""
        return [answer for answer in self.answers if answer.selected]

    def select_answers(self, answers: list[int]) -> None:
        """Update state of answers to selected."""
        answers = [int(answer) - 1 for answer in answers]
        for answer in answers:
            if 0 <= answer < len(self.answers):
                self.answers[answer].selected = True
                display_message(f'{yellow("Your answer:")} {self.answers[answer].value}')
            else:
                raise IndexError('Invalid answer selected.')

@dataclass
class Topic:
    """Represents a topic with its questions."""
    name: str
    path: str
    questions: list[Question] = field(default_factory=list)

    def load_topic(self, amount_of_questions: int) -> None:
        """Load amount of requested questions into the topic."""
        while len(self.questions) < amount_of_questions:
            question = self._load_random_question()
            if question not in self.questions:
                self.questions.append(question)
    
    def show_questions(self) -> None:
        """Show all questions of the topic and let user select answers."""
        for i, question in enumerate(self.questions):
            question.show_question(i + 1)
            try:
                answers = input('> ').split(',')
                question.select_answers(answers)
            except (ValueError, IndexError):
                display_message(red('Invalid input. Skipping...'))
    
    def show_results(self) -> None:
        rows = []
        for i, question in enumerate(self.questions):
            question_str = question.question[:75] + (question.question[75:] and '..')
            correct_answers = question.correct_answers()
            your_answers = question.selected_answers()
            result = '✅' if set(correct_answers) == set(your_answers) else '❌'
            rows.append([
                f'{yellow(f"#{i + 1}")} {question_str}',
                ', '.join([ans.value[:35] + (ans.value[:35] and '..') for ans in correct_answers]),
                result
            ])

        correct_count = self._correct_answers_count()
        display_table(['Question', 'Correct Answer', 'Result'], rows)
        display_message(
            f'{green("Correct: " + str(correct_count))} - '
            f'{red("Wrong: " + str(len(self.questions) - correct_count))}', bold=True
        )

    def _correct_answers_count(self) -> int:
        return sum(
            set(question.selected_answers()) == set(question.correct_answers())
            for question in self.questions
        )

    def _load_random_question(self) -> Question:
        """Load a random question from the topic's YAML file."""
        question_file = random.choice([f for f in os.listdir(self.path) if f.endswith('.yaml')])
        with open(self.path + '/' + question_file) as file:
            questions = yaml.safe_load(file)['questions']
            random_question = random.choice(questions)
            question = Question(uuid=random_question['uuid'], question=random_question['question'])
            for answer in random_question['answers']:
                question.answers.append(Answer(value=answer['value'], correct=answer['correct']))
            
            return question

    @staticmethod
    def list_topics(data_folder: str) -> list:
        """List all available topics."""
        return [Topic(name=topic.lower(), path=os.path.join(data_folder, topic)) for topic in os.listdir(data_folder)]

