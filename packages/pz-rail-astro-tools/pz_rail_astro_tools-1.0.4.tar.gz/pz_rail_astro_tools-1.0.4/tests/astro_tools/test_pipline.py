import os
from rail.utils.testing_utils import build_and_read_pipeline

import pytest

@pytest.mark.parametrize(
    "pipeline_class",
    [
        'rail.pipelines.utility.apply_phot_errors.ApplyPhotErrorsPipeline',
        'rail.pipelines.utility.spectroscopic_selection_pipeline.SpectroscopicSelectionPipeline',
    ]
)
def test_build_and_read_pipeline(pipeline_class):
    build_and_read_pipeline(pipeline_class)

