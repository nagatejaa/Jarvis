# import sys
# import time
# import threading
# import webbrowser
# from wikipedia import wikipedia
# from HEAD.mouth import speak
# from Traning_Model.model import mind
#
#
# def load_qa_data(file_path):
#     qa_dict = {}
#     with open(file_path, 'r', encoding='utf-8', errors="replace") as f:
#         for line_number, line in enumerate(f, start=1):  # Add line numbers for debugging
#             line = line.strip()
#             if not line:
#                 continue  # Skip empty lines
#             if ':' not in line:
#                 print(f"Skipping invalid line {line_number}: '{line}' (No colon found)")
#                 continue  # Skip lines without a colon
#             parts = line.split(':', 1)  # Split only at the first colon
#             if len(parts) != 2:
#                 print(f"Skipping invalid line {line_number}: '{line}' (Invalid format after split)")
#                 continue  # Skip invalid lines
#             q, a = parts
#             qa_dict[q.strip()] = a.strip()
#     return qa_dict
#
# qa_file_path = r'C:\Users\nagat\OneDrive\Desktop\JARVIS\DATA\Brain_DATA\qna_data.txt'
# qa_dict = load_qa_data(qa_file_path)
#
#
# def save_qa_data(file_path, qa_dict, new_q, new_a):
#     # Open the file in append mode
#     with open(file_path, 'a', encoding='utf-8') as f:
#         # Write the new question-answer pair
#         f.write(f"{new_q}:{new_a}\n")
#
#
# def print_animated_message(message):
#     for char in message:
#         sys.stdout.write(char)
#         sys.stdout.flush()
#         time.sleep(0.075)
#     print()
#
#
# def wiki_search(prompt):
#     search_prompt = prompt.replace("jarvis", "").replace("wikipedia", "").strip()
#
#     try:
#         wiki_summary = wikipedia.summary(search_prompt, sentences=2)
#         animate_thread = threading.Thread(target=print_animated_message, args=(wiki_summary,))
#         speak_thread = threading.Thread(target=speak, args=(wiki_summary,))
#         animate_thread.start()
#         speak_thread.start()
#         animate_thread.join()
#         speak_thread.join()
#
#         # Check if the question is new
#         if search_prompt not in qa_dict:
#             qa_dict[search_prompt] = wiki_summary
#             save_qa_data(qa_file_path, qa_dict, search_prompt, wiki_summary)
#     except wikipedia.exceptions.DisambiguationError as e:
#         print("DisambiguationError: ", e)
#         speak("I am sorry, I found multiple results for your query. Can you please be more specific?")
#     except wikipedia.exceptions.PageError:
#         google_search(search_prompt)
#
#
# def google_search(prompt):
#     query=prompt.replace("who is","")
#     query=query.strip()
#
#     if query:
#         url = "https://www.google.com/search?q=" + query
#         webbrowser.open_new_tab(url)
#         speak("you can see search results on google")
#     else:
#         speak("I am sorry, I could not understand your query")
#
# def brain(text):
#     try:
#         response = mind(text)
#         if not response:
#             wiki_search(text)
#             return
#         animate_thread = threading.Thread(target=print_animated_message, args=(response,))
#         speak_thread = threading.Thread(target=speak, args=(response,))
#         animate_thread.start()
#         speak_thread.start()
#         animate_thread.join()
#         speak_thread.join()
#
#         qa_dict[text] = response
#         save_qa_data(qa_file_path, qa_dict)
#     except Exception as e:
#         wiki_search(text)
#
# wiki_search("who is tata")










#
#
#
#
#
#
#
#
#
#
#
#
#
#











import sys
import time
import threading
import webbrowser
from wikipedia import wikipedia
from HEAD.mouth import speak


# File Path for Q&A Data
QA_FILE_PATH = r'C:\Users\nagat\OneDrive\Desktop\JARVIS\DATA\Brain_DATA\qna_data.txt'


# Load Q&A Data
def load_qa_data(file_path):
    qa_dict = {}
    with open(file_path, 'r', encoding='utf-8', errors="replace") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            if ':' not in line:
                print(f"Skipping invalid line {line_number}: '{line}' (No colon found)")
                continue
            parts = line.split(':', 1)
            if len(parts) != 2:
                print(f"Skipping invalid line {line_number}: '{line}' (Invalid format after split)")
                continue
            q, a = parts
            qa_dict[q.strip()] = a.strip()
    return qa_dict


# Save new Q&A pair
def save_qa_data(file_path, qa_dict, new_q, new_a):
    if new_q not in qa_dict:
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(f"{new_q}:{new_a}\n")
        qa_dict[new_q] = new_a  # Update in-memory dictionary


# Display text with animation
def print_animated_message(message):
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.075)
    print()


# Wikipedia Search
def wiki_search(prompt, qa_dict):
    search_prompt = prompt.replace("jarvis", "").replace("wikipedia", "").strip()

    try:
        # Fetch summary from Wikipedia
        wiki_summary = wikipedia.summary(search_prompt, sentences=2)
        animate_thread = threading.Thread(target=print_animated_message, args=(wiki_summary,))
        speak_thread = threading.Thread(target=speak, args=(wiki_summary,))
        animate_thread.start()
        speak_thread.start()
        animate_thread.join()
        speak_thread.join()

        # Save the Wikipedia result to Q&A dataset
        save_qa_data(QA_FILE_PATH, qa_dict, search_prompt, wiki_summary)
        return wiki_summary
    except wikipedia.DisambiguationError as e:
        print("DisambiguationError: ", e)
        speak("I found multiple results for your query. Please be more specific.")
        return None
    except wikipedia.PageError:
        print(f"No page found for '{search_prompt}'.")
        speak("I could not find a result for your query.")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        speak("Something went wrong while fetching the result.")
        return None


# Google Search
def google_search(query):
    search_query = query.strip()
    url = f"https://www.google.com/search?q={search_query}"
    webbrowser.open_new_tab(url)
    speak("I have opened Google for your query.")

#
# # Main Function to Handle Input and Call Appropriate Functions
# def mind(prompt):
#     # Load Q&A data into memory
#     qa_dict = load_qa_data(QA_FILE_PATH)
#
#     # Direct Google search commands
#     if prompt.lower().startswith(("show", "browse", "open in browser", "search")):
#         google_search(prompt)
#         return
#
#     # Check the dataset for a response
#     response = qa_dict.get(prompt)
#     if response:
#         animate_thread = threading.Thread(target=print_animated_message, args=(response,))
#         speak_thread = threading.Thread(target=speak, args=(response,))
#         animate_thread.start()
#         speak_thread.start()
#         animate_thread.join()
#         speak_thread.join()
#         return
#
#     # Try fetching from Wikipedia
#     response = wiki_search(prompt, qa_dict)
#     if response:
#         return  # If Wikipedia returns a result, stop further processing.
#
#     # As a fallback, direct the user to Google
#     google_search(prompt)




# Define array for command keywords
COMMAND_KEYWORDS = ["show", "browse", "open in browser", "search"]

# Main Function to Handle Input and Call Appropriate Functions
def mind(prompt):
    # Load Q&A data into memory
    qa_dict = load_qa_data(QA_FILE_PATH)

    # Normalize the prompt and extract core query
    core_query = prompt.lower().strip()

    # Check if the prompt starts with any command keywords and remove it
    for command in COMMAND_KEYWORDS:
        if core_query.startswith(command):
            # Remove the command keyword and clean the remaining query
            core_query = core_query.replace(command, "").strip()
            # Directly trigger Google search for commands
            google_search(core_query)
            return  # Exit after triggering Google search

    # Check the dataset for a response
    response = qa_dict.get(core_query)
    if response:
        animate_thread = threading.Thread(target=print_animated_message, args=(response,))
        speak_thread = threading.Thread(target=speak, args=(response,))
        animate_thread.start()
        speak_thread.start()
        animate_thread.join()
        speak_thread.join()
        return

    # Try fetching from Wikipedia for the cleaned query
    response = wiki_search(core_query, qa_dict)
    if response:
        return  # If Wikipedia returns a result, stop further processing.

    # As a fallback, direct the user to Google for the cleaned query
    google_search(core_query)

mind("hello")