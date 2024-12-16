import os
import random
import yaml
from prettytable import PrettyTable

DATA_FOLDER = 'data/'

class Styling:
    GREEN = '\033[92m'
    YELLOW = '\033[33m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    ENDBOLD = '\033[0m'

class CLIHandler:
    @staticmethod
    def display_message(message, color='', bold=False):
        print(f'{color}{Styling.BOLD if bold else ""}{message}{Styling.ENDBOLD if bold else ""}{Styling.ENDC}')
    
    @staticmethod
    def display_topics(topics):
        CLIHandler.display_message('-- SYMFONY CERTIFICATE PRACTICE --\n', Styling.GREEN, True)
        for i, topic in enumerate(topics):
            CLIHandler.display_message(f'{i + 1}. {topic.name}')

    @staticmethod
    def display_question(question, question_number):
        CLIHandler.display_message(f'\n{Styling.YELLOW}Question #{question_number}{Styling.ENDC} {Styling.BOLD}{question}{Styling.ENDBOLD}', bold=True)

    @staticmethod
    def display_table(field_names, rows, align='l'):
        table = PrettyTable()
        table.align = align
        table.field_names = [f'{Styling.BOLD}{Styling.GREEN}{field}{Styling.ENDC}{Styling.ENDBOLD}' for field in field_names]
        for row in rows:
            table.add_row(row)
        print('\n', table)

    @staticmethod
    def input_message(message):
        return input(f'{Styling.BOLD}{message}: {Styling.ENDBOLD} ')

    @staticmethod
    def clear_screen():
        os.system('clear')

class Topic:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.questions = []

    def load_topic(self, amount_of_questions):
        while len(self.questions) < amount_of_questions:
            question = self.__load_random_question()
            if question not in self.questions:
                self.questions.append(question)

    def show_questions(self):
        for i, question in enumerate(self.questions):
            question.show_question(i + 1)
            try:
                answers = input('> ').split(',')
                question.select_answers(answers)
            except (ValueError, IndexError):
                CLIHandler.display_message('Invalid input. Skipping...', Styling.RED)

    def show_results(self):
        rows = []
        for i, question in enumerate(self.questions):
            question_str = question.question[:75] + (question.question[:75] and '..')
            correct_answers = question.correct_answers()
            your_answers = question.selected_answers()
            result = '✅' if set(correct_answers) == set(your_answers) else '❌'
            rows.append([
                f'{Styling.YELLOW}#{i + 1}{Styling.ENDC} {question_str}',
                ', '.join([answer.value[:35] + (answer.value[:35] and '..') for answer in correct_answers]),
                result
            ])

        correct_count = self.__correct_answers_count()
        CLIHandler.display_table(
            field_names=['Question', 'Correct Answer', 'Result'],
            rows=rows
        )
        CLIHandler.display_message(
            f'{Styling.BOLD}Score:{Styling.ENDBOLD} {Styling.RED}Wrong: {len(self.questions) - correct_count}{Styling.ENDC} - '
            f'{Styling.GREEN}Correct: {correct_count}{Styling.ENDC}'
        )

    def __correct_answers_count(self):
        return sum(
            set(question.selected_answers()) == set(question.correct_answers())
            for question in self.questions
        )

    def __load_random_question(self):
        question_file = random.choice([f for f in os.listdir(self.path) if f.endswith('.yaml')])
        with open(self.path + '/' + question_file) as file:
            questions = yaml.safe_load(file)['questions']
            random_question = random.choice(questions)
            question = Question(random_question['uuid'], random_question['question'])
            for answer in random_question['answers']:
                question.add_answer(Answer(answer['value'], answer['correct']))
            
            return question
    
    @staticmethod
    def list_topics():
        return [Topic(topic.lower(), os.path.join(DATA_FOLDER, topic)) for topic in os.listdir(DATA_FOLDER)]

class Question:
    def __init__(self, uuid, question):
        self.uuid = uuid
        self.question = question.replace('\n', ' ').replace('\r', ' ')
        self.answers = []

    def __eq__(self, other):
        if isinstance(other, Question):
            return self.uuid == other.uuid
        return False

    def add_answer(self, answer):
        self.answers.append(answer)

    def show_question(self, question_number):
        CLIHandler.display_question(self.question, question_number)
        for i, answer in enumerate(self.answers):
            CLIHandler.display_message(f'\t[{Styling.GREEN}{i + 1}{Styling.ENDC}] {answer.value}')
    
    def select_answers(self, answers):
        answers = [int(answer) - 1 for answer in answers]
        for answer in answers:
            if 0 <= answer < len(self.answers):
                self.answers[answer].select()
                CLIHandler.display_message(f'{Styling.YELLOW}Your answer: {Styling.ENDC}{self.answers[answer].value}')
            else:
                raise IndexError('Invalid answer selected')

    def selected_answers(self):
        return [answer for answer in self.answers if answer.selected]

    def correct_answers(self):
        return [answer for answer in self.answers if answer.correct]


class Answer:
    def __init__(self, value, correct):
        self.value = value
        self.correct = correct
        self.selected = False

    def select(self):
        self.selected = True

def main():
    topics = Topic.list_topics()
    CLIHandler.display_topics(topics)

    try:
        selected_topic = int(CLIHandler.input_message('\nSelect topic')) - 1
        amount_of_questions = int(CLIHandler.input_message('Amount of questions'))
    except ValueError:
        CLIHandler.display_message('Invalid input. Exiting...', Styling.RED)
        return
    
    if not (0 <= selected_topic < len(topics)):
        CLIHandler.display_message('Invalid input. Exiting...', Styling.RED)
        return

    CLIHandler.clear_screen()
    topic = topics[selected_topic]
    topic.load_topic(amount_of_questions)
    topic.show_questions()
    topic.show_results()

if __name__ == '__main__':
    main()
