from FUNCTION.wish import wish
from FUNCTION.welcome import welcome
from HEAD.ear import listen
from HEAD.brain import mind
def jarvis():
#    welcome()
    wish()
    while True:
        text = listen().lower()
        text =text.replace("jar", "jarvis")
        if "jarvis" in text:
            welcome()

jarvis()