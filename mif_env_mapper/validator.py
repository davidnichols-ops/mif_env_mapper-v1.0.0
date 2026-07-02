"""
Schema Validation Module 
Validates structural correctness against target design parameters.
"""

import logging
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class SchemaValidator:
    """
    Validates structural correctness of data against JSON-like schemas.
    
    Methods:
        validate(instance, schema): Validates data against a schema definition
        validate_with_errors(instance, schema): Returns validation errors list
        check_type(value, expected_type): Type checking helper
    """
    
    @staticmethod
    def check_type(value: Any, expected_type: str) -> bool:
        """
        Check if a value matches the expected JSON schema type.
        
        Args:
            value: The value to check
            expected_type: JSON schema type string
            
        Returns:
            True if value matches expected type
        """
        type_map = {
            "string": str,
            "integer": int,
            "number": (int, float),
            "boolean": bool,
            "array": list,
            "object": dict,
            "null": type(None),
        }
        
        if expected_type not in type_map:
            logger.warning(f"Unknown type in schema: {expected_type}")
            return True  # Allow unknown types (permissive)
        
        expected = type_map[expected_type]
        
        # Special case: bool is subclass of int in Python
        if expected_type == "integer" and isinstance(value, bool):
            return False
            
        return isinstance(value, expected)
    
    @classmethod
    def validate(cls, instance: Dict, schema: Dict) -> bool:
        """
        Validates data structure against a JSON schema definition.
        
        Args:
            instance: Data to validate
            schema: Schema to validate against
            
        Returns:
            True if valid, False otherwise
        """
        errors = cls.validate_with_errors(instance, schema)
        return len(errors) == 0
    
    @classmethod
    def validate_with_errors(cls, instance: Any, schema: Any, path: str = "$") -> List[str]:
        """
        Validates data and returns list of all validation errors.
        
        Args:
            instance: Data to validate
            schema: Schema to validate against
            path: Current JSON path (for error messages)
            
        Returns:
            List of error message strings
        """
        errors: List[str] = []
        
        if not isinstance(schema, dict):
            errors.append(f"{path}: Invalid schema format (expected object)")
            return errors
        
        # Check type
        if "type" in schema:
            if not cls.check_type(instance, schema["type"]):
                expected = schema["type"]
                actual = type(instance).__name__
                errors.append(f"{path}: Expected {expected}, got {actual}")
                return errors  # Type mismatch - no point checking further
        
        # Check required fields for objects
        if schema.get("type") == "object" and isinstance(instance, dict):
            # Check required fields
            for req_field in schema.get("required", []):
                if req_field not in instance:
                    errors.append(f"{path}: Missing required field '{req_field}'")
            
            # Check property types
            if "properties" in schema:
                for prop_key, prop_rules in schema["properties"].items():
                    if prop_key in instance:
                        prop_path = f"{path}.{prop_key}"
                        errors.extend(cls.validate_with_errors(instance[prop_key], prop_rules, prop_path))
            
            # Check additionalProperties (if false, reject unknown keys)
            if schema.get("additionalProperties") is False:
                allowed = set(schema.get("properties", {}).keys())
                for key in instance:
                    if key not in allowed:
                        errors.append(f"{path}: Unknown property '{key}'")
        
        # Check array items
        if schema.get("type") == "array" and isinstance(instance, list):
            if "items" in schema:
                for i, item in enumerate(instance):
                    item_path = f"{path}[{i}]"
                    errors.extend(cls.validate_with_errors(item, schema["items"], item_path))
            
            # Check minItems
            if "minItems" in schema and len(instance) < schema["minItems"]:
                errors.append(f"{path}: Array has {len(instance)} items, minimum is {schema['minItems']}")
            
            # Check maxItems
            if "maxItems" in schema and len(instance) > schema["maxItems"]:
                errors.append(f"{path}: Array has {len(instance)} items, maximum is {schema['maxItems']}")
        
        # Check string constraints
        if schema.get("type") == "string" and isinstance(instance, str):
            if "minLength" in schema and len(instance) < schema["minLength"]:
                errors.append(f"{path}: String length {len(instance)} is less than minimum {schema['minLength']}")
            if "maxLength" in schema and len(instance) > schema["maxLength"]:
                errors.append(f"{path}: String length {len(instance)} exceeds maximum {schema['maxLength']}")
            if "pattern" in schema:
                import re
                if not re.search(schema["pattern"], instance):
                    errors.append(f"{path}: String does not match pattern '{schema['pattern']}'")
        
        # Check enum
        if "enum" in schema and instance not in schema["enum"]:
            errors.append(f"{path}: Value must be one of {schema['enum']}")
        
        return errors
