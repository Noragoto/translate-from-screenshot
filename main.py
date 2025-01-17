from PIL import ImageGrab
import io


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

image = get_screenshot_from_clipboard()
if image:
    image.show()