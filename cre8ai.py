import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizer

# from fastapi import FastAPI
# from fastapi.testclient import TestClient

from stability_ai import generateImageFromText
from add_text import addText

STYLE = "manga, uncolored"

# # set up FastAPI app
# app = FastAPI()

# model for paraphrasing
model_name = 'tuner007/pegasus_paraphrase'
torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name).to(torch_device)

# receive POST
# @app.post("/")
def receive_post_data(json_data: dict):
    # Access values from json
    username = json_data.get("username","")
    panelNum = json_data.get("panel", "")
    description = json_data.get("description", "")
    text = json_data.get("text", "")
    paraphaseOrNot = json_data.get("paraphase", "")

    # call generateImageFromText
    panel_prompt = description + ", cartoon box, " + STYLE
    panel_image = generateImageFromText(panel_prompt)

    # check for paraphase flag
    if int(paraphaseOrNot) == 0:
        panelWithText = addText(text, panel_image)
    else:
        # use pegasus model for paraphrasing
        batch = tokenizer.prepare_seq2seq_batch(str(text), truncation=True, padding='longest', max_length=60,
                                                return_tensors="pt").to(torch_device)
        translated = model.generate(**batch, max_length=60, num_beams=10, num_return_sequences=1)
        paraphrased_text = tokenizer.batch_decode(translated, skip_special_tokens=True)

        panelWithText = addText(paraphrased_text[0], panel_image)

    # save the panel with text
    panelWithText.save(f"output/panel-{panelNum}-{username}.png")

    return {"message": "Operation successful"}

# def testBackend():
#   test_data = {
#     "username": "panel-1-randominthesky.png",
#     "panel": 1,
#     "description": "A lady and a man holding hands",
#     "text": "I think love you dear yes.",
#     "paraphase": 0
#   }
#   response = client.post("/", json=test_data)
#   assert response.status_code == 200
#   assert response.json() == {"message": "Operation successful"}
