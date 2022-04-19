# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Denis Shipilov <shipilovds@gmail.com>
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from gi.repository import Gio, GLib
import re


class ValueProcessor():
    '''Class with static methods that helps to convert string (that looks like a tuple) to tuple.

    The reason of such strange action is simple:
    Ansible (yaml) does not support tuple in comfortable way of usage.
    It creates some severities, so I decided to make it simple.
    '''

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
                # try to find tuple presented as string
                new_item = ValueProcessor.process_string(item)
            else:
                new_item = item
            new_list.append(new_item)

        return new_list

    @staticmethod
    def process_string(obj):
        '''This method detects whether the input object is a string or a tuple.

        Whith this ansible module we can detect strings like this:
        ```('xkb', 'us')``` as a tuple. This method helps us to do so.
        Also it helps to detect int in string (ansible module args makes string from int)

        Args:
            obj (str): Sting which might be a tuple or int

        Returns:
            (int), (str) or (tuple): Depending on detected type
        '''
        if obj.isdigit():
            return int(obj)
        find = re.findall(r'\(\'([a-z]+)\'\,\s?\'([a-z]+)\'\)', obj)
        if len(find) == 1 and isinstance(find[0], tuple):
            return find[0]
        else:
            return obj

    @staticmethod
    def process_unknown(obj):
        '''Method that helps to determine the actual value type.

        Sometimes values like this: ```('xkb', 'us')``` actually is a tuple
        So we need to determine the actual value type for the strings.
        For the lists we need to determine each item inside.

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

    @staticmethod
    def get_variant_list(value):
        '''Creates list GLib.Variant and GLib.VariantType objects from value.

        Values inside the list will also be processed (depending on their type) by the corresponding functions.
        Result - GLib.Variant with 'list' type, with GLib.Variant items inside.

        Args:
            value (list): List value we need to process with each inner value

        Returns:
            GLib.VariantType
            GLib.Variant
        '''
        variants_list = []
        result_type = None
        for item in value:
            result_type, item_variant = GVariant.get_variant(item)
            variants_list.append(item_variant)
        result_value = GLib.Variant.new_array(result_type, variants_list)
        return result_type, result_value

    @staticmethod
    def get_variant_tuple(value):
        '''Creates tuple GLib.Variant and GLib.VariantType objects from value.

        Values inside the tuple will also be processed (depending on their type) by the corresponding functions.
        Result - GLib.Variant with 'tuple' type, with GLib.Variant items inside.

        Args:
            value (tuple): Tuple value we need to process

        Returns:
            GLib.VariantType
            GLib.Variant
        '''
        types_list = []
        variants_list = []
        for item in value:
            item_type, item_variant = GVariant.get_variant(item)
            types_list.append(item_type)
            variants_list.append(item_variant)
        result_type = GLib.VariantType.new_tuple(types_list)
        result_value = GLib.Variant.new_tuple(*variants_list)
        return result_type, result_value

    @staticmethod
    def get_variant_int(value):
        '''Creates integer GLib.Variant and GLib.VariantType objects from value.

        Args:
            value (int): Integer value we need to process

        Returns:
            GLib.VariantType
            GLib.Variant
        '''
        result_type = GLib.VariantType.new('i')
        result_value = GLib.Variant.new_int32(value)
        return result_type, result_value

    @staticmethod
    def get_variant_str(value):
        '''Creates string GLib.Variant and GLib.VariantType objects from value.

        Args:
            value (str): String value we need to process

        Returns:
            GLib.VariantType
            GLib.Variant
        '''
        result_type = GLib.VariantType.new('s')
        result_value = GLib.Variant.new_string(value)
        return result_type, result_value

    @staticmethod
    def get_variant_boolean(value):
        '''Creates boolean GLib.Variant and GLib.VariantType objects from value.

        Args:
            value (bool): Boolean value we need to process

        Returns:
            GLib.VariantType
            GLib.Variant
        '''
        result_type = GLib.VariantType.new('b')
        result_value = GLib.Variant.new_boolean(value)
        return result_type, result_value

    @staticmethod
    def get_variant(value):
        '''Creates GLib.Variant and GLib.VariantType objects from value.

        Args:
            value: Accepts any value type (almost).

        Raises:
            ValueException: If value type is not supported by method logic.

        Returns:
            GLib.VariantType
            GLib.Variant
        '''
        if isinstance(value, list):
            result_type, result_value = GVariant.get_variant_list(value)
        elif isinstance(value, bool):
            result_type, result_value = GVariant.get_variant_boolean(value)
        elif isinstance(value, int):
            result_type, result_value = GVariant.get_variant_int(value)
        elif isinstance(value, str):
            result_type, result_value = GVariant.get_variant_str(value)
        elif isinstance(value, tuple):
            result_type, result_value = GVariant.get_variant_tuple(value)
        else:
            raise ValueException('Unsupported value type: {}'.format(type(value)))

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
    '''
    def __init__(self, schema_id, schema_path, schema_key):
        self.schema_id = schema_id
        self.schema_path = self._validate_schema_path(schema_path)
        self.schema_key = schema_key
        self._schema_obj = self._obtain_gio_settings_schema()
        self._settings_obj = self._obtain_gio_settings()

    def _validate_schema_path(self, schema_path):
        if schema_path is None:
            return None
        match = re.match(r'(\/[a-z]+)+\/', schema_path)
        if match is None:
            raise SchemaException('Schema path \'{}\' is incorrect.{}'.format(schema_path, match))
        else:
            return schema_path

    def _obtain_gio_settings_schema(self):
        '''Method to get Gsettings schema object

        Raises:
            SchemaException: If Gsettings schema does not exist.
        '''
        source = Gio.SettingsSchemaSource.get_default()
        schema_obj = source.lookup(self.schema_id, False)
        if schema_obj is None:
            raise SchemaException('Schema \'{}\' does not exist'.format(self.schema_id))
        if not schema_obj.has_key(self.schema_key):
            raise SchemaException('Key \'{}\' does not exist'.format(self.schema_key))

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
        variant_type, variant_value = GVariant.get_variant(new_value)
        changed = self._settings_obj.set_value(self.schema_key, variant_value)
        if changed:
            self._settings_obj.sync()
            self._settings_obj.apply()
        else:
            raise ValueException('Cannot change value! Check possible values or value type. qwe_new: {} qwe_type: {}'.format(new_value, variant_value.dup_string()))
