# Copyright 2016-2017 Esteve Fernandez <esteve@apache.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import pathlib

from pathlib import Path

if os.environ['ROS_DISTRO'] <= 'humble':
    import rosidl_cmake as rosidl_pycommon
else:
    import rosidl_pycommon

from rosidl_parser.definition import AbstractGenericString
from rosidl_parser.definition import AbstractNestedType
from rosidl_parser.definition import AbstractSequence
from rosidl_parser.definition import AbstractString
from rosidl_parser.definition import AbstractWString
from rosidl_parser.definition import Action
from rosidl_parser.definition import Array
from rosidl_parser.definition import BasicType
from rosidl_parser.definition import BoundedSequence
from rosidl_parser.definition import BoundedString
from rosidl_parser.definition import BoundedWString
from rosidl_parser.definition import IdlContent
from rosidl_parser.definition import IdlLocator
from rosidl_parser.definition import Message
from rosidl_parser.definition import NamespacedType
from rosidl_parser.definition import Service
from rosidl_parser.definition import UnboundedSequence
from rosidl_parser.definition import UnboundedString
from rosidl_parser.definition import UnboundedWString

from rosidl_parser.parser import parse_idl_file

import sys

# Workaround for RHEL 8 which ships Python 3.6 that lacks str.removesuffix()
# (added in Python 3.9, PEP 616). On Python 3.9+, the native implementation
# is used.
# TODO(esteve): Remove this workaround when RHEL 8 is no longer supported.
if sys.version_info >= (3, 9):
    def _removesuffix(s, suffix):
        return s.removesuffix(suffix)
else:
    def _removesuffix(s, suffix):
        return s[:-len(suffix)] if suffix and s.endswith(suffix) else s

package_name = ""

# Taken from http://stackoverflow.com/a/6425628
def convert_lower_case_underscore_to_camel_case(word):
    return ''.join(x.capitalize() or '_' for x in word.split('_'))


def generate_rs(generator_arguments_file, typesupport_impls):
    args = rosidl_pycommon.read_generator_arguments(generator_arguments_file)

    global package_name
    package_name = args['package_name']

    # expand init modules for each directory
    modules = {}
    idl_content = IdlContent()
    dependency_packages = set()

    (Path(args['output_dir']) / 'rust/src').mkdir(parents=True, exist_ok=True)

    for dep_tuple in args.get('ros_interface_dependencies', []):
        dep_parts = dep_tuple.split(':', 1)
        assert len(dep_parts) == 2
        if dep_parts[0] != package_name:
            dependency_packages.add(dep_parts[0])

    for idl_tuple in args.get('idl_tuples', []):
        idl_parts = idl_tuple.rsplit(':', 1)
        assert len(idl_parts) == 2

        idl_rel_path = pathlib.Path(idl_parts[1])
        idl_stems = modules.setdefault(str(idl_rel_path.parent), set())
        idl_stems.add(idl_rel_path.stem)

        locator = IdlLocator(*idl_parts)
        idl_file = parse_idl_file(locator)
        idl_content.elements += idl_file.content.elements

    typesupport_impls = typesupport_impls.split(';')

    template_dir = args['template_dir']

    mapping_msgs = {
        os.path.join(template_dir, 'msg.rs.em'): ['rust/src/%s'],
        os.path.join(template_dir, 'msg/rmw.rs.em'): ['rust/src/msg/%s'],
    }

    mapping_srvs = {
        os.path.join(template_dir, 'srv.rs.em'): ['rust/src/%s'],
        os.path.join(template_dir, 'srv/rmw.rs.em'): ['rust/src/srv/%s'],
    }

    mapping_actions = {
        os.path.join(template_dir, 'action.rs.em'): ['rust/src/%s'],
        os.path.join(template_dir, 'action/rmw.rs.em'): ['rust/src/action/%s'],
    }

    # Ensure the required templates exist
    for template_file in mapping_msgs.keys():
        assert os.path.exists(template_file), \
            'Messages template file %s not found' % template_file
    for template_file in mapping_srvs.keys():
        assert os.path.exists(template_file), \
            'Services template file %s not found' % template_file
    for template_file in mapping_actions.keys():
        assert os.path.exists(template_file), \
            'Actions template file %s not found' % template_file

    data = {
        'pre_field_serde': pre_field_serde,
        'get_rs_name': get_rs_name,
        'make_get_rs_type': make_get_rs_type,
        'constant_value_to_rs': constant_value_to_rs,
        'value_to_rs': value_to_rs,
        'convert_camel_case_to_lower_case_underscore':
        rosidl_pycommon.convert_camel_case_to_lower_case_underscore,
        'convert_lower_case_underscore_to_camel_case':
        convert_lower_case_underscore_to_camel_case,
        'msg_specs': [],
        'srv_specs': [],
        'action_specs': [],
        'package_name': package_name,
        'typesupport_impls': typesupport_impls,
        'interface_path': idl_rel_path,
    }

    latest_target_timestamp = rosidl_pycommon.get_newest_modification_time(
        args['target_dependencies'])

    for message in idl_content.get_elements_of_type(Message):
        data['msg_specs'].append(('msg', message))

    for service in idl_content.get_elements_of_type(Service):
        data['srv_specs'].append(('srv', service))

    for action in idl_content.get_elements_of_type(Action):
        data['action_specs'].append(('action', action))

    if data['msg_specs']:
        for template_file, generated_filenames in mapping_msgs.items():
            stem = _removesuffix(Path(template_file).stem, ".em")

            for generated_filename in generated_filenames:
                generated_file = os.path.join(args['output_dir'],
                                              generated_filename % stem)
                rosidl_pycommon.expand_template(
                    os.path.join(template_dir, template_file),
                    data.copy(),
                    generated_file,
                    minimum_timestamp=latest_target_timestamp)

    if data['srv_specs']:
        for template_file, generated_filenames in mapping_srvs.items():
            stem = _removesuffix(Path(template_file).stem, ".em")

            for generated_filename in generated_filenames:
                generated_file = os.path.join(args['output_dir'],
                                              generated_filename % stem)
                rosidl_pycommon.expand_template(
                    os.path.join(template_dir, template_file),
                    data.copy(),
                    generated_file,
                    minimum_timestamp=latest_target_timestamp)

    if data['action_specs']:
        for template_file, generated_filenames in mapping_actions.items():
            stem = _removesuffix(Path(template_file).stem, ".em")

            for generated_filename in generated_filenames:
                generated_file = os.path.join(args['output_dir'],
                                              generated_filename % stem)
                rosidl_pycommon.expand_template(
                    os.path.join(template_dir, template_file),
                    data.copy(),
                    generated_file,
                    minimum_timestamp=latest_target_timestamp)

    rosidl_pycommon.expand_template(
        os.path.join(template_dir, 'lib.rs.em'),
        data.copy(),
        os.path.join(args['output_dir'], 'rust/src/lib.rs'),
        minimum_timestamp=latest_target_timestamp)

    cargo_toml_data = {
        'dependency_packages': dependency_packages,
        'package_name': package_name,
        'package_version': args['package_version'],
    }
    rosidl_pycommon.expand_template(
        os.path.join(template_dir, 'Cargo.toml.em'),
        cargo_toml_data,
        os.path.join(args['output_dir'], 'rust/Cargo.toml'),
        minimum_timestamp=latest_target_timestamp)

    rosidl_pycommon.expand_template(
        os.path.join(template_dir, 'build.rs.em'),
        {},
        os.path.join(args['output_dir'], 'rust/build.rs'),
        minimum_timestamp=latest_target_timestamp)

    return 0

def get_rs_name(name):
    keywords = [
        # strict keywords
        'as', 'break', 'const', 'continue', 'crate', 'else', 'enum', 'extern', 'false', 'fn', 'for', 'if', 'for',
        'impl', 'in', 'let', 'loop', 'match', 'mod', 'move', 'mut', 'pub', 'ref', 'return', 'self', 'Self', 'static',
        'struct', 'super', 'trait', 'true', 'type', 'unsafe', 'use', 'where', 'while',
        # Edition 2024+
        'gen',
        # Edition 2018+
        'async', 'await', 'dyn',
        # Reserved
        'abstract', 'become', 'box', 'do', 'final', 'macro', 'override', 'priv', 'typeof', 'unsized', 'virtual',
        'yield', 'try'
    ]
    # If the field name is a reserved keyword in Rust append an underscore
    return name if not name in keywords else name + '_'

def escape_string(s):
    s = s.replace('\\', '\\\\')
    s = s.replace("'", "\\'")
    return s


def value_to_rs(type_, value):
    assert type_.is_primitive_type()
    assert value is not None

    if not type_.is_array:
        return primitive_value_to_rs(type_, value)

    rs_values = []
    for single_value in value:
        rs_value = primitive_value_to_rs(type_, single_value)
        rs_values.append(rs_value)
    return '{%s}' % ', '.join(rs_values)


def primitive_value_to_rs(type_, value):
    assert type_.is_primitive_type()
    assert value is not None

    if type_.type == 'bool':
        return 'true' if value else 'false'

    if type_.type in [
            'byte',
            'char',
            'wchar',
            'int8',
            'uint8',
            'int16',
            'uint16',
            'int32',
            'uint32',
            'int64',
            'uint64',
            'float64',
    ]:
        return str(value)

    if type_.type == 'float32':
        return '%sf' % value

    if type_.type == 'string':
        return '"%s"' % escape_string(value)

    assert False, "unknown primitive type '%s'" % type_


def constant_value_to_rs(type_, value):
    assert value is not None

    if isinstance(type_, BasicType):
        if type_.typename == 'boolean':
            return 'true' if value else 'false'
        elif type_.typename == 'float32':
            return '%sf' % value
        return str(value)

    if isinstance(type_, AbstractGenericString):
        return '"%s"' % escape_string(value)

    assert False, "unknown constant type '%s'" % type_

# Type hierarchy:
#
# AbstractType
# - AbstractNestableType
#   - AbstractGenericString
#     - AbstractString
#       - BoundedString
#       - UnboundedString
#     - AbstractWString
#       - BoundedWString
#       - UnboundedWString
#   - BasicType
#   - NamedType
#   - NamespacedType
# - AbstractNestedType
#   - Array
#   - AbstractSequence
#     - BoundedSequence
#     - UnboundedSequence


def pre_field_serde(type_):
    if isinstance(type_, Array) and type_.size > 32:
        return '#[cfg_attr(feature = "serde", serde(with = "serde_big_array::BigArray"))]\n    '
    else:
        return ''


def make_get_rs_type(idiomatic):
    def get_rs_type(type_, current_idiomatic, desired_idiomatic):
        if isinstance(type_, BasicType):
            if type_.typename == 'boolean':
                return 'bool'
            elif type_.typename in ['byte', 'octet']:
                return 'u8'
            elif type_.typename == 'char':
                return 'u8'
            elif type_.typename == 'wchar':
                return 'u16'
            elif type_.typename == 'float':
                return 'f32'
            elif type_.typename == 'double':
                return 'f64'
            elif type_.typename == 'int8':
                return 'i8'
            elif type_.typename == 'uint8':
                return 'u8'
            elif type_.typename == 'int16':
                return 'i16'
            elif type_.typename == 'uint16':
                return 'u16'
            elif type_.typename == 'int32':
                return 'i32'
            elif type_.typename == 'uint32':
                return 'u32'
            elif type_.typename == 'int64':
                return 'i64'
            elif type_.typename == 'uint64':
                return 'u64'
        elif isinstance(type_, BoundedString):
            return 'rosidl_runtime_rs::BoundedString<{}>'.format(type_.maximum_size)
        elif isinstance(type_, BoundedWString):
            return 'rosidl_runtime_rs::BoundedWString<{}>'.format(type_.maximum_size)
        elif isinstance(type_, UnboundedString):
            return 'std::string::String' if current_idiomatic and desired_idiomatic else 'rosidl_runtime_rs::String'
        elif isinstance(type_, UnboundedWString):
            return 'std::string::String' if current_idiomatic and desired_idiomatic else 'rosidl_runtime_rs::WString'
        elif isinstance(type_, Array):
            return f'[{get_rs_type(type_.value_type, current_idiomatic, desired_idiomatic)}; {type_.size}]'
        elif isinstance(type_, UnboundedSequence):
            container_type = 'Vec' if current_idiomatic and desired_idiomatic else 'rosidl_runtime_rs::Sequence'
            return f'{container_type}<{get_rs_type(type_.value_type, current_idiomatic, desired_idiomatic)}>'
        elif isinstance(type_, BoundedSequence):
            # BoundedSequences can be in the idiomatic API, but the containing type cannot be from the
            # idiomatic API because we do not implement SequenceAlloc for idiomatic types.
            return f'rosidl_runtime_rs::BoundedSequence<{get_rs_type(type_.value_type, current_idiomatic, False)}, {type_.maximum_size}>'
        elif isinstance(type_, NamespacedType):
            # All types should be referencable like this
            # `super::msg::rmw::Foo` (From idiomatic modules)
            # `super::super::msg::rmw::Foo` (From non-idiomatic modules)
            # `<other_package>::msg::rmw::Foo` (From external packages)
            prefix = 'super::' if current_idiomatic else 'super::super::'

            symbol = f'{prefix}{"::".join(type_.namespaced_name()[1:])}'

            # This symbol is coming from an external crate (or needs a `use` statement).
            # So it should not be relative (i.e., no `super::`) and should have the top level
            # package name (i.e., `builtin_interfaces::`)
            top_level_package = type_.namespaces[0]
            if top_level_package != package_name:
                symbol = "::".join(type_.namespaced_name())

            if not desired_idiomatic and "::rmw::" not in symbol:
                parts = symbol.split("::")
                parts.insert(-1, "rmw")
                symbol = "::".join(parts)

            return symbol

        assert False, "unknown type '%s'" % type_.typename

    # Start out by assuming all calls have matching current and desired idiomatic values.
    # (i.e. symbols within the `...::rmw` scope want other values in the `...::rmw` scope).
    return lambda _type: get_rs_type(_type, idiomatic, idiomatic)
