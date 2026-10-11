from natlas import NAtlasClient

def main():
    client = NAtlasClient()
    try:
        result = client.voice_pipeline("question.wav")
        print(f"User asked ({result.language}): {result.transcript}")
        print(f"N-ATLAS replied: {result.response}")
    except Exception as e:
        print(f"Pipeline error: {e}")

if __name__ == "__main__":
    main()
