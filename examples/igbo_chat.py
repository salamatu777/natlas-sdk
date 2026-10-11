from natlas import NAtlasClient

def main():
    client = NAtlasClient()
    response = client.chat("Kedu?", language="ig")
    print(f"N-ATLAS (Igbo): {response.text}")

if __name__ == "__main__":
    main()
