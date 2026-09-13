import cv2
from deepface import DeepFace
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.chat.util import Chat, reflections
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

nltk.download('vader_lexicon')
nltk.download('punkt')

sid = SentimentIntensityAnalyzer()

# Load pre-trained cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Open webcam
video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not video.isOpened():
    raise IOError("Cannot open webcam")

# Define basic chat patterns
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

# Define mood patterns for personality detection
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

# Combine basic patterns and mood patterns into a single list
all_patterns = basic_patterns + [(mood_pattern, responses) for mood, (mood_pattern, responses) in mood_patterns.items()]

# Create chatbot
chatbot = Chat(all_patterns, reflections)

# Main chat function
def start_chat():
    print("Hello! I am a chatbot. How can I assist you today?")
    while True:
        user_input = input("User: ")
        if user_input is not None:
            print("Sentiment Analysis:", sid.polarity_scores(user_input))
        response = chatbot.respond(user_input)
        print("Chatbot:", response)
        
        if user_input.lower() == 'bye':
            break

# Start chat
start_chat()

# Face detection and emotion analysis loop
while video.isOpened():
    ret, frame = video.read()

    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (89, 2, 236), 1)
            face_img = frame[y:y + h, x:x + w].copy()

            try:
                analyze = DeepFace.analyze(face_img, actions=['emotion'])
                cv2.putText(frame, analyze['dominant_emotion'], (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (224, 77, 176), 2)
                print(analyze['dominant_emotion'])
            except:
                print('No face detected')

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release video capture and close all windows
video.release()
cv2.destroyAllWindows()
