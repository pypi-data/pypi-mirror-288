import base64
import functools
import inspect
from typing import Optional, get_origin, get_args, Union

from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from pydantic import BaseModel

from .db_sqlalchemy_instance import default_sqlalchemy_instance as db
from .logger_setting import pyjson_translator_logging

GLOBAL_DB_SCHEMA_CACHE = {}


def generate_db_schema(input_class_instance: any,
                       db_sqlalchemy_merge: bool = False):
    input_db_class = input_class_instance.__class__

    if input_db_class in GLOBAL_DB_SCHEMA_CACHE:
        return GLOBAL_DB_SCHEMA_CACHE[input_db_class]

    def get_nested_schema(relation_class_instance):
        related_model = relation_class_instance.mapper.entity
        related_instance = related_model()
        return generate_db_schema(related_instance, db_sqlalchemy_merge)

    schema_fields = {}
    for attr_name, relation in input_db_class.__mapper__.relationships.items():
        if relation.uselist:
            nested_db_schema = get_nested_schema(relation)
            if nested_db_schema:
                schema_fields[attr_name] = fields.Nested(nested_db_schema, many=True)

    class Meta:
        model = input_db_class
        load_instance = db_sqlalchemy_merge

    schema_class = type(f"{input_db_class.__name__}Schema", (SQLAlchemyAutoSchema,),
                        {"Meta": Meta, **schema_fields})

    GLOBAL_DB_SCHEMA_CACHE[input_db_class] = schema_class
    return schema_class


def orm_class_to_dict(instance: any,
                      db_sqlalchemy_merge: bool = False):
    schema = generate_db_schema(instance, db_sqlalchemy_merge)()
    return schema.dump(instance)


def orm_class_from_dict(cls: type,
                        data: any,
                        db_sqlalchemy_instance: SQLAlchemy = db,
                        db_sqlalchemy_merge: bool = False):
    schema = generate_db_schema(cls(), db_sqlalchemy_merge)()
    schema_object = schema.load(data)

    if db_sqlalchemy_merge:
        return db_sqlalchemy_instance.session.merge(schema_object)
    else:
        return schema_object


def with_prepare_func_json_data(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        prepare_json_data(func, args, kwargs)
        return func(*args, **kwargs)

    return wrapper


def with_post_func_data(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return_type = type(result)

        if result is None:
            return result

        if return_type is not inspect.Signature.empty and isinstance(return_type, tuple):
            serialized_results = tuple(serialize_value(val) for val in result)
            deserialized_results = tuple(deserialize_value(val, get_real_return_type(typ))
                                         for val, typ in zip(serialized_results, return_type))
            return deserialized_results
        elif return_type is not inspect.Signature.empty:
            serialized_result = serialize_value(result)
            return deserialize_value(serialized_result, get_real_return_type(return_type))
        else:
            fail_to_translator(f"Unhandled real post_func type {type(return_type).__name__}")

    return wrapper


def get_real_return_type(return_type: type,
                         db_sqlalchemy_instance: SQLAlchemy = db):
    if return_type in (int, float, str, bool, bytes, complex):
        return return_type
    if return_type in (list, tuple, set, dict):
        return return_type
    origin = get_origin(return_type)
    if origin in (list, tuple, set, dict):
        return origin
    if origin is Union:
        return get_real_return_type(get_args(return_type)[0])
    if issubclass(return_type, BaseModel) or issubclass(return_type, db_sqlalchemy_instance.Model):
        return return_type
    fail_to_translator(f"Unhandled real return type {type(return_type).__name__}")


def prepare_json_data(func, args, kwargs):
    sig = inspect.signature(func)
    bound_args = sig.bind(*args, **kwargs)
    bound_args.apply_defaults()

    json_data = {}
    deserialized_data = {}

    for name, arg_value in bound_args.arguments.items():
        if name == 'self':
            pyjson_translator_logging.info(f"Skipping 'self' parameter.")
            continue

        serialized_value = serialize_value(arg_value)
        json_data[name] = serialized_value
        pyjson_translator_logging.info(f"Processed parameter '{name}': {serialized_value}")

        deserialized_value = deserialize_value(serialized_value, type(arg_value))
        deserialized_data[name] = deserialized_value
        pyjson_translator_logging.info(f"Deserialized parameter '{name}': {deserialized_value}")

    pyjson_translator_logging.info(f"Final JSON data prepared for sending: {json_data}")
    return json_data


def serialize_value(value: any,
                    db_sqlalchemy_instance: SQLAlchemy = db,
                    db_sqlalchemy_merge: bool = False):
    if value is None:
        pyjson_translator_logging.info("Serializing None value.")
        return value
    if isinstance(value, (int, float, str, bool)):
        pyjson_translator_logging.info(f"Serializing primitive type: {value}")
        return value
    if isinstance(value, bytes):
        encoded_bytes = base64.b64encode(value).decode('utf-8')
        pyjson_translator_logging.info(f"Serializing bytes: {encoded_bytes}")
        return encoded_bytes
    if isinstance(value, complex):
        complex_dict = {"real": value.real, "imaginary": value.imag}
        pyjson_translator_logging.info(f"Serializing complex number to dict: {complex_dict}")
        return complex_dict
    if isinstance(value, (list, tuple)):
        pyjson_translator_logging.info(f"Serializing list or tuple: {value}")
        return [serialize_value(item) for item in value]
    if isinstance(value, set):
        pyjson_translator_logging.info(f"Serializing set: {value}")
        return [serialize_value(item) for item in value]
    if isinstance(value, dict):
        pyjson_translator_logging.info(f"Serializing dictionary. Keys: {value.keys()}")
        return {serialize_value(k): serialize_value(v) for k, v in value.items()}
    if isinstance(value, db_sqlalchemy_instance.Model):
        pyjson_translator_logging.info(f"Serializing database model: {type(value).__name__}")
        serialized_model = orm_class_to_dict(value, db_sqlalchemy_merge)
        pyjson_translator_logging.info(f"Serialized db.Model to dict: {serialized_model}")
        return serialized_model
    if isinstance(value, BaseModel):
        pyjson_translator_logging.info(f"Serializing pydantic BaseModel: {type(value).__name__}")
        model_dict = value.model_dump()
        pyjson_translator_logging.info(f"Serialized BaseModel to dict: {model_dict}")
        return model_dict
    if hasattr(value, '__dict__'):
        pyjson_translator_logging.info(f"Serializing using __dict__ for: {type(value).__name__}")
        return {k: serialize_value(v) for k, v in value.__dict__.items()}
    if callable(getattr(value, 'to_dict', None)):
        pyjson_translator_logging.info(f"Serializing using custom method to_dict for: {type(value).__name__}")
        return value.to_dict()
    if callable(getattr(value, 'dict', None)):
        pyjson_translator_logging.info(f"Serializing using custom method dict for: {type(value).__name__}")
        return value.dict()
    if get_origin(value) is Optional:
        pyjson_translator_logging.info(
            f"Encountered an Optional type, deeper serialization might be required for: {value}")
        return serialize_value(value)
    fail_to_translator(f"Unhandled serialize type {type(value).__name__}")


def deserialize_value(value: any,
                      expected_type: type = None,
                      db_sqlalchemy_instance: SQLAlchemy = db,
                      db_sqlalchemy_merge: bool = False):
    if value is None:
        pyjson_translator_logging.info("Deserializing None value.")
        return value
    if expected_type in (int, float, str, bool):
        pyjson_translator_logging.info(f"Deserializing primitive type: {value}")
        return expected_type(value)
    if expected_type == bytes:
        decoded_bytes = base64.b64decode(value.encode('utf-8'))
        pyjson_translator_logging.info(f"Deserialized bytes: {decoded_bytes}")
        return decoded_bytes
    if expected_type == complex:
        complex_value = complex(value['real'], value['imaginary'])
        pyjson_translator_logging.info(f"Deserialized complex number from dict: {complex_value}")
        return complex_value
    if expected_type in (list, tuple):
        pyjson_translator_logging.info(f"Deserializing list or tuple: {value}")
        return [deserialize_value(item, type(item)) for item in value]
    if expected_type == set:
        pyjson_translator_logging.info(f"Deserializing set: {value}")
        return set(deserialize_value(item, type(item)) for item in value)
    if expected_type == dict:
        pyjson_translator_logging.info(f"Deserializing dictionary. Keys: {value.keys()}")
        return {deserialize_value(k, type(k)): deserialize_value(v, type(v)) for k, v in value.items()}
    if expected_type and issubclass(expected_type, db_sqlalchemy_instance.Model):
        pyjson_translator_logging.info(f"Deserializing database model: {expected_type.__name__}")
        model_instance = orm_class_from_dict(expected_type, value, db_sqlalchemy_instance, db_sqlalchemy_merge)
        pyjson_translator_logging.info(f"Deserialized db.Model to instance: {model_instance}")
        return model_instance
    if expected_type and issubclass(expected_type, BaseModel):
        pyjson_translator_logging.info(f"Deserializing pydantic BaseModel: {expected_type.__name__}")
        model_instance = expected_type.model_validate(value)
        pyjson_translator_logging.info(f"Deserialized BaseModel to instance: {model_instance}")
        return model_instance
    if expected_type and hasattr(expected_type, '__dict__'):
        pyjson_translator_logging.info(f"Deserializing using __dict__ for: {expected_type.__name__}")
        constructor_params = expected_type.__init__.__code__.co_varnames[
                             1:expected_type.__init__.__code__.co_argcount]
        if all(param in value for param in constructor_params):
            return expected_type(**{param: value[param] for param in constructor_params})
        else:
            missing_params = [param for param in constructor_params if param not in value]
            fail_to_translator(f"Missing required parameters for initializing "
                               f"'{exception_class.__name__}': {', '.join(missing_params)}")
    if expected_type and callable(getattr(expected_type, 'to_dict', None)):
        pyjson_translator_logging.info(f"Deserializing using custom method to_dict for: {expected_type.__name__}")
        return expected_type.to_dict(value)
    if expected_type and callable(getattr(expected_type, 'dict', None)):
        pyjson_translator_logging.info(f"Deserializing using custom method dict for: {expected_type.__name__}")
        return expected_type.dict(value)
    fail_to_translator(f"Unhandled deserialize type {expected_type.__name__ if expected_type else 'unknown'}")


def fail_to_translator(pyjson_translator_fail_message: str):
    pyjson_translator_logging.warning(pyjson_translator_fail_message)
    raise PyjsonTranslatorException(pyjson_translator_fail_message)


class PyjsonTranslatorException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
