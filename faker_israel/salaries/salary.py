import os
import json
import functools

from .. import common_draw
from ..common import PRIVATE_DATA_PATH


@functools.lru_cache()
def get_name_translations():
    with open(os.path.join(PRIVATE_DATA_PATH, 'salaries', 'name_translations.json')) as f:
        return json.load(f)


def _(text):
    return get_name_translations()[text]


class Salary:

    def __init__(self, id_, provider, test=False, no_bg=False, mock=False, no_pdf=False, source_image=None, **kwargs):
        self.id = id_
        self.provider = provider
        self.test = test
        self.no_bg = no_bg
        self.mock = mock
        self.no_pdf = no_pdf
        self.source_image = source_image

    def save_init(self, output_path, source_file_name, annotation_labels_item_filter, labels, default_label):
        original_width, original_height, res_labels = common_draw.init_draw_labels(
            annotation_labels_item_filter, 'salaries/label_studio.json', 'full',
            labels, default_label, mock=self.mock
        )
        image_draw, image = common_draw.init_draw_image(
            output_path, source_file_name, original_width, original_height, getattr(self, 'source_image', None)
        )
        return image_draw, res_labels, image
