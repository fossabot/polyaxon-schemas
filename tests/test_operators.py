# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon_schemas.polyaxonfile.parser import Parser
from polyaxon_schemas.operators import ForConfig, IfConfig
from polyaxon_schemas.polyaxonfile.specification import Specification


class TestOperatorConfigs(TestCase):
    def test_for_operator_config(self):
        config_dict = {
            'len': 5,
            'do': 'Value at {{ i }}',
            'index': 'i'
        }
        config = ForConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        expected = ['Value at 0', 'Value at 1', 'Value at 2', 'Value at 3', 'Value at 4']
        assert expected == config.parse(Specification, Parser(), {})

        config_dict = {
            'len': 5,
            'do': [{'Conv2D': {'strides': ['{{ i }}', '{{ i }}']}},
                   {'Pooling2D': {'strides': ['{{ i }}', '{{ i }}']}}],
            'index': 'i'
        }
        config = ForConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        # Lists get flattened
        expected = [{'Conv2D': {'strides': [0, 0]}}, {'Pooling2D': {'strides': [0, 0]}},
                    {'Conv2D': {'strides': [1, 1]}}, {'Pooling2D': {'strides': [1, 1]}},
                    {'Conv2D': {'strides': [2, 2]}}, {'Pooling2D': {'strides': [2, 2]}},
                    {'Conv2D': {'strides': [3, 3]}}, {'Pooling2D': {'strides': [3, 3]}},
                    {'Conv2D': {'strides': [4, 4]}}, {'Pooling2D': {'strides': [4, 4]}}]
        assert expected == config.parse(Specification, Parser(), {})

    def test_if_operator_config(self):
        config_dict = {
            'cond': '{{ i }} == 5',
            'do': 'It was True',
            'else_do': 'It was False'
        }
        config = IfConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
        assert 'It was True' == config.parse(Specification, Parser(), {'i': 5})
        assert 'It was False' == config.parse(Specification, Parser(), {'i': 3})
