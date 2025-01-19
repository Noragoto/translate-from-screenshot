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
    # Преобразуем изображение OpenCV в PIL
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Создаем объект для рисования
    draw = ImageDraw.Draw(pil_image)

    # Загружаем шрифт
    font = ImageFont.truetype(font_path, font_size)

    # Добавляем текст
    draw.text(position, text, font=font, fill=color)

    # Преобразуем обратно в формат OpenCV
    image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    return image

def recognize_text(image):
    # Преоьразуем PIL изображение в np.array
    image_np = np.array(image)

    reader = easyocr.Reader(['en'])
    translator = GoogleTranslator(source='en', target='ru')

    result = reader.readtext(image_np)

    for bbox, text, prob in result:
        # Переводим текст
        translated_text = translator.translate(text)
        print(translated_text)
    return result


image = get_screenshot_from_clipboard()
if image:
    result = recognize_text(image)