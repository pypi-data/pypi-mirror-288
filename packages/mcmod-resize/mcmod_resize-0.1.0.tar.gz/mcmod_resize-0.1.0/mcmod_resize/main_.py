import PIL.Image
import enum
import math

class ImageType(enum.Enum):
    Small = 32
    Big = 128

"""
把一张Minecraft材质转成mcmod.cn要求大小的图片。
"""
def resize_to(img: PIL.Image.Image, to: ImageType) -> PIL.Image.Image:
    width, height = img.width, img.height
    x_offset, y_offset = None, None
    """
    如果宽度不够:
        如果2倍缩放超出要求大小，我们在它周围填上空白
        否则2倍缩放再次调用
    否则，0.5倍缩放然后再次调用
    """
    if width <= to.value:
        if width * 2 <= to.value:
            return resize_to(img.resize((width * 2, height), resample = PIL.Image.Resampling.HAMMING), to)
        x_offset = math.floor((to.value - width) / 2)
    else:
        return resize_to(img.resize((width / 2, height)), to)
    """
    竖向同理。
    """
    if height <= to.value:
        if height * 2 <= to.value:
            return resize_to(img.resize((width, height * 2), resample = PIL.Image.Resampling.HAMMING), to)
        y_offset = math.floor((to.value - height) / 2)
    else:
        return resize_to(img.resize((width, height / 2)), to)
    """
    现在只需要填上空白。
    """
    new_image = PIL.Image.new("RGBA", (to.value, to.value))
    new_image.paste(img, (x_offset, y_offset))
    return new_image
