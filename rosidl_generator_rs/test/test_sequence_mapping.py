# Copyright 2026 Open Source Robotics Foundation, Inc.
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

import unittest

from rosidl_generator_rs import get_public_rs_type, make_get_rs_type
from rosidl_parser.definition import (
    Array, BasicType, BoundedSequence, NamespacedType,
    UnboundedSequence, UnboundedString, UnboundedWString,
)


class SequenceMappingTest(unittest.TestCase):
    def test_primitive_sequences(self):
        types = {
            'boolean': 'bool', 'char': 'u8', 'wchar': 'u16',
            'octet': 'u8', 'float': 'f32', 'double': 'f64',
            'int8': 'i8', 'uint8': 'u8', 'int16': 'i16', 'uint16': 'u16',
            'int32': 'i32', 'uint32': 'u32', 'int64': 'i64', 'uint64': 'u64',
        }
        native = make_get_rs_type(False)
        idiomatic = make_get_rs_type(True)
        for name, rust in types.items():
            with self.subTest(type=name):
                element = BasicType(name)
                self.assertEqual(native(UnboundedSequence(element)),
                                 f'rosidl_runtime_rs::Sequence<{rust}>')
                self.assertEqual(idiomatic(UnboundedSequence(element)), f'Vec<{rust}>')
                self.assertEqual(native(BoundedSequence(element, 8)),
                                 f'rosidl_runtime_rs::BoundedSequence<{rust}, 8>')
                self.assertEqual(native(Array(element, 8)), f'[{rust}; 8]')
                self.assertEqual(idiomatic(BoundedSequence(element, 8)),
                                 f'rosidl_runtime_rs::BoundedSequence<{rust}, 8>')
                self.assertEqual(get_public_rs_type(UnboundedSequence(element), 'buffer'),
                                 'rosidl_buffer_rs::Buffer<u8>' if name == 'uint8'
                                 else f'Vec<{rust}>')
                self.assertEqual(get_public_rs_type(BoundedSequence(element, 8), 'buffer'),
                                 f'rosidl_buffer_rs::BoundedVec<{rust}, 8>')

    def test_string_and_message_sequences(self):
        native = make_get_rs_type(False)
        for element, rust in [
            (UnboundedString(), 'rosidl_runtime_rs::String'),
            (UnboundedWString(), 'rosidl_runtime_rs::WString'),
            (NamespacedType(['other', 'msg'], 'Sample'), 'other::msg::rmw::Sample'),
        ]:
            with self.subTest(type=rust):
                self.assertEqual(native(UnboundedSequence(element)),
                                 f'rosidl_runtime_rs::Sequence<{rust}>')
                self.assertEqual(native(BoundedSequence(element, 8)),
                                 f'rosidl_runtime_rs::BoundedSequence<{rust}, 8>')


    def test_buffer_nested_messages(self):
        element = NamespacedType(['other', 'msg'], 'Image')
        self.assertEqual(get_public_rs_type(element, 'buffer'), 'other::msg::buffer::Image')
        self.assertEqual(get_public_rs_type(UnboundedSequence(element), 'buffer'),
                         'Vec<other::msg::buffer::Image>')
        self.assertEqual(get_public_rs_type(BoundedSequence(element, 3), 'buffer'),
                         'rosidl_buffer_rs::BoundedVec<other::msg::buffer::Image, 3>')
        self.assertEqual(get_public_rs_type(Array(element, 3), 'buffer'),
                         '[other::msg::buffer::Image; 3]')


if __name__ == '__main__':
    unittest.main()
