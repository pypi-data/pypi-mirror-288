from typing import Any, Tuple

import numpy as np
import torch
from dataset2vec.model import Dataset2Vec
from torch import Tensor

from wsmf.metamodels.train import (
    LandmarkerReconstructionTrainingInterface,
    MetricLearningTrainingInterface,
)

from .selector import WarmstartHpSelector


class RepresentationBasedHpSelector(WarmstartHpSelector):

    @torch.no_grad()
    def __init__(
        self,
        encoder: (
            Dataset2Vec
            | MetricLearningTrainingInterface
            | LandmarkerReconstructionTrainingInterface
        ),
        metadataset: dict[str, Tuple[Tensor, Tensor]],
        landmarkers: dict[str, Tensor],
        configurations: list[dict[str, Any]],
    ):
        super().__init__(metadataset, landmarkers, configurations)
        self.encoder = encoder
        self.encodings = [
            self.encoder(*dataset_from_db) for dataset_from_db in self.datasets
        ]

    @torch.no_grad()
    def propose_configurations_idx(
        self, dataset: Tuple[Tensor, Tensor], n_configurations: int
    ) -> list[int]:
        dataset_encoding = self.encoder(*dataset)
        distances = np.array(
            [
                torch.norm(dataset_encoding - encoding_from_db).cpu().numpy()
                for encoding_from_db in self.encodings
            ]
        )
        closest_datasets_idx = np.argpartition(distances, n_configurations)[
            :n_configurations
        ].tolist()
        return [
            self.best_configurations_idx[idx] for idx in closest_datasets_idx
        ]
