# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon_schemas.initializations import ZerosInitializerConfig, OnesInitializerConfig
from polyaxon_schemas.layers.normalization import BatchNormalizationConfig

from tests.utils import assert_equal_layers


class TestNormalizationConfigs(TestCase):
    def test_batch_normalization_config(self):
        config_dict = {
            'axis': -1,
            'momentum': 0.99,
            'epsilon': 1e-3,
            'center': True,
            'scale': True,
            'beta_initializer': ZerosInitializerConfig().to_schema(),
            'gamma_initializer': OnesInitializerConfig().to_schema(),
            'moving_mean_initializer': ZerosInitializerConfig().to_schema(),
            'moving_variance_initializer': OnesInitializerConfig().to_schema(),
            'beta_regularizer': None,
            'gamma_regularizer': None,
            'beta_constraint': None,
            'gamma_constraint': None,
        }

        config = BatchNormalizationConfig.from_dict(config_dict)
        assert_equal_layers(config, config_dict)
