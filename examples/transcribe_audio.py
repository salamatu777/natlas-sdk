from natlas import NAtlasClient

def main():
    # Make sure you have a valid audio file named 'test_audio.wav'
    client = NAtlasClient()
    try:
        result = client.transcribe("test_audio.wav")
        print(f"Language: {result.language}")
        print(f"Transcript: {result.text}")
    except Exception as e:
        print(f"Error transcribing: {e}")

if __name__ == "__main__":
    main()
