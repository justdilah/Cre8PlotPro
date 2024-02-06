from PIL import Image, ImageDraw, ImageFont

def addText(text, panel):
  # call generatePanelWithText
  panelWithText = generatePanelWithText(text)

  result = Image.new('RGB', (panel.width, panel.height + panelWithText.height))
  result.paste(panel, (0, 0))
  result.paste(panelWithText, (0, panel.height))

  return result

def generatePanelWithText(text):
    # Define image dimensions
    width = 1024
    height = 128

    # Create a white background image
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)

    # text details
    font = ImageFont.truetype(font="Friendszone.ttf", size=50)
    x = 10
    y = 10
    text_color = (0, 0, 0)
    draw.text((x, y), text, fill=text_color, font=font)

    return image