# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Denis Shipilov <shipilovds@gmail.com>
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from gi.repository import Gio, GLib
import re


class ValueProcessor():
    '''Class with static methods that helps to convert string object to the type they are really belong to.

    The reason of such strange action is simple:
    Ansible (yaml) does not support tuple in comfortable way of usage.
    Also it doesn't support float type. And sometimes `'true'` really means `True`.
    It creates some troubles, so I decided to make it simple.
    '''

    @classmethod
    def is_float(cls, obj):
        try:
            float(obj)
            return True
        except Exception:
            return False

    @classmethod
    def is_int(cls, obj):
        return obj.isdigit()

    @classmethod
    def is_bool(cls, obj):
        return obj.lower() in ('true', 'false')

    @classmethod
    def to_bool(cls, string):
        if string.lower() == 'true':
            return True
        elif string.lower() == 'false':
            return False

    @staticmethod
    def process_string(obj):
        '''This method helps to find out if there is another type hidden in the string.

        Whith this ansible module we can detect strings like this:
        ```('xkb', 'us')``` as a tuple. This method helps us to do so.
        Also it helps to detect int, float or boolean represented as string (ansible module args makes string from them)

        Args:
            obj (str): Sting which might be a tuple or int

        Returns:
            (int/float/bool/tuple/str): Depending on detected type
        '''
        if ValueProcessor.is_int(obj):
            return int(obj)
        if ValueProcessor.is_float(obj):
            return float(obj)
        if ValueProcessor.is_bool(obj):
            return ValueProcessor.to_bool(obj)
        # let's find out if it is a tuple
        # (it is always only 2 items inside the tuple here. so we will try to find them.)
        find = re.fullmatch(r'\(\'?([a-z0-9.]+)\'?\,\s?\'?([a-z0-9.]+)\'?\)', obj)
        if find is not None:
            return (ValueProcessor.process_string(find.group(1)), ValueProcessor.process_string(find.group(2)))
        else:
            return obj

    @staticmethod
    def process_list(obj):
        '''This method helps us to detect the type of items in the list and place there the correct ones.

        Args:
            obj (list): List with undetected items

        Returns:
            list: Might contain tuples or any other types
        '''
        new_list = []
        for item in obj:
            if isinstance(item, str):
                # try to find another type presented as string
                new_item = ValueProcessor.process_string(item)
            else:
                new_item = item
            new_list.append(new_item)

        return new_list

    @staticmethod
    def process_unknown(obj):
        '''Method that helps to determine the actual value type.

        String is not always a string. We are going to process it.
        For the lists we need to determine each item inside.
        For any other type we do nothing.

        Args:
            obj: Might be a list or eny other possible type

        Returns:
            Might be a list or tuple or eny other possible type
        '''
        if isinstance(obj, list):
            new_obj = ValueProcessor.process_list(obj)
        elif isinstance(obj, str):
            new_obj = ValueProcessor.process_string(obj)
        else:
            new_obj = obj

        return new_obj


class GVariant():
    '''Class with static methods that helps to produce GLib.Variant

    Main method that uses the others - `get_variant`
    '''

    VARIANTS = {
        'G_VARIANT_TYPE_BOOLEAN': {'typestring': 'b', 'classname': 'bool'},
        'G_VARIANT_TYPE_INT32':   {'typestring': 'i', 'classname': 'int'},
        'G_VARIANT_TYPE_STRING':  {'typestring': 's', 'classname': 'str'},
        'G_VARIANT_TYPE_TUPLE':   {'typestring': 'r', 'classname': 'tuple'},
        'G_VARIANT_TYPE_ARRAY':   {'typestring': 'a', 'classname': 'list'},
        'G_VARIANT_TYPE_DOUBLE':  {'typestring': 'd', 'classname': 'float'},
    }

    @staticmethod
    def get_variant_list(value, value_type_string):
        '''Creates list GLib.Variant and GLib.VariantType objects from value.

        Values inside the list will also be processed (depending on their type) by the corresponding functions.
        Result - GLib.Variant with 'list' type, with GLib.Variant items inside.

        Args:
            value (list): List value we need to process with each inner value
            value_type_string (str): GLib.Variant type string

        Returns:
            GLib.VariantType
            GLib.Variant
        '''
        variants_list = []
        result_type = GLib.VariantType.new(value_type_string)
        child_value_type_string = value_type_string[1:]
        child_type = GLib.VariantType.new(child_value_type_string)
        for item in value:
            _, item_variant = GVariant.get_variant(item, child_value_type_string)
            variants_list.append(item_variant)
        result_value = GLib.Variant.new_array(child_type, variants_list)
        return result_type, result_value

    @staticmethod
    def get_variant_tuple(value, value_type_string):
        '''Creates tuple GLib.Variant and GLib.VariantType objects from value.

        Values inside the tuple will also be processed (depending on their type) by the corresponding functions.
        Result - GLib.Variant with 'tuple' type, with GLib.Variant items inside.

        Args:
            value (tuple): Tuple value we need to process
            value_type_string (str): GLib.Variant type string

        Returns:
            GLib.VariantType
            GLib.Variant
        '''
        types_list = []
        variants_list = []
        child_value_type_string = value_type_string[1:]
        for index, item in enumerate(value):
            item_type, item_variant = GVariant.get_variant(item, child_value_type_string[index])
            types_list.append(item_type)
            variants_list.append(item_variant)
        result_type = GLib.VariantType.new_tuple(types_list)
        result_value = GLib.Variant.new_tuple(*variants_list)
        return result_type, result_value

    @staticmethod
    def get_variant_by_type(value, value_type):
        '''Creates GLib.Variant and GLib.VariantType objects from value and value type

        Value types are defined in `GVariant.VARIANTS` (Class manifest constant)
        More info about it: https://lazka.github.io/pgi-docs/GLib-2.0/classes/VariantType.html#GLib.VariantType

        Args:
            value: Value we need to process
            value_type (str): GLib.Variant type string

        Raises:
            ValueException: If provided value type doesn't match with the expected type.

        Returns:
            GLib.VariantType
            GLib.Variant
        '''
        provided_type = type(value).__name__
        expected_type = GVariant.VARIANTS[value_type]['classname']
        if provided_type != expected_type:
            # if provided_type == 'dict' and expected_type == 'str':  # I saw such cases, so let it be...
            #     value = str(value)
            #     # TODO: I can't finish this processing right now. It needs more time.
            # else:
            raise ValueException(f'Provided value type ({provided_type}) does not match with expected type ({expected_type})')

        result_type = GLib.VariantType.new(GVariant.VARIANTS[value_type]['typestring'])

        if expected_type == 'bool':
            result_value = GLib.Variant.new_boolean(value)
        elif expected_type == 'int':
            result_value = GLib.Variant.new_int32(value)
        elif expected_type == 'float':
            result_value = GLib.Variant.new_double(value)
        elif expected_type == 'str':
            result_value = GLib.Variant.new_string(value)
        return result_type, result_value

    @staticmethod
    def get_simple_variant(value, value_type_string):
        '''Creates GLib.Variant and GLib.VariantType objects from value and type string

        Value type depends on `value_type_string`

        Args:
            value: Value we need to process
            value_type_string (str): GLib.Variant type string

        Raises:
            ValueException: If value type is not supported by method logic.

        Returns:
            GLib.VariantType
            GLib.Variant
        '''
        provided_type = type(value).__name__
        for data_type in GVariant.VARIANTS:
            if GVariant.VARIANTS[data_type]['typestring'] == value_type_string:
                return GVariant.get_variant_by_type(value, data_type)

        # raise error if cannot find supported type string
        raise ValueException(f'Unsupported value type. Given value: {value} Given value type: {provided_type} Expected type string: {value_type_string}')

    @staticmethod
    def get_complex_variant(value, value_type_string):
        '''Helps to get GLib.Variant and GLib.VariantType for complex data types.

        Args:
            value (list/tuple): Accepts value of any type (almost).
            value_type_string (str): GLib.Variant type string

        Raises:
            ValueException: If value type is not supported by method logic.

        Returns:
            GLib.VariantType
            GLib.Variant
        '''
        provided_type = type(value).__name__
        if provided_type == 'list':
            result_type, result_value = GVariant.get_variant_list(value, value_type_string)
        elif provided_type == 'tuple':
            result_type, result_value = GVariant.get_variant_tuple(value, value_type_string)
        else:
            raise ValueException(f'Unsupported value type. Given value: {value} Given value type: {provided_type} Expected type string: {value_type_string}')

        return result_type, result_value

    @staticmethod
    def get_variant(value, value_type_string):
        '''Creates GLib.Variant and GLib.VariantType objects from value.

        Uses correcponding functions to process simple and complex data types

        Args:
            value: Accepts value of any type (almost).
            value_type_string (str): GLib.Variant type string

        Returns:
            GLib.VariantType
            GLib.Variant
        '''
        if len(value_type_string) > 1:
            result_type, result_value = GVariant.get_complex_variant(value, value_type_string)
        else:
            result_type, result_value = GVariant.get_simple_variant(value, value_type_string)

        return result_type, result_value


class SchemaException(Exception):
    '''Custom exception for schema troubles'''
    pass


class ValueException(Exception):
    '''Custom exception for value troubles'''
    pass


class GsettingsWrapper():
    '''Class that helps to operate with Gsettings

    Args:
        schema_id (str): The ID of the schema
        schema_path (str): Schema path
        schema_key (str): Schema key to get the value for

    Attributes:
        schema_id (str): The ID of the schema
        schema_path (str): Schema path
        schema_key (str): Schema key to get the value for
        value (GLib.Variant): Schema value for `schema_key`
    '''
    def __init__(self, schema_id, schema_path, schema_key):
        self.schema_id = schema_id
        self.schema_path = self._validate_schema_path(schema_path)
        self.schema_key = schema_key
        self._schema_obj = self._obtain_gio_settings_schema()
        self._settings_obj = self._obtain_gio_settings()
        self.value = self.read()

    def _validate_schema_path(self, schema_path):
        '''Method to validate schemas path

        Raises:
            SchemaException: If schema path is incorrect
        '''
        if schema_path is None:
            return None
        if re.match(r'(\/[a-z]+)+\/', schema_path) is None:
            raise SchemaException(f'Schema path \'{schema_path}\' is incorrect.')
        else:
            return schema_path

    def _obtain_gio_settings_schema(self):
        '''Method to get Gsettings schema object

        Raises:
            SchemaException: If Gsettings schema or schema key does not exist.
        '''
        source = Gio.SettingsSchemaSource.get_default()
        schema_obj = source.lookup(self.schema_id, False)
        if schema_obj is None:
            raise SchemaException(f'Schema \'{self.schema_id}\' does not exist')
        if not schema_obj.has_key(self.schema_key):
            raise SchemaException(f'Key \'{self.schema_key}\' does not exist')

        return schema_obj

    def _obtain_gio_settings(self):
        '''Method to get Gsettings object'''
        backend = Gio.SettingsBackend.get_default()
        return Gio.Settings.new_full(self._schema_obj, backend, self.schema_path)

    def read(self):
        '''Read value from Gsettings key.

        Gets GLib.Variant from Gio.Settings.
        You can decompose it into a native Python object with `unpack()` method.

        Returns:
            GLib.Variant
        '''
        return self._settings_obj.get_value(self.schema_key)

    def write(self, schema_value):
        '''Writes value for Gsettings key.

        Args:
            schema_value (str): gsettings value

        Raises:
            ValueException: If schema value is not writable or cannot be changed.
        '''
        if not self._settings_obj.is_writable(self.schema_key):
            raise ValueException('Value cannot be changed because it is not writable!')
        new_value = ValueProcessor.process_unknown(schema_value)
        value_type_string = self.value.get_type_string()
        variant_type, variant_value = GVariant.get_variant(new_value, value_type_string)
        changed = self._settings_obj.set_value(self.schema_key, variant_value)
        if changed:
            self._settings_obj.sync()
            self._settings_obj.apply()
            self.value = variant_value
        else:
            raise ValueException(f'Cannot change value! Check possible values or value type. Value: {new_value} Variant type: {variant_value.dup_string()}')
