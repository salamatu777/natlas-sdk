from natlas import NAtlasClient

def main():
    client = NAtlasClient()
    response = client.chat("Ina kwana?", language="ha")
    print(f"N-ATLAS (Hausa): {response.text}")

if __name__ == "__main__":
    main()
