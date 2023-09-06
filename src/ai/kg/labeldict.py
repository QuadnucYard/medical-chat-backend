from typing import overload
import numpy as np


class LabelDict:
    def __init__(self, labels: list[str], unk_label="[UNK]") -> None:
        self.unk_label = unk_label
        self.labels = [unk_label] + labels if unk_label not in labels else labels
        assert len(self.labels) == len(set(self.labels)), "ERROR: repeated labels appeared!"

    # @overload
    # def __getitem__(self, idx: int) -> str:
    #     ...

    # @overload
    # def __getitem__(self, idx: list[int]) -> list[str]:
    #     ...

    # @overload
    # def __getitem__(self, idx: str) -> int:
    #     ...

    # @overload
    # def __getitem__(self, idx: list[str]) -> list[int]:
    #     ...

    # def __getitem__(
    #     self, idx: int | list[int] | str | list[str]
    # ) -> list[int] | list[str] | int | str | None:
    #     if isinstance(idx, list):
    #         return [self.__getitem__(i) for i in idx]
    #     elif isinstance(idx, str):
    #         return self.encode(idx)
    #     elif isinstance(idx, int):
    #         return self.decode(idx)

    #     print("Warning: unknown indexing type!")
    #     return None

    def __len__(self) -> int:
        return len(self.labels)

    def save_dict(self, save_path) -> None:
        with open(save_path, "w") as f:
            f.write("\n".join(self.labels))

    @overload
    def encode(self, labels: str) -> int:
        ...

    @overload
    def encode(self, labels: list[str]) -> list[int]:
        ...

    def encode(self, labels: str | list[str]) -> int | list[int]:
        if isinstance(labels, list):
            return [self.encode(i) for i in labels]
        if labels in self.labels:
            return self.labels.index(labels)
        else:
            return self.labels.index(self.unk_label)

    @overload
    def decode(self, labels: int) -> str:
        ...

    @overload
    def decode(self, labels: list[int]) -> list[str]:
        ...

    def decode(self, labels: int | list[int]) -> list[str] | str:
        if isinstance(labels, list):
            return [self.decode(i) for i in labels]
        return self.labels[labels]

    @classmethod
    def load_dict(cls, load_path, **kwargs):
        with open(load_path, "r") as f:
            labels = f.read().strip("\n").split("\n")

        return cls(labels, **kwargs)
