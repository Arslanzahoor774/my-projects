import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.chat.util import Chat, reflections
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

nltk.download('vader_lexicon')
nltk.download('punkt')

sid = SentimentIntensityAnalyzer()


basic_patterns = [
    (r'hi|hello|hey', ['Hello!', 'Hi there!', 'Hey!']),
    (r'how are you?', ['I am good, thank you!', 'I\'m doing well, how about you?', 'Feeling pretty good, thanks for asking.', 'All good here, how about you?']),
    (r'what\'s your name?', ['I am a chatbot.', 'You can call me Chatbot.', 'I go by Chatbot.', 'My name is Chatbot.']),
    (r'bye|goodbye', ['Goodbye!', 'See you later!', 'Bye!', 'Take care!', 'Until next time!', 'Farewell!', 'Bye-bye!']),
    (r'how\'s the weather\?', ['It\'s sunny today!', 'Looks like rain later.', 'Perfect weather for a walk!', 'A bit chilly, but nothing a jacket can\'t fix.', 'Sunny with a chance of clouds.', 'It\'s foggy outside.']),
    (r'what are you doing\?', ['Just chatting with you!', 'Answering your questions.', 'Nothing much, just being a chatbot.']),
    (r'what\'s up\?', ['Not much, just here to chat!', 'Just hanging out, what about you?', 'Just chilling, what\'s up with you?']),
    (r'how was your day\?', ['Pretty good, thanks for asking!', 'It was alright, nothing too exciting.', 'Fantastic, thanks for asking!', 'Could\'ve been better, but overall not bad.', 'Long and tiring, but I\'m here now!']),
    (r'are you human\?', ['I\'m not human, but I try my best to chat like one!', 'Nope, I\'m a chatbot designed to assist you.']),
]

mood_patterns = {
    'happiness': [r'happy|joy|cheerful|delighted', [
        'That\'s wonderful to hear!', 
        'I\'m glad you\'re feeling happy!', 
        'Happiness is contagious!',
    ]],
    'sadness': [r'sad|unhappy|depressed', [
        'I\'m sorry to hear that.',
        'It\'s okay to feel sad sometimes.',
    ]],
    'anger': [r'angry|mad|frustrated', [
        'Take a deep breath and count to ten.',
        'I understand why you\'re feeling angry.',
    ]],
    'fear': [r'fear|scared|anxious', [
        'It\'s okay to feel scared sometimes.',
        'You\'re not alone, I\'m here to help.',
    ]],
    'surprise': [r'surprised|shocked|astonished', [
        'Wow, that\'s unexpected!',
        'Surprises can be exciting!',
    ]],
    'disgust': [r'disgust|disgusted|repulsed', [
        'I understand why you\'re feeling disgusted.',
        'That sounds unpleasant.',
    ]]
}

mood_patterns_list = [(mood_pattern, responses) for mood, (mood_pattern, responses) in mood_patterns.items()]


all_patterns = basic_patterns + mood_patterns_list


chatbot = Chat(all_patterns, reflections)


def start_chat():
    print("Hello! I am a chatbot. How can I assist you today?")
    while True:
        user_input = input("User: ")
        if user_input is not None:
            print("sid",sid.polarity_scores(user_input))
        response = chatbot.respond(user_input)
        print("Chatbot:", response)
        
        if user_input.lower() == 'bye':
            break


start_chat()
