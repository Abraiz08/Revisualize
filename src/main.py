import json


import config
from models import Panel, VisualDescription

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


def main():
    num_panels = int(input("Enter number of panels: "))
    panels = createPanelObjects(num_panels)
    with open("data/panelsdata.json", "w") as file:
        json.dump([p.model_dump() for p in panels], file, indent=2)

    with open('data/panelsdata.json', 'r') as file:
        panels = [Panel.model_validate(p) for p in json.load(file)]

    generateStoryboard(panels)

def createPanelObjects(num_panels: int) -> list[Panel]:
    with open('data/scene.txt', 'r') as file:
        scene = file.read()
    panels: list[Panel] = []
    #TODO prime the AI to split the scene into num_panels visual beats first before running this (to cover the full scene)
    for i in range(num_panels):
        visual_description = decomposeNextBeat(scene, panels)
        panels.append(Panel(panel_number=i, visual_description=visual_description))
    return panels

def decomposeNextBeat(scene: str, panels_so_far: list[Panel]) -> VisualDescription:
    #TODO runs too many times with increasing prompt size
    context_json = json.dumps([p.model_dump() for p in panels_so_far], indent=2)
    response = config.CLIENT.models.generate_content(
        model = config.TEXT_MODEL,
        contents=config.BASE_PROMPT + scene + config.CONTEXT_PROMPT + context_json,
        config={
            "response_mime_type": "application/json",
            "response_schema": VisualDescription,
        },
    )
    return response.parsed

def generateStoryboard(panels: list[Panel]):
    for panel in panels:
        generatePanel(panel)

def generatePanel(panel: Panel):
    response = config.CLIENT.models.generate_content(
        model = config.IMAGE_MODEL,
        contents="Generate an image of " + panel.model_dump_json(),
    )

    for part in response.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            image = part.as_image()
            image.save(f"output/generated_image{panel.panel_number}.png")

if __name__ == "__main__":
    main() 