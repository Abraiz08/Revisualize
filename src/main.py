from google import genai
from PIL import Image

# The client gets the API key from the environment variable `GEMINI_API_KEY`.

#{
#   "sequence_id": "SC_01",
#   "panel_number": 1,
#   "timestamp": "00:02:15",
#   "visual_description": {
#     "subject": "A weathered detective in a tan trench coat",
#     "action": "Lighting a cigarette while leaning against a brick wall",
#     "setting": "A rain-slicked alleyway in neo-noir Tokyo, neon signs reflecting in puddles",
#     "key_elements": ["glowing embers", "steam from a manhole", "shadowy figure in background"]
#   },
#   "cinematography": {
#     "shot_size": "Medium Close-Up (MCU)",
#     "camera_angle": "Low angle, looking up to create a sense of power",
#     "lens": "35mm anamorphic, shallow depth of field",
#     "composition": "Rule of thirds, subject on the right, leading lines from the alley walls"
#   },
#   "lighting_and_atmosphere": {
#     "time_of_day": "Night",
#     "lighting_style": "Chiaroscuro, high contrast",
#     "primary_color_palette": ["Cyberpunk blue", "Electric orange", "Deep blacks"],
#     "weather": "Heavy rain and mist"
#   },
#   "technical_metadata": {
#     "aspect_ratio": "21:9",
#     "art_style": "Cinematic photorealism, 8k, highly detailed textures",
#     "negative_prompt": "cartoon, bright colors, sunny, blurry face"
#   },
#   "continuity_notes": {
#     "character_consistency": "Ref_ID_Det_01",
#     "previous_panel_connection": "Matches lighting from Panel 0"
#   }
# }


client = genai.Client()

PROMPT = 'Act as a storyboard artist. Given a script or a scene, find the first visual beat for which to create a storyboard panel, analyze it and output a JSOn object strictly in the form:' \
'\n{\n"panel_number":,\n"visual_description": {\n\t"subject":\n\t"action":\n\t"setting":\n\t"key_elements":[]\n\t}\n}'\
'\nOutput the JSON object and nothing else. This is the script/scene:\n'


def main():
    with open('data/scene.txt', 'r') as file:
        data = file.read()
    scene = data
    decomposeSceneToJSON(scene)
    # response = generateImage(scene)
    # for part in response.parts:
    #     if part.text is not None:
    #         print(part.text)
    #     elif part.inline_data is not None:
    #         image = part.as_image()
    #         image.save("output/generated_image.png")

def decomposeSceneToJSON(scene):
    response = response = client.models.generate_content(
        model = "gemini-3-flash-preview",
        contents = PROMPT + scene
    )
    print(response.text)

def generateImage(scene):
    response = client.models.generate_content(
        model = "gemini-3.1-flash-image-preview",
        contents = "Generate an image of " + scene
    )
    return response

if __name__ == "__main__":
    main()