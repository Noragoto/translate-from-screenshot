import tkinter as tk
from tkinter import messagebox
from PIL import ImageGrab, ImageFont, Image, ImageDraw
import io
import easyocr
import cv2
import numpy as np
from deep_translator import GoogleTranslator


def get_screenshot_from_clipboard():
    try:
        image = ImageGrab.grabclipboard()

        if image:
            byte_io = io.BytesIO()
            image.save(byte_io, 'PNG')
            byte_io.seek(0)
            return image
        else:
            print("The clipboard does not contain an image")
            return None
    except Exception as e:
        print(f"Error when capturing an image: {e}")
        return None


def add_text_to_image(image, text, position, font_path='arial.ttf', font_size=20, color=(255, 255, 255)):
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_image)
    font = ImageFont.truetype(font_path, font_size)
    draw.text(position, text, font=font, fill=color)
    image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    return image


def recognize_text(image):
    image_np = np.array(image)
    reader = easyocr.Reader(['en'])
    translator = GoogleTranslator(source='en', target='ru')

    result = reader.readtext(image_np)
    translated_texts = []

    for bbox, text, prob in result:
        translated_text = translator.translate(text)
        translated_texts.append(translated_text)

    return translated_texts


def on_capture_button_click():
    image = get_screenshot_from_clipboard()
    if image:
        translated_texts = recognize_text(image)
        if translated_texts:
            text_result.delete(1.0, tk.END)  # Clearing the previous content
            for translated_text in translated_texts:
                text_result.insert(tk.END, f"{translated_text}\n")  # Adding the translated text
        else:
            messagebox.showinfo("Result", "Couldn't recognize the text")
    else:
        messagebox.showwarning("Warning", "The clipboard does not contain an image.")


# Main menu
root = tk.Tk()
root.title("Распознавание текста с буфера обмена")
root.geometry('600x400')

# A button to capture a screenshot from the clipboard
capture_button = tk.Button(root, text="Take text from screenshot", command=on_capture_button_click, height=1, width=25)
capture_button.pack(pady=20)

# A text field for displaying the translated text
text_result = tk.Text(root, height=10, width=70)
text_result.pack(pady=10)

# Start GUI
root.mainloop()