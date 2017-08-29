# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import Mapping

import six

from marshmallow import Schema, post_load, ValidationError
from marshmallow import post_dump

from polyaxon_schemas.base import BaseConfig
from polyaxon_schemas.graph import GraphConfig


class FeatureProcessorsSchema(Schema):

    @post_dump(pass_original=True)
    def make_dump(self, data, original):
        if isinstance(original.feature_processors, Mapping):
            feature_processors = {}
            for key, val in six.iteritems(original.feature_processors):
                feature_processors[key] = val.to_dict()
            return feature_processors

        raise ValidationError("Feature processor is not valid for, `{}`".format(original))

    @post_load(pass_original=True)
    def make_load(self, data, original):
        if isinstance(original, Mapping):
            feature_processors = {}
            for key, val in six.iteritems(original):
                feature_processors[key] = GraphConfig.from_dict(val)
            return FeatureProcessorsConfig(feature_processors)

        raise ValidationError("Feature processor is not valid for, `{}`".format(original))


class FeatureProcessorsConfig(BaseConfig):
    SCHEMA = FeatureProcessorsSchema
    IDENTIFIER = 'FeatureProcessors'

    def __init__(self, feature_processors):
        self.feature_processors = feature_processors
