from models import Topic
from cli_handler import display_topics, input_message, clear_screen, display_message
from styling import red

DATA_FOLDER = 'data/'

def main():
    topics = Topic.list_topics(DATA_FOLDER)
    display_topics(topics)

    try:
        selected_topic = int(input_message('\nSelect topic')) - 1
        amount_of_questions = int(input_message('Amount of questions'))
    except ValueError:
        display_message('Invalid input. Exiting...', red)
        return
    
    if not (0 <= selected_topic < len(topics)):
        display_message('Invalid input. Exiting...', red)
        return

    clear_screen()
    topic = topics[selected_topic]
    topic.load_topic(amount_of_questions)
    topic.show_questions()
    topic.show_results()

if __name__ == '__main__':
    main()

