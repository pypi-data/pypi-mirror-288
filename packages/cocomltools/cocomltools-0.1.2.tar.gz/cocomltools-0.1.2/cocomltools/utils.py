import json
from pathlib import Path
from sklearn.model_selection import train_test_split
from typing import List
import random


def check_is_json(file_path: str) -> bool:
    file_path = Path(file_path)
    return file_path.is_file() and file_path.suffix == ".json"


def load_json_file(json_path: Path):
    with open(json_path, "r") as f:
        json_data = json.load(f)
    return json_data


def get_max_id_from_seq(seq: list[dict]) -> int:
    if len(seq) == 0:
        return 0
    return max([elem["id"] for elem in seq])


def random_split(data: List, split_ratio: float = 0.2):
    random.shuffle(data)
    split_index = int(len(data) * split_ratio)
    set_A, set_B = data[split_index:], data[:split_index]
    return set_A, set_B


def stratified_split(data_dict, ratio=0.2):
    train_split = {}
    test_split = {}

    for key, annotations in data_dict.items():
        if len(annotations) > 1:
            # Splitting annotations with stratification
            annotations_train, annotations_test = train_test_split(
                annotations,
                test_size=ratio,
                stratify=[key] * len(annotations),
                random_state=42,
            )
            train_split[key] = annotations_train
            test_split[key] = annotations_test
        else:
            # For classes with only one annotation, add it to the training set
            train_split[key] = annotations
            test_split[key] = []

    return train_split, test_split
