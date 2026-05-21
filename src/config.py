from google import genai

CLIENT = genai.Client()
TEXT_MODEL = "gemini-3-flash-preview"
IMAGE_MODEL = "gemini-3.1-flash-image-preview"

BASE_PROMPT = (
    'Act as a storyboard artist. Given the script/scene below, identify the next '
    'visual beat and describe it. This is the script/scene:\n'
)

CONTEXT_PROMPT = '\nPanels already generated (find the next beat after these):\n'

