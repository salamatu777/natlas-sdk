from natlas import NAtlasClient

def main():
    client = NAtlasClient()
    response = client.chat("Bawo ni?", language="yo")
    print(f"N-ATLAS (Yoruba): {response.text}")

if __name__ == "__main__":
    main()
