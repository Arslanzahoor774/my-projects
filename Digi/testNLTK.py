# import nltk
# from nltk.sentiment import SentimentIntensityAnalyzer
# from nltk.chat.util import Chat, reflections
# import ssl
# import cv2
# import os
# import re
# import random
# from deepface import DeepFace
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.naive_bayes import MultinomialNB

# # Download necessary NLTK data
# nltk.download('vader_lexicon')
# nltk.download('punkt')
# nltk.download('stopwords')

# # Initialize Sentiment Intensity Analyzer
# sid = SentimentIntensityAnalyzer()

# # Define stopwords
# stop_words = set(stopwords.words('english'))

# # Define basic patterns
# basic_patterns = [
#     (r'hi|hello|hey', ['Hello!', 'Hi there!', 'Hey!']),
#     (r'how are you?', ['I am good, thank you!', 'I\'m doing well, how about you?', 'Feeling pretty good, thanks for asking.', 'All good here, how about you?']),
#     (r'what\'s your name|what is your name', ['I am a chatbot.', 'You can call me Chatbot.', 'I go by Chatbot.', 'My name is Chatbot.']),
#     (r'bye|goodbye', ['Goodbye!', 'See you later!', 'Bye!', 'Take care!', 'Until next time!', 'Farewell!', 'Bye-bye!']),
#     (r'how\'s the weather|how is the weather', ['It\'s sunny today!', 'Looks like rain later.', 'Perfect weather for a walk!', 'A bit chilly, but nothing a jacket can\'t fix.', 'Sunny with a chance of clouds.', 'It\'s foggy outside.']),
#     (r'what are you doing', ['Just chatting with you!', 'Answering your questions.', 'Nothing much, just being a chatbot.']),
#     (r'what\'s up|what is up', ['Not much, just here to chat!', 'Just hanging out, what about you?', 'Just chilling, what\'s up with you?']),
#     (r'how was your day', ['Pretty good, thanks for asking!', 'It was alright, nothing too exciting.', 'Fantastic, thanks for asking!', 'Could\'ve been better, but overall not bad.', 'Long and tiring, but I\'m here now!']),
#     (r'are you human', ['I\'m not human, but I try my best to chat like one!', 'Nope, I\'m a chatbot designed to assist you.']),
#     (r'that\'s interesting|interesting', ['That\'s Fascinating!', 'I\'m intrigued!']),
#     (r'I get what you mean|get what you mean', ['I totally get what you mean!', 'Exactly!', 'I understand!']),
#     (r'oh, I know|know exactly', ['Oh, I know exactly what you\'re talking about!', 'Absolutely!', 'I\'ve been there!']),
#     (r'haha|that\'s hilarious', ['Haha, that\'s hilarious!', 'You crack me up!', 'Too funny!']),
#     (r'wow|didn\'t know', ['Wow, I didn\'t know that!', 'That\'s news to me!', 'Interesting fact!']),
#     (r'you\'re so right|you\'re right', ['You\'re so right!', 'Spot on!', 'Exactly!']),
#     (r'I agree|agree completely', ['I agree completely!', 'Couldn\'t have said it better myself!', 'Absolutely!']),
#     (r'I feel the same way|feel the same', ['I feel the same way!', 'Me too!', 'Exactly how I\'m feeling!']),
#     (r'exactly', ['Exactly!', 'Spot on!', 'That\'s the one!']),
#     (r'I\'ve been there|been there before', ['Oh, I\'ve been there before!', 'I know the feeling!', 'Been there, done that!']),
#     (r'sounds like a plan|like a plan', ['Sounds like a plan!', 'Count me in!', 'Let\'s do it!']),
#     (r'I\'m here for you|here for you', ['I\'m here for you!', 'You can count on me!', 'Always here to chat!']),
#     (r'you\'re the best|the best', ['You\'re the best!', 'You\'re awesome!', 'You rock!']),
#     (r'thanks for sharing|for sharing', ['Thanks for sharing!', 'Appreciate you opening up!', 'Sharing is caring!']),
#     (r'I appreciate your perspective|appreciate your perspective', ['I appreciate your perspective!', 'Thanks for sharing your viewpoint!', 'Your insights are valuable!']),
#     (r'I\'m glad we\'re chatting|glad we\'re chatting', ['I\'m glad we\'re chatting!', 'Me too!', 'Love our conversations!']),
#     (r'always full of surprises|full of surprises', ['You\'re always full of surprises!', 'You never cease to amaze me!', 'You keep me on my toes!']),
#     (r'you never fail to make me smile|make me smile', ['You never fail to make me smile!', 'You brighten my day!', 'Your smile is contagious!']),
#     (r'keep the conversation flowing|conversation flowing', ['Keep the conversation flowing!', 'Let\'s keep talking!', 'I love our chats!']),
#     (r'I love chatting with you|love chatting with you', ['I love chatting with you!', 'You\'re one of my favorite people to talk to!', 'I always enjoy our conversations!']),
#     (r'let\'s keep this conversation going|conversation going', ['Let\'s keep this conversation going!', 'I\'m enjoying this chat too much to stop!', 'Don\'t want this conversation to end!']),
#     (r'making my day|make my day', ['You\'re making my day!', 'Thanks for bringing a smile to my face!', 'You\'ve made my day brighter!']),
#     (r'great conversationalist|conversationalist', ['You\'re a great conversationalist!', 'I enjoy our chats so much!', 'Love talking to you!']),
#     (r'keep the conversation going|conversation going', ['Keep the conversation going!', 'I\'m enjoying this chat too much to stop!', 'Don\'t want this conversation to end!']),
#     (r'always know what to say|know what to say', ['You always know what to say!', 'Your words always resonate with me!', 'You have a way with words!']),
#     (r'thanks for being so awesome|being so awesome', ['Thanks for being so awesome!', 'You\'re awesome!', 'You rock!']),
#     (r'lucky to have you|have you as a chat partner', ['I\'m lucky to have you as a chat partner!', 'I appreciate our chats!', 'Chatting with you is the best part of my day!']),
#     (r'smiling from ear to ear|from ear to ear', ['I\'m smiling from ear to ear!', 'You always bring a smile to my face!', 'You\'re the reason behind my smile!']),
#     (r'words brighten my day|brighten my day', ['Your words brighten my day!', 'You always know how to make me feel better!', 'Thanks for brightening my day!']),
#     (r'ray of sunshine|a ray of sunshine', ['You\'re a ray of sunshine!', 'You bring light into my life!', 'Thanks for being my sunshine!']),
#     (r'appreciate your positivity|your positivity', ['I appreciate your positivity!', 'Thanks for spreading positivity!', 'Your positive energy is contagious!']),
#     (r'breath of fresh air|fresh air', ['You\'re like a breath of fresh air!', 'Your perspective is refreshing!', 'Thanks for being a breath of fresh air!']),
#     (r'grateful for our conversations|our conversations', ['I\'m grateful for our conversations!', 'I love our chats!', 'You\'re the best chat partner!']),
#     (r'way with words|with words', ['You have a way with words!', 'Your words always resonate with me!', 'I admire your eloquence!']),
#     (r'inspired by your words|by your words', ['I\'m inspired by your words!', 'You always motivate me!', 'Thanks for inspiring me!']),
#     (r'bringing so much joy|so much joy', ['Thanks for bringing so much joy to our conversation!', 'You always bring joy into my life!', 'Your happiness is contagious!']),
#     (r'love the vibe|the vibe you bring', ['I love the vibe you bring to our chats!', 'Your energy is infectious!', 'Thanks for bringing such a positive vibe!']),
#     (r'perspective always adds depth|adds depth to our discussions', ['Your perspective always adds depth to our discussions!', 'You always provide insightful perspectives!', 'Thanks for adding depth to our conversations!']),
#     (r'true conversationalist|conversationalist', ['You\'re a true conversationalist!', 'I love talking to you!', 'You\'re an amazing chat partner!']),
#     (r'grateful for your friendship|your friendship', ['I\'m grateful for your friendship!', 'You\'re an amazing friend!', 'Thanks for being there for me!']),
#     (r'ok|done|yes', ['sure', 'yup', 'fine']),
# ]
# # Define mood patterns
# mood_patterns = [
#     (r'happy|joy|cheerful|delighted|happiness', [
#         'That\'s wonderful to hear!', 
#         'I\'m glad you\'re feeling happy!', 
#         'Happiness is contagious!',
#         'Your happiness brings a smile to my face!',
#         'It\'s fantastic to see you in such high spirits!',
#         'You radiate positivity, and it\'s contagious!',
#         'May your happiness continue to brighten your day!',
#         'Embrace the joy you feel, and let it spread to those around you!',
#         'There\'s nothing better than basking in the glow of happiness!',
#         'Your cheerful demeanor is a ray of sunshine on even the gloomiest days!',
#         'I hope this happiness stays with you for a long time!',
#         'Life is so much better when we choose to focus on the things that make us happy!',
#         'The world becomes a brighter place when you\'re filled with joy!'
#     ]),
#     (r'sad|unhappy|depressed|sadness', [
#        'I\'m sorry to hear that.',
#         'It\'s okay to feel sad sometimes.',
#         'I understand how you feel.',
#         'Would you like to talk about it?',
#         'Sending you virtual hugs!',
#         'Things will get better, I promise.',
#         'Remember, it\'s okay not to be okay.',
#         'I\'m here for you if you need support.',
#         'You\'re not alone in feeling this way.',
#         'Take your time to process your emotions.'
#     ]),
#     (r'angry|mad|frustrated|anger', [
#         'Take a moment to cool off before reacting.',
#         'It\'s okay to feel angry, but let\'s try to address the issue calmly.',
#         'Expressing your feelings is important. What\'s bothering you?',
#         'Anger is a natural emotion, but it\'s important to manage it constructively.',
#         'Try to focus on finding a solution rather than dwelling on the problem.',
#         'Deep breaths can help you calm down. Inhale deeply, then exhale slowly.',
#         'Is there something specific that\'s causing your anger?',
#         'Remember, you have the power to control your reactions.',
#         'Don\'t let anger consume you. Let\'s work through this together.',
#         'Taking a break and stepping away from the situation can give you perspective.'
#     ]),
#     (r'fear|scared|anxious|fear', [
#         'It\'s okay to feel scared sometimes.',
#         'You\'re not alone, I\'m here to help.',
#         'Fear is a natural emotion, and it\'s okay to acknowledge it.',
#         'Remember, it\'s normal to feel scared when facing the unknown.',
#         'You\'re not alone in feeling anxious; many people experience the same emotions.',
#         'Take a deep breath and focus on things you can control.',
#         'Facing your fears can be empowering and lead to personal growth.',
#         'Just know that you have the strength to overcome whatever challenges come your way.',
#         'Sometimes, talking about your fears can help alleviate them. I\'m here to listen if you need someone to talk to.',
#         'You\'ve faced challenges before, and you can overcome this one too.',
#         'Remember that fear is just a temporary feeling; it doesn\'t define you or your future.',
#         'Take small steps to confront your fears, and soon you\'ll see that they aren\'t as daunting as they seem.'
#     ]),
#     (r'surprised|shocked|astonished|surprise', [
#         'Wow, that\'s unexpected!',
#         'Surprises can be exciting!',
#         'I didn\'t see that coming! What a surprise!',
#         'Well, that\'s a twist I didn\'t expect!',
#         'Surprises like that keep things interesting!',
#         'Your reaction says it all! What a pleasant surprise!',
#         'Isn\'t it amazing how life can still surprise us?',
#         'Unexpected moments like this make life so exciting!',
#         'Surprises often lead to the best stories!',
#         'You\'ve left me pleasantly surprised with that revelation!',
#         'It\'s moments like these that make life worth living!',
#         'Embrace the surprise and enjoy the moment!'
#     ]),
#     (r'disgust|disgusted|repulsed|disgust', [
#         'I can see why you\'re feeling disgusted.',
#         'That must be really unpleasant.',
#         'It sounds like a situation that would make anyone feel repulsed.',
#         'Feeling disgusted is a natural reaction to such things.',
#         'It\'s okay to be repulsed by certain things.',
#         'I empathize with your feelings of disgust.',
#         'That sounds absolutely repulsive.',
#         'It\'s normal to feel repulsed by certain experiences.',
#         'I\'m sorry you had to experience something so unpleasant.',
#         'Sometimes, things can be really disgusting.'
#     ])
# ]

# # Define personality patterns
# personality_patterns = [
#     (r'open-minded|curious|creative|Openness to Experience',[
#         'I admire your open-mindedness!', 'Curiosity is the key to growth.', 'Creativity is a wonderful trait.'
#         'Your open-mindedness is truly inspiring!',
#         'Being curious opens doors to new possibilities.',
#         'Creativity allows us to see the world in new and exciting ways.',
#         'Your openness to new experiences is refreshing!',
#         'Exploring new ideas is a fantastic way to expand your horizons.',
#         'Embracing creativity leads to endless opportunities.',
#         'I admire your willingness to explore new concepts.',
#         'Curiosity is the spark that ignites innovation.',
#         'Your creative spirit shines brightly!',
#         'Keep fostering your curiosity; it\'s the key to endless discoveries.'
#     ]),
#     (r'responsible|organized|disciplined|Conscientiousness',[
#         'Being responsible is admirable.', 'Organization leads to efficiency.', 'Discipline is essential for success.',
#         'Taking responsibility is a mark of maturity.',
#         'Your organized approach sets a great example.',
#         'Discipline is the bridge between goals and accomplishments.',
#         'Being responsible shows integrity and reliability.',
#         'Organizational skills are the cornerstone of productivity.',
#         'Discipline fuels progress and achievement.',
#         'Your commitment to being responsible is commendable.',
#         'Efficiency thrives in an organized environment.',
#         'Discipline is the key to turning dreams into reality.',
#         'Responsibility is the foundation of trust and respect.'
        
#     ]),
#     (r'social|outgoing|energetic|Extraversion',[
#         'You seem like a very social person!', 'Being outgoing can lead to exciting opportunities.', 'Your energy is infectious.',
#         'Your social skills are impressive!',
#         'Being outgoing opens doors to new connections.',
#         'Your vibrant energy lights up the room.',
#         'It\'s great to see your outgoing personality shine.',
#         'Socializing brings joy and fulfillment.',
#         'Your energetic spirit is inspiring.',
#         'You bring so much positivity to social interactions.',
#         'Being outgoing helps create memorable experiences.',
#         'Your enthusiasm for life is contagious.',
#         'Your outgoing nature makes gatherings more enjoyable.'
#     ]),
#     (r'kind|compassionate|cooperative|Agreeableness',[
#         'Kindness is a virtue.', 'Compassion makes the world a better place.', 'Cooperation leads to harmony.',
#          'Your kindness brightens the day of those around you.',
#         'Compassion towards others is a wonderful trait.',
#         'Your cooperative nature fosters teamwork and collaboration.',
#         'Being kind creates positive ripple effects in the world.',
#         'Compassion is the key to understanding and empathy.',
#         'Cooperation brings people together to achieve common goals.',
#         'Your kindness touches the hearts of many.',
#         'Compassion is a language that everyone understands.',
#         'Cooperation builds strong and supportive communities.',
#         'Your agreeable nature makes interactions pleasant and harmonious.'
#     ]),
#     (r'anxious|moody|worried|Neuroticism',[
#         'It\'s okay to feel anxious sometimes.', 'Moodiness is a part of being human.', 'Don\'t worry too much, things will be okay.',
#         'Remember to take deep breaths when feeling anxious.',
#         'Your mood may fluctuate, but it will pass.',
#         'Worrying too much can sometimes cloud our judgment.',
#         'It\'s important to address and manage anxiety for overall well-being.',
#         'Being moody is natural, but it\'s essential to find balance.',
#         'Find healthy outlets to express and cope with your mood swings.',
#         'When feeling worried, try focusing on the present moment.',
#         'Reach out to supportive friends or family when feeling anxious.',
#         'Practice self-care activities to alleviate moodiness and worry.',
#         'Take small steps to address your worries one at a time.'
#     ])
# ]
# # Combine all patterns
# all_patterns = basic_patterns + mood_patterns + personality_patterns
# chatbot = Chat(all_patterns, reflections)

# # Preprocess text data
# def preprocess_text(text):
#     # Tokenize the text
#     tokens = word_tokenize(text)
#     # Remove stopwords and punctuation
#     filtered_tokens = [token.lower() for token in tokens if token.lower() not in stop_words and token.isalnum()]
#     return ' '.join(filtered_tokens)

# # Train Naive Bayes classifier
# def train_classifier():
#     corpus = [preprocess_text(pattern[0]) for pattern in all_patterns]
#     labels = [pattern[1] for pattern in all_patterns]
#     vectorizer = CountVectorizer()
#     X = vectorizer.fit_transform(corpus)
#     clf = MultinomialNB()
#     clf.fit(X, labels)
#     return vectorizer, clf

# # Classify user input using Naive Bayes classifier
# def classify_input(user_input, vectorizer, clf):
#     preprocessed_input = preprocess_text(user_input)
#     input_vector = vectorizer.transform([preprocessed_input])
#     predicted_label = clf.predict(input_vector)[0]
#     return predicted_label

# # Modify the main function to use Naive Bayes classification
# def main():
#     print("Welcome to the Human Activity Chatbot!")
#     print("You can chat with me about anything, and I'll respond based on my personality, mood, style, and your human traits.\n")
    
#    # Train Naive Bayes classifier
# vectorizer, clf = train_classifier()



# def capture_image():
#     video = cv2.VideoCapture(0)
#     if not video.isOpened():
#         raise IOError("Cannot open webcam")

#     ret, frame = video.read()

#     if not ret:
#         raise RuntimeError("Failed to capture image")

#     filename = "captured_image.jpg"
#     cv2.imwrite(filename, frame)

#     video.release()
#     return filename


# while True:
#     user_input = input("User: ")
#     if user_input.lower() == 'bye':
#         print("Chatbot: Goodbye!")
#         break

#     predicted_label = classify_input(user_input, vectorizer, clf)
#     print("Predicted Label:", predicted_label)
    
#     if predicted_label == 'neutral':
#         # Proceed with your existing response generation logic
#         response = chatbot.respond(user_input)
#         if response is None:
#             print("Chatbot: Sorry, I didn't understand that. Can you please rephrase?")
#         else:
#             print("Chatbot:", response)
#     else:
#         # Use your existing logic for mood-based responses
#         try:
#             result = capture_image()
#             response = chatbot.respond(result)
#             if response is None:
#                 print("Chatbot:", result)
#             else:
#                 print("Chatbot:", response)                   
#         except Exception as e:
#             print("Error capturing image:",  e)

# if __name__ == "__main__":
#     main()




# import pandas as pd
# import nltk
# import cv2
# from nltk.sentiment import SentimentIntensityAnalyzer
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# from nltk.chat.util import Chat, reflections
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.naive_bayes import MultinomialNB

# # Download necessary NLTK data
# nltk.download('vader_lexicon')
# nltk.download('punkt')
# nltk.download('stopwords')

# # Initialize Sentiment Intensity Analyzer
# sid = SentimentIntensityAnalyzer()

# # Define stopwords
# stop_words = set(stopwords.words('english'))

# # Define basic patterns
# basic_patterns = [
#     (r'hi|hello|hey', ['Hello!', 'Hi there!', 'Hey!']),
#     (r'how are you?', ['I am good, thank you!', 'I\'m doing well, how about you?', 'Feeling pretty good, thanks for asking.', 'All good here, how about you?']),
#     # Other basic patterns...
# ]

# # Define mood patterns
# mood_patterns = [
#     # Mood patterns...
# ]

# # Define personality patterns
# personality_patterns = [
#     # Personality patterns...
# ]

# # Combine all patterns
# all_patterns = basic_patterns + mood_patterns + personality_patterns
# chatbot = Chat(all_patterns, reflections)

# # Preprocess text data
# def preprocess_text(text):
#     # Tokenize the text
#     tokens = word_tokenize(text)
#     # Remove stopwords and punctuation
#     filtered_tokens = [token.lower() for token in tokens if token.lower() not in stop_words and token.isalnum()]
#     return ' '.join(filtered_tokens)

# # Train Naive Bayes classifier from CSV file
# def train_classifier_from_csv(csv_file_path):
#     # Read the CSV file
#     data = pd.read_csv(csv_file_path)
    
#     # Extract pattern and response columns
#     corpus = data['Pattern'].apply(preprocess_text)
#     labels = data['Type']

#     vectorizer = CountVectorizer()
#     X = vectorizer.fit_transform(corpus)
#     clf = MultinomialNB()
#     clf.fit(X, labels)
#     return vectorizer, clf

# # Modify the main function to use Naive Bayes classification with CSV data
# def main():
#     print("Welcome to the Human Activity Chatbot!")
#     print("You can chat with me about anything, and I'll respond based on my personality, mood, style, and your human traits.\n")
    
#     # Specify the path to your CSV file
#     csv_file_path = r"D:\projects\nltkdata.csv"

#     # Train Naive Bayes classifier from CSV data
#     vectorizer, clf = train_classifier_from_csv(csv_file_path)

#     while True:
#         user_input = input("User: ")
#         if user_input.lower() == 'bye':
#             print("Chatbot: Goodbye!")
#             break

#         # Classify user input
#         preprocessed_input = preprocess_text(user_input)
#         input_vector = vectorizer.transform([preprocessed_input])
#         predicted_label = clf.predict(input_vector)[0]
        
#         if predicted_label == 'neutral':
#             # Proceed with basic pattern-based responses
#             response = chatbot.respond(user_input)
#             if response is None:
#                 print("Chatbot: Sorry, I didn't understand that. Can you please rephrase?")
#             else:
#                 print("Chatbot:", response)
#         else:
#             # Use mood-based or personality-based responses
#             # (You can implement this part based on your specific requirements)
#             print("Chatbot: This functionality is not implemented yet.")

# if __name__ == "__main__":
#     main()




import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

# Load the dataset
data = pd.read_csv('D:\projects\\nltkdata.csv')

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data['Pattern'], data['Response'], test_size=0.2, random_state=42)

# Vectorize the text data
vectorizer = CountVectorizer()
X_train_counts = vectorizer.fit_transform(X_train)
X_test_counts = vectorizer.transform(X_test)

# Train the Naive Bayes classifier
clf = MultinomialNB()
clf.fit(X_train_counts, y_train)

# Test the classifier
y_pred = clf.predict(X_test_counts)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
