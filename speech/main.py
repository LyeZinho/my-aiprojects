from gtts import gTTS
import os

def text_to_speech(text, output_file="output.mp3", language="en", accent="us"):
    # Create a gTTS object with the input text, language, and accent
    tts = gTTS(text=text, lang=language, slow=False, tld=accent)

    # Save the speech audio to the output file
    tts.save(output_file)
    print(f"Speech audio saved to {output_file}")

if __name__ == "__main__":
    
    selected_language = "pt-br"
    selected_accent = "com"
    output_filename = "output.mp3"
    input_text = input("Enter the text you want to convert to speech: ")

    text_to_speech(input_text, output_file=output_filename, language=selected_language, accent=selected_accent)
