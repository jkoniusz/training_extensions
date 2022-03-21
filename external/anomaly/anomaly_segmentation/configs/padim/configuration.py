"""
Configurable parameters for Padim anomaly classification task
"""

# Copyright (C) 2021 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions
# and limitations under the License.

from attr import attrs
from ote_anomalib.configs.configuration import BaseAnomalyConfig
from ote_sdk.configuration.elements import string_attribute


@attrs
class PadimAnomalySegmentationConfig(BaseAnomalyConfig):
    """
    Configurable parameters for PADIM anomaly classification task.
    """

    header = string_attribute("Configuration for Padim")
    description = header