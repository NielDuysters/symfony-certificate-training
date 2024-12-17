from prettytable import PrettyTable
from styling import bold as setBold, green, yellow, red, CLS

def display_message(message: str, color=lambda x: x, bold: bool = False) -> None:
    """Print a styled message"""
    style = setBold if bold else lambda x: x
    print(style(color(message)))

def display_topics(topics: list) -> None:
    """Print a list of topics"""
    display_message('-- SYMFONY CERTIFICATE PRACTICE --', color=green, bold=True)
    for i, topic in enumerate(topics):
        display_message(f'{i + 1}. {topic.name}')

def display_question(question: str, question_number: int) -> None:
    """Print a question"""
    display_message(f'\n{yellow(f"Question #{question_number}")} {question}', bold=True)

def display_table(field_names: list, rows: list, align: str = 'l') -> None:
    """Print a table"""
    table = PrettyTable()
    table.align = align
    table.field_names = [setBold(green(field)) for field in field_names]
    for row in rows:
        table.add_row(row)
    print('\n', table)

def input_message(message: str) -> str:
    """Get user input"""
    return input(setBold(f'{message}: '))

def clear_screen() -> None:
    print(CLS, end='')

