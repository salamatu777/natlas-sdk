from natlas import NAtlasClient

def main():
    client = NAtlasClient()
    response = client.chat("Hello, how are you today?")
    print(f"Assistant: {response.text}")

if __name__ == "__main__":
    main()
