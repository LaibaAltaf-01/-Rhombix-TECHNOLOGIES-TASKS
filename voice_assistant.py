"""
JARVIS-Lite — A Python Voice Assistant
========================================
Runs in two modes, auto-detected:

  1. VOICE MODE  (on your own machine, with a mic + speakers)
     Uses `speech_recognition` (Google Web Speech API) for listening
     and `pyttsx3` for offline text-to-speech.

  2. TEXT MODE  (works anywhere — no mic/speaker required, e.g. servers,
     sandboxes, or when the voice libraries / hardware aren't available)
     You type instead of speak, and replies are printed instead of spoken.

Install for full voice mode on your own PC:
    pip install SpeechRecognition pyttsx3 pyaudio

Run it:
    python voice_assistant.py
"""

import datetime
import random
import sys
import webbrowser
import math
import re

# --------------------------------------------------------------------------
# Try to load real voice libraries. If unavailable (no mic, no package,
# no audio device — like in this sandbox), fall back to text mode.
# --------------------------------------------------------------------------
VOICE_MODE = False
try:
    import speech_recognition as sr
    import pyttsx3

    recognizer = sr.Recognizer()
    tts_engine = pyttsx3.init()
    tts_engine.setProperty("rate", 175)
    with sr.Microphone() as _test_mic:
        pass  # confirms a real microphone device exists
    VOICE_MODE = True
except Exception:
    VOICE_MODE = False


ASSISTANT_NAME = "JARVIS"
USER_NAME = "Laiba"


def speak(text: str):
    """Output a response — spoken aloud in voice mode, printed in text mode."""
    print(f"{ASSISTANT_NAME}: {text}")
    if VOICE_MODE:
        tts_engine.say(text)
        tts_engine.runAndWait()


def listen() -> str:
    """Get user input — via microphone in voice mode, via typing in text mode."""
    if VOICE_MODE:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"{USER_NAME}: {command}")
            return command.lower()
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            speak("My speech service seems to be offline right now.")
            return ""
    else:
        try:
            command = input(f"{USER_NAME}: ")
        except EOFError:
            return "exit"
        return command.lower().strip()


# --------------------------------------------------------------------------
# Intent handlers
# --------------------------------------------------------------------------
def handle_greeting():
    hour = datetime.datetime.now().hour
    if hour < 12:
        period = "morning"
    elif hour < 17:
        period = "afternoon"
    else:
        period = "evening"
    speak(f"Good {period}, {USER_NAME}! I'm {ASSISTANT_NAME}. How can I help you today?")


def handle_time():
    now = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"It's currently {now}.")


def handle_date():
    today = datetime.datetime.now().strftime("%A, %B %d, %Y")
    speak(f"Today is {today}.")


def handle_joke():
    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs.",
        "I told my computer I needed a break, and it said no problem — it froze immediately.",
        "Why did the developer go broke? Because they used up all their cache.",
        "There are 10 types of people in the world: those who understand binary, and those who don't.",
    ]
    speak(random.choice(jokes))


def handle_calculation(command: str):
    expression = command
    for word in ["calculate", "what is", "what's", "compute", "solve"]:
        expression = expression.replace(word, "")
    expression = expression.strip()
    if not re.fullmatch(r"[0-9\.\+\-\*\/\(\)\s]+", expression):
        speak("I can only safely calculate simple math expressions right now.")
        return
    try:
        result = eval(expression, {"__builtins__": {}}, {"math": math})
        speak(f"That equals {result}.")
    except Exception:
        speak("Sorry, I couldn't work out that calculation.")


def handle_search(command: str):
    query = command.replace("search for", "").replace("search", "").replace("google", "").strip()
    if not query:
        speak("What would you like me to search for?")
        return
    speak(f"Searching the web for {query}.")
    if VOICE_MODE:
        webbrowser.open(f"https://www.google.com/search?q={query}")


def handle_notes(command: str, notes: list):
    if "add" in command or "take" in command or "note that" in command or "note:" in command:
        note = command
        for phrase in ["add a note that", "take a note that", "add note that",
                       "take note that", "note that", "add a note", "take a note",
                       "add note", "take note", "note:"]:
            if phrase in note:
                note = note.split(phrase, 1)[1]
                break
        note = note.strip()
        if note:
            notes.append(note)
            speak(f"Noted: {note}")
        else:
            speak("What should I note down?")
    elif "read" in command or "show" in command:
        if notes:
            speak("Here are your notes: " + "; ".join(notes))
        else:
            speak("You don't have any notes yet.")
    return notes


def handle_unknown():
    responses = [
        "I'm not sure how to help with that yet, but I'm learning!",
        "Could you rephrase that? I didn't quite catch the intent.",
        "That's outside what I can do right now.",
    ]
    speak(random.choice(responses))


# --------------------------------------------------------------------------
# Main loop
# --------------------------------------------------------------------------
def main():
    mode_label = "VOICE MODE (microphone + speech)" if VOICE_MODE else "TEXT MODE (no mic/speaker detected)"
    print("=" * 60)
    print(f" {ASSISTANT_NAME} — Python Voice Assistant  [{mode_label}]")
    print("=" * 60)

    notes = []
    handle_greeting()

    while True:
        command = listen()
        if not command:
            continue

        if any(word in command for word in ["exit", "quit", "bye", "goodbye", "stop"]):
            speak("Goodbye! Have a great day.")
            break

        elif any(word in command for word in ["hello", "hi ", "hey"]) or command in ("hi", "hey"):
            handle_greeting()

        elif "time" in command:
            handle_time()

        elif "date" in command or "day is it" in command:
            handle_date()

        elif "joke" in command:
            handle_joke()

        elif any(word in command for word in ["calculate", "what is", "what's", "compute", "solve"]) and \
                re.search(r"\d", command):
            handle_calculation(command)

        elif "search" in command or "google" in command:
            handle_search(command)

        elif "note" in command:
            notes = handle_notes(command, notes)

        elif "your name" in command:
            speak(f"I'm {ASSISTANT_NAME}, your personal voice assistant.")

        elif "how are you" in command:
            speak("I'm running smoothly and ready to help!")

        else:
            handle_unknown()


if __name__ == "__main__":
    main()
