from google import genai
from PIL import Image

import json

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

#TODO maybe try splitting the file into line by line and then sending to ai with the line at which the last visual beat left off, that way we wont have to send the whole wall of text everytime, possibly using less tokens?
#TODO make different services, eg, the image generation starts as soon as we have the first json panel data
#TODO save character descriptions somewhere and sue them to generate consistently 

client = genai.Client()

PROMPT = 'Act as a storyboard artist. Given a script or a scene, find the next visual beat for which to create a storyboard panel, analyze it and output a JSOn object strictly in the form:' \
'\n{\n"visual_description": {\n\t"subject":\n\t"action":\n\t"setting":\n\t"key_elements":[]\n\t}\n}'\
'\nOutput the JSON object and nothing else. This is the script/scene:\n'

CONTEXT = '\nThis is all the context so far, the next visual beat should be after all this context:\n'

def main():

    #TODO make this typesafe

    # num_panels = input("Enter number of panels: ")
    # panelsJSONString = createSceneObjects(int(num_panels))
    # panelsdata = json.loads(panelsJSONString)

    # with open("data/panelsdata.json", "w") as file:
    #     json.dump(panelsdata, file)
    
    with open('data/panelsdata.json', 'r') as file:
        panelsdata = json.load(file)
    
    generateStoryboard(panelsdata)

def createSceneObjects(num_panels: int) -> str:
    with open('data/scene.txt', 'r') as file:
        data = file.read()
    scene = data
    context = ''
    #TODO prime the AI to split the scene into num_panels visual beats first before running this (to cover the full scene)
    for i in range(num_panels):  
        context += "{\n\"panel_number\": " + "\""+str(i)+"\"," + decomposeSceneToJSON(scene, context)[1:]
        if (i != num_panels - 1):
            context += ","
    return "["+context+"]"

def decomposeSceneToJSON(scene: str, context: str) -> str:
    #TODO runs too many times with increasing prompt size
    response = response = client.models.generate_content(
        model = "gemini-3-flash-preview",
        contents = PROMPT + scene + CONTEXT + context
    )
    return response.text

def generateStoryboard(panelsdata: dict):
    for panel in panelsdata:
        generatePanel(str(panel), panel["panel_number"])

def generatePanel(panel: str, panel_number: str):
#-> genai.types.GenerateContentResponse2:
    response = client.models.generate_content(
        model = "gemini-3.1-flash-image-preview",
        contents = "Generate an image of " + panel
    )

    for part in response.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            image = part.as_image()
            image.save("output/generated_image" + panel_number + ".png")

if __name__ == "__main__":
    main() 