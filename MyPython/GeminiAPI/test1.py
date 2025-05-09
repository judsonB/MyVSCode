# To run this code you need to install the following dependencies:
# pip install google-genai

import base64
from google import genai
from google.genai import types


def generate():
    client = genai.Client(
        vertexai=True,
        project="",
        location="",
    )

    files = [
        # Please ensure that the file is available in local system working direrctory or change the file path.
        client.files.upload(file="MyPython/GeminiAPI/image_croissant.jpeg"),
    ]
    model = "gemini-1.5-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_uri(
                    file_uri=files[0].uri,
                    mime_type=files[0].mime_type,
                ),
                types.Part.from_text(text="""Given this image:

1. First, describe the image
2. Then, detail the recipe to bake this item in JSON format. Include item names and quantities for the recipe"""),
            ],
        ),
        types.Content(
            role="model",
            parts=[
                types.Part.from_text(text="""The image shows a basket full of freshly baked croissants. They are golden brown and flaky, and some of them have a slightly burnt edge. They are piled high in the basket, and some of them are overlapping. The background is blurred, but it appears to be a kitchen counter or table.

{
  \"title\": \"Croissants\",
  \"ingredients\": [
    {
      \"name\": \"All-purpose flour\",
      \"quantity\": \"500g\"
    },
    {
      \"name\": \"Salt\",
      \"quantity\": \"10g\"
    },
    {
      \"name\": \"Sugar\",
      \"quantity\": \"20g\"
    },
    {
      \"name\": \"Instant yeast\",
      \"quantity\": \"7g\"
    },
    {
      \"name\": \"Unsalted butter\",
      \"quantity\": \"250g\"
    },
    {
      \"name\": \"Milk\",
      \"quantity\": \"250ml\"
    },
    {
      \"name\": \"Egg yolk\",
      \"quantity\": \"1\"
    }
  ],
  \"instructions\": [
    \"In a large bowl, combine the flour, salt, sugar, and yeast.\",
    \"Add the milk and mix until a dough forms.\",
    \"Knead the dough for 10 minutes, until it is smooth and elastic.\",
    \"Place the dough in a greased bowl, cover, and let it rise in a warm place for 1 hour.\",
    \"Roll out the dough into a rectangle about 1/4 inch thick.\",
    \"Spread the softened butter evenly over the dough.\",
    \"Fold the dough in thirds, like a letter.\",
    \"Wrap the dough in plastic wrap and refrigerate for 30 minutes.\",
    \"Repeat steps 7 and 8 two more times.\",
    \"Roll out the dough into a rectangle about 1/2 inch thick.\",
    \"Cut the dough into triangles.\",
    \"Roll up each triangle, starting from the wide end.\",
    \"Place the croissants on a baking sheet lined with parchment paper.\",
    \"Cover and let them rise for 1 hour.\",
    \"Brush the croissants with egg yolk and bake at 375 degrees Fahrenheit for 15-20 minutes, or until golden brown.\"
  ],
  \"notes\": \"You can use a stand mixer with a dough hook to knead the dough. Make sure the butter is softened to room temperature before spreading it on the dough. The croissants will rise best in a warm place, like a turned-off oven with a bowl of hot water inside.\"
}"""),
            ],
        ),
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""INSERT_INPUT_HERE"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        top_k=64,
        response_mime_type="text/plain",
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")

if __name__ == "__main__":
    generate()
