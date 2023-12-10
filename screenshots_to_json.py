import base64
import requests
import os

api_key = "" # OpenAI API Key
image_folder = "" # Folder containing the screenshots
batch_size = 3  # how many screenshots to process

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


# List all files in the image folder
image_files = [os.path.join(image_folder, file) for file in os.listdir(image_folder) if file.lower().endswith((".png", ".jpg", ".jpeg"))]



prompt = '''
These are screenshots of my computer. Analyze these screenshots and fill out this information for each of the attatched screenshots. OUTPUT IT AS A JSON LIST with one json object for each:
program_name: str [fill a value here with what program I am using]
website: str [fill a value here with what website I am using]
category: str [fill a value here with what this categorizes as {entertainment, deep work, light work}]
project: str [classify me working on one of these projects project {"ski trip", "movie night", "app dev"}]
description: str [give me a one line description of what you think I am doing in the context of the project]
'''

content = [
  {"type": "text",
   "text": f"{prompt}"}
]

for image_file in image_files[:batch_size]:
  content.append(
    {"type": "image_url",
    "image_url": {
      "url": f"data:image/jpeg;base64,{encode_image(image_file)}"
    }
  })

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

payload = {
  "model": "gpt-4-vision-preview",
  "messages": [
    {
      "role": "user",
      "content": content
    }
  ],
  "max_tokens": 400
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

print(response.json())