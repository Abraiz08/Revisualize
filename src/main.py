from google import genai
from PIL import Image

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client()

def main():
    
    scene = input("Scene: ")
    response = generateImage(scene)
    for part in response.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            image = part.as_image()
            image.save("generated_image.png")

def generateImage(scene):
    response = client.models.generate_content(
        model = "gemini-3.1-flash-image-preview",
        contents = "Generate an image of " + scene
    )
    return response

if __name__ == "__main__":
    main()