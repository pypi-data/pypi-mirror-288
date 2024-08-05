import time
import uuid
import sys
from datetime import timedelta
from faker.providers import BaseProvider


class CommonProvider(BaseProvider):
    _file_extensions = (
        "flac", "mp3", "wav", "bmp", "gif", "jpeg", "jpg", "png",
        "tiff", "css", "csv", "html", "js", "json", "txt", "mp4",
        "avi", "mov", "webm"
    )

    def duration(self):
        return timedelta(seconds=self.generator.random.randint(0, int(time.time())))

    def uuid(self):
        return uuid.uuid4()

    def rand_small_int(self, pos=False):
        if pos:
            return self.generator.random.randint(0, 32767)
        return self.generator.random.randint(-32768, 32767)

    def rand_int(self, pos=False):
        if pos:
            return self.generator.random.randint(0, 4294967295)
        return self.generator.random.randint(-4294967295, 4294967295)

    def rand_big_int(self):
        return self.generator.random.randint(-sys.maxsize, sys.maxsize)

    def rand_float(self):
        return self.generator.random.random()

    def file_name(self):
        filename = self.generator.word()
        extension = self.generator.random.choice(self._file_extensions)
        return '{0}.{1}'.format(filename, extension)

    def comma_sep_ints(self):
        ints = [str(self.rand_int()) for x in range(10)]
        return ','.join(ints)

    def binary(self, length=512):
        word = self.generator.text(length)
        return str.encode(str(word))
