"""
voice_ai_agent.py
-------------------

This module implements a simple voice‑enabled AI agent in Python.  The agent
listens to the user's speech via the microphone, transcribes the audio to
text, generates a response, and plays the response back using text‑to‑speech.

The `speech_recognition` library provides a straightforward way to capture
audio from a microphone and convert it to text.  According to the
SpeechRecognition PyPI page, the library supports multiple speech recognition
engines and APIs and can be used to perform recognition both online and
offline【760221817442684†L31-L35】.  To capture audio from a microphone you will
also need the optional `PyAudio` package.  Simplilearn's tutorial on speech
recognition notes that if you intend to capture audio input from a
microphone, you should install PyAudio using ``pip install pyaudio``【269290886358714†L263-L267】.

This example uses the built‑in Google Web Speech API through the
`recognize_google` method to transcribe speech to text.  The Real Python
tutorial on speech recognition shows how to use `speech_recognition.Recognizer`
and `speech_recognition.Microphone` to record audio and call the
``recognize_google`` method【313621666111249†L983-L1015】.  For text‑to‑speech
output, the script uses the `pyttsx3` library, which works offline on most
platforms.

Note: In order to generate conversational responses, this example simply echoes
the recognized text back to the user.  You can replace the implementation
inside ``respond()`` with a call to an actual language model (for example,
OpenAI's ChatGPT API or a local HuggingFace model via ``transformers``) if you
have the appropriate libraries and API keys.  Keep in mind that using online
APIs may require an internet connection and could incur costs.
"""

import speech_recognition as sr
import pyttsx3
from typing import Optional


class VoiceAgent:
    """A simple voice‑enabled agent that listens and speaks."""

    def __init__(self) -> None:
        # Create a recognizer and a TTS engine.
        self.recognizer = sr.Recognizer()
        # Initialize the text‑to‑speech engine.  On some systems the default
        # driver may not be available; if you experience issues, consult
        # pyttsx3 documentation for details on selecting an engine.
        self.tts_engine = pyttsx3.init()

    def listen(self) -> Optional[str]:
        """
        Listen for a single utterance from the microphone and return the
        transcribed text.

        Returns ``None`` if speech could not be transcribed.
        """
        with sr.Microphone() as source:
            # Adjust for ambient noise and record audio from the microphone.
            self.recognizer.adjust_for_ambient_noise(source)
            print("Listening… (say 'quit' to exit)")
            audio = self.recognizer.listen(source)

        # Try to recognize the speech using the Google Web Speech API.
        try:
            transcription = self.recognizer.recognize_google(audio)
            print(f"User said: {transcription}")
            return transcription
        except sr.UnknownValueError:
            # Speech was unintelligible.
            print("Could not understand audio")
            return None
        except sr.RequestError as exc:
            # API was unreachable or unresponsive.
            print(f"Speech recognition API error: {exc}")
            return None

    def respond(self, message: str) -> str:
        """
        Generate a response to the user's message.

        This simple implementation echoes the user's input.  Replace this
        method with calls to a language model for more sophisticated
        conversations.
        """
        return f"You said: {message}"

    def speak(self, message: str) -> None:
        """Use text‑to‑speech to speak the provided message aloud."""
        self.tts_engine.say(message)
        self.tts_engine.runAndWait()



def main() -> None:
    """
    Entry point for running the voice agent in a loop.

    The agent will listen for user input until the user says 'quit',
    'exit' or 'stop'.  Each recognized utterance is passed to
    ``respond()`` and the returned text is spoken back to the user.
    """
    agent = VoiceAgent()
    while True:
        user_input = agent.listen()
        if user_input is None:
            agent.speak("Sorry, I didn't catch that. Please try again.")
            continue

        if user_input.strip().lower() in {"quit", "exit", "stop"}:
            agent.speak("Goodbye!")
            break

        # Generate a response and speak it.
        reply = agent.respond(user_input)
        print(f"Agent: {reply}")
        agent.speak(reply)


if __name__ == "__main__":
    main()
