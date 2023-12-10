from base64 import b64encode
from requests import post
from os import environ, path, listdir
from dotenv import load_dotenv

image_folder = "" # Folder containing the screenshots

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return b64encode(image_file.read()).decode('utf-8')

def batch_gpt_vision(files, batch_size):
  prompt = '''
  These are screenshots of my computer. Analyze these screenshots and fill out this information for each of the attatched screenshots. OUTPUT IT AS JSONL with 1 json object for each screenshot:
  time: time stamp [parse the time stamp from the file name and insert it here]
  program_name: str [fill a value here with what software program I am using (for example, Google Chrome, VSCode, XCode. I may be using multiple software, but do your best guess as to what I am actively using in the screenshot]
  website: str [fill a value here with what website I am using. Use the link: for example, [google.com](http://google.com) or [arxiv.org](http://arxiv.org) If there are multiple websites, do your best guess as to which website I am using]
  category: str [fill a value here with what this categorizes as {entertainment, deep work, light work}]
  project: str [classify me working on one of these projects project {"ski trip", "machine learning project", "mobile app dev", “goofing off”}]
  '''

  content = [
    {"type": "text",
    "text": f"{prompt}"}
  ]


  for image_file in files[:batch_size]:
    content.append(
      {"type": "image_url",
      "image_url": {
        "url": f"data:image/jpeg;base64,{encode_image(image_file)}"
      }
    })

  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {environ['OPENAI_KEY']}"
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

  response = post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

  return response.json()

if __name__ == "__main__":
    
  load_dotenv()

  # List all files in the image folder
  image_files = [path.join(image_folder, file) for file in listdir(image_folder) if file.lower().endswith((".png", ".jpg", ".jpeg"))]

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
    "Authorization": f"Bearer {environ['OPENAI_KEY']}"
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

  response = post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

  print(response.json())