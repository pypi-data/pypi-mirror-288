import importlib
import inspect
import logging
from abc import ABC, abstractmethod
from typing import (Annotated, Any, Dict, Type, Union, get_args, get_origin,
                    get_type_hints)

import pysnooper
from kaya_module_sdk.src.exceptions.kunimplemented import \
    KayaUnimplementedException
from kaya_module_sdk.src.module.arguments import Args
from kaya_module_sdk.src.module.config import KConfig
from kaya_module_sdk.src.module.returns import Rets
from kaya_module_sdk.src.utils.metadata.abstract_metadata import KMetadata
from kaya_module_sdk.src.utils.metadata.abstract_validation import KValidation
from kaya_module_sdk.src.utils.metadata.display_description import \
    DisplayDescription
from kaya_module_sdk.src.utils.metadata.display_name import DisplayName

log = logging.getLogger(__name__)


class Config(KConfig):
    def __init__(self):
        super().__init__()


class Module(ABC):
    """[ DESCRIPTION ]: Kaya Strategy Module Template.

    [ MANIFEST ]: {
        "moduleName": "string",         -- Name of the module
        "moduleDisplayLabel": "string", -- Display label for this module in the frontend
        "moduleCategory": "enum",       -- Category of the module. An ENUM defined by the NeptuneAPI smithy model.
        "moduleDescription": "string",  -- Description of the module
        "author": "kaya_id(user)",      -- UserID of the User vertex that owns this module.
        "inputs": [{
            "name": "string",           -- Name of the input field in the request object
            "label": "string",          -- Display label for this input in the frontend
            "type": "kaya_id(value)",   -- VertexID of the value that represents this input datatype
            "description": "string",    -- Description of the INPUT
            "validations": [
                "validation_pattern"    -- An array of validation queries to run against the inputs.
            ]}
        ],
        "outputs": [{
            "name": "string",           -- Name of the output field in the returned structure
            "label": "string",          -- Display label for this output in the frontend
            "type": "kaya_id(value)",   -- VertexID of the value that represents this output datatype
            "description": "string"     -- Description of the output
            "validations": [
                "validation_pattern"    -- An array of validation queries to run against the inputs.
            ]}
        ]
    }
    """

    config: KConfig
    subclasses: list = []
    modules: dict = {}
    _manifest: dict = {}
    _recompute_manifest: bool = True

    def __init__(self) -> None:
        self.config = Config()
        self.import_subclasses()
        self.modules = {item.__class__.__name__: item for item in self.subclasses}

    #   @pysnooper.snoop()
    def import_subclasses(self) -> list:
        module_name = self.__module__
        package = importlib.import_module(module_name).__package__
        if not package:
            return self.subclasses
        try:
            module = importlib.import_module(f"{package}.module")
        except Exception as e:
            return self.subclasses
        for cls_name, obj in inspect.getmembers(module):
            if (
                inspect.isclass(obj)
                and issubclass(obj, Module)
                and obj not in [Module, Args, Rets, KConfig, KMetadata, KValidation]
                and cls_name != "KayaStrategyModule"
            ):
                subclass_instance = obj()
                self.subclasses.append(subclass_instance)
        return self.subclasses

    #   @pysnooper.snoop()
    def _extract_manifest(self) -> Dict[str, Any]:
        main_method = self.main
        type_hints = get_type_hints(main_method)
        args_hints = {
            param: type_hint
            for param, type_hint in type_hints.items()
            if param != "return"
        }
        return_hint = type_hints.get("return", None)
        signature = inspect.signature(main_method)
        params_metadata = {}
        for param_name, param in signature.parameters.items():
            expected_type = args_hints.get(param_name, "Any")
            params_metadata[param_name] = {
                "expected_type": expected_type,
                "annotation": param.annotation,
                "details": self._get_class_metadata(expected_type)
                if inspect.isclass(expected_type)
                else None,
            }
        return_metadata = {
            "expected_type": return_hint,
            "annotation": signature.return_annotation,
            "details": self._get_class_metadata(return_hint)
            if inspect.isclass(return_hint)
            else None,
        }
        metadata = {
            "moduleName": self.config.name,
            "moduleDisplayLabel": self.config.display_label,
            "moduleCategory": self.config.category,
            "moduleDescription": self.config.description,
            "author": self.config.author,
            "inputs": [],
            "outputs": [],
        }
        metadata["inputs"] += self._extract_metadata(params_metadata["args"]["details"])
        metadata["outputs"] += self._extract_metadata(return_metadata["details"])
        return metadata

    #   @pysnooper.snoop()
    def _extract_metadata(self, details: dict) -> list:
        metadata = []
        if not details:
            return metadata
        for detail in details:
            unpacked = self._unpack_annotated(details[detail]["type"])
            record = {
                "name": detail,
                "label": detail,
                "type": str(unpacked[0]).split("'")[1],
                "description": None,
                "validations": [],
            }
            for item in unpacked[1]:
                if not isinstance(item, KMetadata):
                    continue
                segmented = str(item).split(":")
                if isinstance(item, DisplayName):
                    record["label"] = segmented[1]
                elif isinstance(item, DisplayDescription):
                    record["description"] = segmented[1]
                elif isinstance(item, KValidation):
                    record["validations"].append(str(item))
            metadata.append(record)
        return metadata

    #   @pysnooper.snoop()
    def _unpack_annotated(self, annotated_type):
        # Check if the type is an Annotated type
        if get_origin(annotated_type) is Annotated:
            base_type, *metadata = get_args(annotated_type)
            # Check if the base type is another Annotated type
            if get_origin(base_type) is Annotated:
                return self._unpack_annotated(base_type)
            return base_type, metadata
        # If the type is a list, we need to unpack its inner type
        elif get_origin(annotated_type) is list:
            inner_type = get_args(annotated_type)[0]
            return self._unpack_annotated(inner_type)
        return annotated_type, []

    #   @pysnooper.snoop()
    def _get_class_metadata(self, cls: Type) -> Dict[str, Any]:
        """Recursively fetch the metadata for class attributes with type
        annotations."""
        if not hasattr(cls, "__annotations__"):
            return {}
        class_metadata = {}
        for attr_name, attr_type in cls.__annotations__.items():
            class_metadata[attr_name] = {
                "type": attr_type,
                "details": self._get_class_metadata(attr_type)
                if inspect.isclass(attr_type)
                else None,
            }
        return class_metadata

    @property
    def manifest(self) -> dict:
        """
        [ RETURN ]: {
            "moduleName": "string",
            "moduleDisplayLabel": "string",
            "moduleCategory": "enum",
            "moduleDescription": "string",
            "author": "kaya_id(user)",
            "inputs": [
                {
                "name": "string",
                "label": "string",
                "type": "kaya_id(value)",
                "description": "string",
                "validations": [
                    "validation_pattern"
                ]
                }
            ],
            "outputs": [
                {
                "name": "string",
                "label": "string",
                "type": "kaya_id(value)",
                "description": "string"
                }
            ]
        }
        """
        if self._manifest and not self._recompute_manifest:
            return self._manifest
        self._manifest = self._extract_manifest()
        return self._manifest

    @abstractmethod
    def main(self, args: Args) -> Rets:
        pass


# CODE DUMP

#   def main_batch(self, args: Args) -> Rets:
#       return KayaUnimplementedException('Unimplemented method!')

#       for arg in params_metadata['args']['details']:
#           unpacked = self.unpack_annotated(params_metadata['args']['details'][arg]['type'])
#           print(f'[ DEBUG ]: unpacked ({arg}) - ', unpacked)
#           input_metadata = {
#               'name': arg,
#               'label': arg,
#               'type': unpacked[0],
#               'description': None,
#               'validations': [],
#           }
#           for item in unpacked[1]:
#               if not isinstance(item, KMetadata):
#                   continue
#               meta_unpacked = get_type_hints(item, include_extras=True)
#               segmented = str(item).split(':')
#               if isinstance(item, DisplayName):
#                   input_metadata['label'] = segmented[1]
#               if isinstance(item, KValidation):
#                   input_metadata['validations'].append(item)
#           metadata['inputs'].append(input_metadata)


#       for ret in return_metadata['details']:
#           unpacked = self.unpack_annotated(return_metadata['details'][ret]['type'])
#           output_metadata = {
#               'name': ret,
#               'label': ret,
#               'type': unpacked[0],
#               'description': None,
#               'validations': []
#           }
#           for item in unpacked[1]:
#               if not isinstance(item, KMetadata):
#                   continue
#               segmented = str(item).split(':')
#               if isinstance(item, DisplayName):
#                   output_metadata['label'] = segmented[1]
#               elif isinstance(item, KValidation):
#                   output_metadata['validations'].append(str(item))

#           metadata['outputs'].append(output_metadata)


#   import abc
#   import inspect
#   from typing import get_type_hints, Any, Dict, Type, Union

#   class TypeChecked(abc.ABC):
#       @abc.abstractmethod
#       def main(self) -> Any:
#           """
#           Abstract method that child classes must implement.
#           """
#           pass

#       def metadata(self) -> Dict[str, Any]:
#           """
#           Checks the type annotations of the 'main' method and its argument and return value classes, and returns metadata.
#           """
#           # Get the 'main' method of the current instance
#           main_method = self.main

#           # Get the type hints for the 'main' method
#           type_hints = get_type_hints(main_method)

#           # Extract arguments and return type from the type hints
#           args_hints = {param: type_hint for param, type_hint in type_hints.items() if param != 'return'}
#           return_hint = type_hints.get('return', None)

#           # Inspect the 'main' method signature
#           signature = inspect.signature(main_method)

#           # Get parameter names and their types
#           params_metadata = {}
#           for param_name, param in signature.parameters.items():
#               expected_type = args_hints.get(param_name, 'Any')
#               params_metadata[param_name] = {
#                   'expected_type': expected_type,
#                   'annotation': param.annotation,
#                   'details': self._get_class_metadata(expected_type) if inspect.isclass(expected_type) else None
#               }

#           # Get return type
#           return_metadata = {
#               'expected_type': return_hint,
#               'annotation': signature.return_annotation,
#               'details': self._get_class_metadata(return_hint) if inspect.isclass(return_hint) else None
#           }

#           # Generate the metadata dictionary
#           metadata = {
#               'parameters': params_metadata,
#               'return': return_metadata
#           }

#           # Validate types if possible
#           self._validate_types(metadata)

#           return metadata

#       def _validate_types(self, metadata: Dict[str, Any]) -> None:
#           """
#           Validate the types of parameters and return value.
#           """
#           for param_name, param_data in metadata['parameters'].items():
#               if param_data['annotation'] != inspect.Parameter.empty:
#                   if not self._is_valid_type(param_data['annotation'], param_data['expected_type']):
#                       raise TypeError(f"Parameter '{param_name}' has type '{param_data['annotation']}' but expected type '{param_data['expected_type']}'")

#           if metadata['return']['annotation'] != inspect.Signature.empty:
#               if not self._is_valid_type(metadata['return']['annotation'], metadata['return']['expected_type']):
#                   raise TypeError(f"Return value has type '{metadata['return']['annotation']}' but expected type '{metadata['return']['expected_type']}'")

#       def _is_valid_type(self, actual: Any, expected: Any) -> bool:
#           """
#           Check if the actual type matches the expected type, including custom classes.
#           """
#           if expected == Any:
#               return True
#           if isinstance(expected, type):
#               return issubclass(actual, expected)
#           return actual == expected

#       def _get_class_metadata(self, cls: Type) -> Dict[str, Any]:
#           """
#           Recursively fetch the metadata for class attributes with type annotations.
#           """
#           if not hasattr(cls, '__annotations__'):
#               return {}

#           class_metadata = {}
#           for attr_name, attr_type in cls.__annotations__.items():
#               class_metadata[attr_name] = {
#                   'type': attr_type,
#                   'details': self._get_class_metadata(attr_type) if inspect.isclass(attr_type) else None
#               }
#           return class_metadata

#   # Custom class example
#   class DummyArgs:
#       a: int
#       b: str

#   class DummyRets:
#       c: float
#       d: DummyArgs

#   # Example of a child class
#   class MyClass(TypeChecked):
#       def main(self, args: DummyArgs) -> DummyRets:
#           return DummyRets(c=1.0, d=args)

#   # Example usage
#   if __name__ == "__main__":
#       instance = MyClass()
#       metadata = instance.metadata()
#       print(json.dumps(metadata, indent=4, default=str))


#   import abc
#   import inspect
#   from typing import get_type_hints, Any, Dict, Type, Union

#   class TypeChecked(abc.ABC):
#       @abc.abstractmethod
#       def main(self) -> Any:
#           """
#           Abstract method that child classes must implement.
#           """
#           pass

#       def metadata(self) -> Dict[str, Any]:
#           """
#           Checks the type annotations of the 'main' method and returns metadata.
#           """
#           # Get the 'main' method of the current instance
#           main_method = self.main

#           # Get the type hints for the 'main' method
#           type_hints = get_type_hints(main_method)

#           # Extract arguments and return type from the type hints
#           args_hints = {param: type_hint for param, type_hint in type_hints.items() if param != 'return'}
#           return_hint = type_hints.get('return', None)

#           # Inspect the 'main' method signature
#           signature = inspect.signature(main_method)

#           # Get parameter names and their types
#           params_metadata = {}
#           for param_name, param in signature.parameters.items():
#               expected_type = args_hints.get(param_name, 'Any')
#               params_metadata[param_name] = {
#                   'expected_type': expected_type,
#                   'annotation': param.annotation
#               }

#           # Get return type
#           return_metadata = {
#               'expected_type': return_hint,
#               'annotation': signature.return_annotation
#           }

#           # Generate the metadata dictionary
#           metadata = {
#               'parameters': params_metadata,
#               'return': return_metadata
#           }

#           # Validate types if possible
#           self._validate_types(metadata)

#           return metadata

#       def _validate_types(self, metadata: Dict[str, Any]) -> None:
#           """
#           Validate the types of parameters and return value.
#           """
#           for param_name, param_data in metadata['parameters'].items():
#               if param_data['annotation'] != inspect.Parameter.empty:
#                   if not self._is_valid_type(param_data['annotation'], param_data['expected_type']):
#                       raise TypeError(f"Parameter '{param_name}' has type '{param_data['annotation']}' but expected type '{param_data['expected_type']}'")

#           if metadata['return']['annotation'] != inspect.Signature.empty:
#               if not self._is_valid_type(metadata['return']['annotation'], metadata['return']['expected_type']):
#                   raise TypeError(f"Return value has type '{metadata['return']['annotation']}' but expected type '{metadata['return']['expected_type']}'")

#       def _is_valid_type(self, actual: Any, expected: Any) -> bool:
#           """
#           Check if the actual type matches the expected type, including custom classes.
#           """
#           if expected == Any:
#               return True
#           if isinstance(expected, type):
#               return issubclass(actual, expected)
#           return actual == expected

#   # Custom class example
#   class CustomClass:
#       pass

#   # Example of a child class
#   class MyClass(TypeChecked):
#       def main(self, x: int, y: CustomClass) -> CustomClass:
#           return y

#   # Example usage
#   if __name__ == "__main__":
#       instance = MyClass()
#       metadata = instance.metadata()
#       print(json.dumps(metadata, indent=4))
