import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from HEAD.mouth import speak

# import nltk
# nltk.download('stopwords')
# import nltk
# nltk.download('punkt')
# Load your Q&A dataset from a text file
# def load_dataset(file_path):
#     with open(file_path, 'r', encoding='utf-8') as file:
#         lines = file.readlines()
#         qna_pairs = [line.strip().split(':') for line in lines if ':' in line]
#         dataset = [{'question': q, 'answer': a} for q, a in qna_pairs]
#     return dataset
#


def load_dataset(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        qna_pairs = []

        # Process each line to extract question-answer pairs
        for line_number, line in enumerate(lines, start=1):
            line = line.strip()
            if not line:
                continue  # Skip empty lines
            if ':' not in line:
                print(f"Skipping invalid line {line_number}: '{line}' (No colon found)")
                continue  # Skip lines without a colon

            parts = line.split(":", 1)  # Split only at the first colon
            if len(parts) != 2:
                print(f"Skipping invalid line {line_number}: '{line}' (Invalid format after split)")
                continue  # Skip lines that cannot be split into exactly two parts

            q, a = parts
            qna_pairs.append({'question': q.strip(), 'answer': a.strip()})

        return qna_pairs


# Preprocess the text
def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    ps = PorterStemmer()
    tokens = word_tokenize(text.lower())
    tokens = [ps.stem(token) for token in tokens if token.isalnum() and token not in stop_words]
    return ' '.join(tokens)

# Train the TF-IDF vectorizer
def train_tfidf_vectorizer(dataset):
    corpus = [preprocess_text(qa['question']) for qa in dataset]
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(corpus)
    return vectorizer, X

# Retrieve the most relevant answer
def get_answer(question, vectorizer, X, dataset):
    question = preprocess_text(question)
    question_vec = vectorizer.transform([question])
    similarities = cosine_similarity(question_vec, X)
    best_match_index = similarities.argmax()
    return dataset[best_match_index]['answer']

# Main function
def mind(text):
    # Replace 'your_dataset.txt' with the path to your Q&A dataset
    dataset_path = r'C:\Users\nagat\OneDrive\Desktop\JARVIS\DATA\Brain_DATA\qna_data.txt'
    dataset = load_dataset(dataset_path)
    vectorizer, X = train_tfidf_vectorizer(dataset)
    user_question = text
    answer = get_answer(user_question, vectorizer, X, dataset)
    print(answer)
    speak(answer)


# # model.py
#
# import nltk
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
# from nltk.stem import PorterStemmer
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# from HEAD.mouth import speak
#
# # Download required NLTK datasets
# nltk.download('punkt')
# nltk.download('stopwords')
#
# # def load_dataset(file_path):
# #     with open(file_path, 'r', encoding='utf-8') as file:
# #         lines = file.readlines()
# #         qna_pairs = [line.strip().split(':') for line in lines if ':' in line]
# #         dataset = [{'question': q, 'answer': a} for q, a in qna_pairs]
# #     return dataset
#
#
# def load_dataset(file_path):
#     dataset = []
#     with open(file_path, 'r', encoding='utf-8') as file:
#         for line_number, line in enumerate(file, start=1):  # Add line numbers for debugging
#             line = line.strip()
#             if ':' not in line:
#                 print(f"Skipping invalid line {line_number}: '{line}' (No colon found)")
#                 continue  # Skip lines without a colon
#             parts = line.split(':', 1)  # Split only at the first colon
#             if len(parts) != 2:
#                 print(f"Skipping invalid line {line_number}: '{line}' (Improper format)")
#                 continue  # Skip invalid lines
#             q, a = parts
#             dataset.append({'question': q.strip(), 'answer': a.strip()})
#     return dataset
#
#
#
# def preprocess_text(text):
#     stop_words = set(stopwords.words('english'))
#     ps = PorterStemmer()
#     tokens = word_tokenize(text.lower())
#     tokens = [ps.stem(token) for token in tokens if token.isalnum() and token not in stop_words]
#     return ' '.join(tokens)
#
# def train_tfidf_vectorizer(dataset):
#     corpus = [preprocess_text(qa['question']) for qa in dataset]
#     vectorizer = TfidfVectorizer()
#     X = vectorizer.fit_transform(corpus)
#     return vectorizer, X
#
# def get_answer(question, vectorizer, X, dataset):
#     question = preprocess_text(question)
#     question_vec = vectorizer.transform([question])
#     similarities = cosine_similarity(question_vec, X)
#     best_match_index = similarities.argmax()
#     return dataset[best_match_index]['answer']
#
# def mind(text):
#     # Load the dataset from the file
#     dataset_path = r'C:\Users\nagat\OneDrive\Desktop\JARVIS\DATA\Brain_DATA\qna_data.txt'
#
#     dataset = load_dataset(dataset_path)
#
#     # Train the TF-IDF vectorizer
#     vectorizer, X = train_tfidf_vectorizer(dataset)
#
#     # Process the user question
#     user_question = text
#     answer = get_answer(user_question, vectorizer, X, dataset)
#
#     # Speak the answer and print it to the console
#     return answer
#
# mind("jarvis how are you")