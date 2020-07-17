#
# Copyright (c) 2020 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import json
from typing import Dict

import pytest
import numpy as np

from src.api.models.classification_attributes_model import ClassificationAttributes
from src.api.models.model_config import ModelOutputConfiguration

MOCK_INFERENCE_OUTPUT = {
    'color':
    np.array([[
        [[0.05]],
        [[0.2]],
        [[0.3]],
        [[0.1]],
        [[0.1]],
        [[0.2]],
        [[0.05]],
    ]]),
    'type':
    np.array([[
        [[0.2]],
        [[0.5]],
        [[0.1]],
        [[0.2]]
    ]])
}


@pytest.fixture
def fake_output_config() -> Dict[str, ModelOutputConfiguration]:
    return {
        'color': ModelOutputConfiguration(output_name='color',
                                          classes={
                                              "white": 0.0,
                                              "gray": 1.0,
                                              "yellow": 2.0,
                                              "red": 3.0,
                                              "green": 4.0,
                                              "blue": 5.0,
                                              "black": 6.0
                                          },
                                          is_softmax=True
                                          ),
        'type': ModelOutputConfiguration(output_name='type',
                                         classes={
                                             "car": 0.0,
                                             "van": 1.0,
                                             "truck": 2.0,
                                             "bus": 3.0
                                         },
                                         is_softmax=True
                                         )
    }


@pytest.mark.parametrize("inference_output,expected_response", [
                        (MOCK_INFERENCE_OUTPUT,
                         {"type": "classification", "subtype": None,
                          "classifications": [{"attributes": [
                              {"name": "color", "value": "yellow", "confidence": 0.3},
                              {"name": "color", "value": "gray", "confidence": 0.2},
                              {"name": "color", "value": "blue", "confidence": 0.2},
                              {"name": "color", "value": "red", "confidence": 0.1},
                              {"name": "color", "value": "green", "confidence": 0.1},
                              {"name": "color", "value": "white",
                                  "confidence": 0.05},
                              {"name": "color", "value": "black", "confidence": 0.05}]},
                              {"attributes": [
                                  {"name": "type", "value": "van",
                                      "confidence": 0.5},
                                  {"name": "type", "value": "car",
                                      "confidence": 0.2},
                                  {"name": "type", "value": "bus",
                                      "confidence": 0.2},
                                  {"name": "type", "value": "truck",
                                   "confidence": 0.1},
                              ]}]}
                         )])
def test_postprocess_inference_output(inference_output, expected_response, fake_output_config):
    model = ClassificationAttributes(endpoint=None, ovms_connector=None, input_configs=None,
                                     output_configs=fake_output_config)
    print(model.postprocess_inference_output(inference_output))
    assert model.postprocess_inference_output(
        inference_output) == json.dumps(expected_response)


@pytest.mark.parametrize("inference_output,expected_response,top_k", [
                        (MOCK_INFERENCE_OUTPUT,
                         {"type": "classification", "subtype": None,
                          "classifications": [{"attributes": [
                              {"name": "color", "value": "yellow", "confidence": 0.3}]},
                              {"attributes": [
                                  {"name": "type", "value": "van",
                                      "confidence": 0.5},
                              ]}]},
                         1
                         )])
def test_postprocess_inference_output_top_k(inference_output, expected_response, top_k, fake_output_config):
    for key in fake_output_config.keys():
        fake_output_config[key].top_k_results = top_k
    model = ClassificationAttributes(endpoint=None, ovms_connector=None, input_configs=None,
                                     output_configs=fake_output_config)
    print(model.postprocess_inference_output(inference_output))
    assert model.postprocess_inference_output(
        inference_output) == json.dumps(expected_response)


@pytest.mark.parametrize("inference_output,expected_response,confidence_threshold", [
                        (MOCK_INFERENCE_OUTPUT,
                         {"type": "classification", "subtype": None,
                          "classifications": [{"attributes": [
                              {"name": "color", "value": "yellow", "confidence": 0.3},
                              {"name": "color", "value": "gray", "confidence": 0.2},
                              {"name": "color", "value": "blue", "confidence": 0.2}]},
                              {"attributes": [
                                  {"name": "type", "value": "van",
                                      "confidence": 0.5},
                                  {"name": "type", "value": "car",
                                      "confidence": 0.2},
                                  {"name": "type", "value": "bus",
                                      "confidence": 0.2},
                              ]}]},
                         0.2
                         )])
def test_postprocess_inference_output_confidence_threshold(inference_output,
                                                           expected_response,
                                                           confidence_threshold, fake_output_config):
    for key in fake_output_config.keys():
        fake_output_config[key].confidence_threshold = confidence_threshold
    model = ClassificationAttributes(endpoint=None, ovms_connector=None, input_configs=None,
                                     output_configs=fake_output_config)
    assert model.postprocess_inference_output(
        inference_output) == json.dumps(expected_response)
