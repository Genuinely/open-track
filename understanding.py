from base64 import b64encode
from requests import post
from os import environ

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return b64encode(image_file.read()).decode("utf-8")

# Path to your image
image_path = "computer_screenshot_heading.png"

# Getting the base64 string
base64_image = encode_image(image_path)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {environ['OPENAI_KEY']}",
}

payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "This is a screenshot of my computer. What specific software program am I using? If I am using a browser, tell me the name of the browser and the name of the website.",
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                },
            ],
        }
    ],
    "max_tokens": 300,
}

response = post(
    "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
)

print(response.json())
