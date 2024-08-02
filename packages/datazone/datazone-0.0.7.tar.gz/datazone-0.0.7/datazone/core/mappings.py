from typing import Optional

from datazone.core.dataset import Dataset
from datazone.models.common import OutputMode


class Input:
    def __init__(self, entity, output_name: Optional[str] = None, **kwargs):
        self.entity = entity
        self.output_name = output_name
        self.kwargs = kwargs


class Output:
    def __init__(
        self,
        dataset: Optional[Dataset] = None,
        materialized: bool = False,
        partition_by: Optional[list[str]] = None,
        mode: Optional[str] = OutputMode.OVERWRITE,
    ):
        self.dataset = dataset
        self.materialize = materialized
        self.partition_by = partition_by
        self.mode = mode
