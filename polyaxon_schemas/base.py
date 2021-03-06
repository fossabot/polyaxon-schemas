# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import Mapping, OrderedDict

import six

from marshmallow import Schema, ValidationError, post_load, post_dump
from marshmallow.utils import utc

from polyaxon_schemas.utils import to_camel_case, TIME_ZONE


class BaseConfig(object):
    """Base for config classes."""

    SCHEMA = None
    IDENTIFIER = None
    REDUCED_ATTRIBUTES = []  # Attribute to remove in the reduced form if they are null.

    def to_dict(self):
        return self.obj_to_dict(self)

    def to_schema(self):
        return self.obj_to_schema(self)

    @classmethod
    def obj_to_dict(cls, obj):
        return cls.SCHEMA(strict=True).dump(obj).data  # pylint: disable=not-callable

    @classmethod
    def remove_reduced_attrs(cls, data):
        obj_dict = OrderedDict((key, value) for (key, value) in six.iteritems(data))
        for attr in cls.REDUCED_ATTRIBUTES:
            if obj_dict[attr] is None:
                del obj_dict[attr]

        return obj_dict

    @classmethod
    def obj_to_schema(cls, obj):
        return {cls.IDENTIFIER: cls.obj_to_dict(obj)}

    @classmethod
    def from_dict(cls, value):
        return cls.SCHEMA(strict=True).load(value).data  # pylint: disable=not-callable

    @staticmethod
    def localize_date(dt):
        if not dt:
            return dt
        if not dt.tzinfo:
            dt = utc.localize(dt)
        return dt.astimezone(TIME_ZONE)


class BaseMultiSchema(Schema):
    __multi_schema_name__ = None
    __configs__ = None
    # to support snake case identifier, e.g. glorot_uniform and GlorotUniform
    __support_snake_case__ = False

    @post_dump(pass_original=True, pass_many=True)
    def handle_multi_schema_dump(self, data, pass_many, original):
        def handle_item(item):
            if hasattr(item, 'get_config'):
                return self.__configs__[item.__class__.__name__].obj_to_schema(item)
            return item.to_schema()

        if pass_many:
            return [handle_item(item) for item in original]

        return handle_item(original)

    @post_load(pass_original=True, pass_many=True)
    def handle_multi_schema_load(self, data, pass_many, original):
        def make(key, val=None):
            key = to_camel_case(key) if self.__support_snake_case__ else key
            try:
                return self.__configs__[key].from_dict(val) if val else self.__configs__[key]()
            except KeyError:
                raise ValidationError("`{}` is not a valid value for schema `{}`".format(
                    key, self.__multi_schema_name__))

        def handle_item(item):
            if isinstance(item, six.string_types):
                return make(item)

            if isinstance(item, Mapping):
                if 'class_name' in item:
                    return make(item['class_name'], item['config'])
                if 'model_type' in item:
                    return make(item.pop('model_type'), item)
                assert len(item) == 1
                key, val = list(six.iteritems(item))[0]
                return make(key, val)

        if pass_many:
            return [handle_item(item) for item in original]

        return handle_item(original)
