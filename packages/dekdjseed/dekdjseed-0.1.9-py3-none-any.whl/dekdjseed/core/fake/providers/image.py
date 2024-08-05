from io import BytesIO
from microbmp import MicroBMP
from faker.providers import BaseProvider


class ImageBmpProvider(BaseProvider):
    def image_bmp(self, width=None, height=None, depth=24, rand=(100, 200)):
        if width is None:
            width = self.generator.random.randint(*rand)
        if height is None:
            height = self.generator.random.randint(*rand)
        img = MicroBMP(width, height, depth)
        div = rand_div(self.generator.random, img.DIB_h)
        div_color = [tuple(self.generator.random.randint(0, 255) for _ in range(3)) for _ in range(len(div))]
        for h in range(img.DIB_h):
            c = div_color[-1]
            div[-1] -= 1
            if div[-1] == 0:
                div.pop()
                div_color.pop()
            for w in range(img.DIB_w):
                img[w, h] = c
        bs = BytesIO()
        img.write_io(bs)
        return bs.getvalue()


def rand_div(random, total):
    cursor = total
    result = []

    while cursor > 0:
        result.append(random.randint(1, cursor))
        cursor -= result[-1]
    return result
