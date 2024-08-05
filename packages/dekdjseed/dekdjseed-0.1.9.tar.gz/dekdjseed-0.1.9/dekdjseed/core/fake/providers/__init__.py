from dektools.derive import extend_cls_list
from .common import CommonProvider
from .image import ImageBmpProvider


def get_providers_cls(*cls_list):
    return extend_cls_list([CommonProvider, ImageBmpProvider], *cls_list)
