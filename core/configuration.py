from dataclasses import dataclass
from functools import lru_cache
from typing import List, Any, Tuple

from core.filesystem import get_img_paths


class Configuration:

    def __init__(
        self,
        input_folder: str,
        labels: List[str],
        mode: str,
    ):
        self.input_folder = input_folder
        self.labels = labels
        self.mode = mode
        self.img_paths = get_img_paths(self.input_folder)
        self.num_labels = len(self.labels)
        self.num_images = len(self.img_paths)
