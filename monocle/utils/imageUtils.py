from PIL import ImageGrab
import os

def grabScreen(savePath):
    screenshot = ImageGrab.grab()
    if os.path.exists(savePath): 
        try: 
            os.remove(savePath)
        except Exception as e:
            print("Error deleting existing screenshot:")
    screenshot.save(savePath, "PNG")
