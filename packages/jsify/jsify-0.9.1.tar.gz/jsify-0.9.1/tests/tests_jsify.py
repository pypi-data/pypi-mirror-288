import pickle
from unittest import TestCase

from jsify.calls import jsified_function, camelized_function
from jsify.jsify import JsonDict, jsify, json_copy, json_get, json_pop, json_popitem, json_setdefault, json_update, \
    json_values, json_keys, json_items, unjsify, JsonIterator, properties_exist, PropertiesExistResult
from jsify.jsify import JsonObject

from jsify.encoder import dumps

from jsify.undefined import Undefined


class TestJsonObject(TestCase):
    test_dict = dict(a=1, b=dict(a=1, b=2, c=3), c=3)
    test_merge = dict(d=1, e=dict(a=1, b=2, c=3), f=3)
    test_list = [1, 2, 3, 4, 5, 6, 7, test_dict, test_merge]
    test_tuple = (1, dict(a=1, b=2, c=3), 3, test_dict)
    test_literal = 2
    test_types_dict = dict(list=test_list, dict=test_dict, tuple=test_tuple, literal=test_literal)
    test_types_list = [test_types_dict['list'], test_types_dict['dict'], test_types_dict['tuple'], test_literal]
    test_types_tuple = (test_types_dict['list'], test_types_dict['dict'], test_types_dict['tuple'], test_literal)

    def test_create_from_literal(self):
        self.assertEqual(jsify(1), 1)
        self.assertEqual(jsify(1.1), 1.1)
        self.assertEqual(jsify("string"), "string")
        self.assertEqual(jsify(None), None)
        self.assertEqual(jsify(True), True)

    def test_create_from_dict(self):
        json_object = jsify(self.test_dict)
        self.assertIsInstance(json_object, JsonDict)
        self.assertDictEqual(unjsify(json_object), self.test_dict)

    def test_create_from_dict_with_merge(self):
        json_object = jsify(self.test_dict, **self.test_merge)
        self.assertIsInstance(json_object, JsonDict)
        self.assertDictEqual(unjsify(json_object), self.test_dict | self.test_merge)

    def test_create_from_list(self):
        self.assertListEqual(list(jsify(self.test_list)), self.test_list)

    def test_create_from_tuple(self):
        self.assertTupleEqual(tuple(jsify(self.test_tuple)), self.test_tuple)

    def test_get_from_dict(self):
        json_object = jsify(self.test_types_dict)
        self.assertNotIsInstance(json_object.literal, JsonObject)
        self.assertEqual(json_object.literal, self.test_literal)
        self.assertIsInstance(json_object.dict, JsonObject)
        self.assertDictEqual(unjsify(json_object.dict), self.test_dict)
        self.assertIsInstance(json_object.list, JsonObject)
        self.assertListEqual(unjsify(json_object.list), self.test_list)
        self.assertIsInstance(json_object.tuple, JsonObject)
        self.assertTupleEqual(unjsify(json_object.tuple), self.test_tuple)

        self.assertNotIsInstance(json_object['literal'], JsonObject)
        self.assertEqual(json_object['literal'], self.test_literal)
        self.assertIsInstance(json_object['dict'], JsonObject)
        self.assertDictEqual(unjsify(json_object['dict']), self.test_dict)
        self.assertIsInstance(json_object['list'], JsonObject)
        self.assertListEqual(unjsify(json_object['list']), self.test_list)
        self.assertIsInstance(json_object['tuple'], JsonObject)
        self.assertTupleEqual(unjsify(json_object['tuple']), self.test_tuple)

    def macro_test_get_from_list_or_tuple(self, json_object):
        self.assertIsInstance(json_object[0], JsonObject)
        self.assertListEqual(unjsify(json_object[0]), self.test_list)
        self.assertIsInstance(json_object[1], JsonObject)
        self.assertDictEqual(unjsify(json_object[1]), self.test_dict)
        self.assertIsInstance(json_object[2], JsonObject)
        self.assertTupleEqual(unjsify(json_object[2]), self.test_tuple)
        self.assertNotIsInstance(json_object[3], JsonObject)
        self.assertEqual(json_object[3], self.test_literal)

    def test_get_from_list(self):
        self.macro_test_get_from_list_or_tuple(jsify(self.test_types_list))

    def test_get_from_tuple(self):
        self.macro_test_get_from_list_or_tuple(jsify(self.test_types_tuple))

    def test_create_attributes_in_dict(self):
        json_object = jsify(self.test_dict.copy())
        json_object.new_literal = self.test_literal
        json_object.new_dict = self.test_dict
        json_object.new_list = self.test_list
        json_object.new_tuple = self.test_tuple
        self.assertDictEqual(unjsify(json_object), self.test_dict | dict(
            new_literal=self.test_literal, new_dict=self.test_dict, new_list=self.test_list, new_tuple=self.test_tuple))

        additional_json_object = jsify(self.test_dict)
        json_object.additional_json = additional_json_object
        self.assertNotIsInstance(unjsify(json_object.additional_json), JsonObject)

        json_object = jsify(self.test_dict.copy())
        json_object['new_literal'] = self.test_literal
        json_object['new_dict'] = self.test_dict
        json_object['new_list'] = self.test_list
        json_object['new_tuple'] = self.test_tuple
        self.assertDictEqual(unjsify(json_object), self.test_dict | dict(
            new_literal=self.test_literal, new_dict=self.test_dict, new_list=self.test_list, new_tuple=self.test_tuple))

        additional_json_object = jsify(self.test_dict)
        json_object['additional_json'] = additional_json_object
        self.assertNotIsInstance(unjsify(json_object['additional_json']), JsonObject)

    def test_create_elements_in_list(self):
        json_object = jsify(self.test_list.copy())
        json_object.append(self.test_literal)
        json_object.append(self.test_dict)
        json_object.append(self.test_list)
        json_object.append(self.test_tuple)
        self.assertListEqual(unjsify(json_object), self.test_list +
                             [self.test_literal, self.test_dict, self.test_list, self.test_tuple])

        additional_json_object = jsify(self.test_dict)
        json_object.append(additional_json_object)
        self.assertNotIsInstance(unjsify(json_object[-1]), JsonObject)

    def test_vars(self):
        class MyClass:
            pass

        json_object = jsify(MyClass())
        self.assertDictEqual(unjsify(vars(json_object)), {})
        json_object = jsify(self.test_list)
        digits = len(str(len(self.test_list)))
        self.assertDictEqual(unjsify(vars(json_object)),
                             {f"{key:0{digits}}": value for key, value in enumerate(self.test_list)})
        json_object = jsify(self.test_tuple)
        digits = len(str(len(self.test_tuple)))
        self.assertDictEqual(unjsify(vars(json_object)),
                             {f"{key:0{digits}}": value for key, value in enumerate(self.test_tuple)})
        json_object = jsify(self.test_dict)
        self.assertDictEqual(unjsify(vars(json_object)), {key: value for key, value in self.test_dict.items()})

    def test_contains(self):
        json_object = jsify(self.test_dict)
        self.assertIn(list(json_keys(self.test_dict))[0], json_object)
        self.assertIn(list(json_keys(self.test_dict))[0], json_keys(json_object))
        self.assertIn(list(json_values(self.test_dict))[0], json_values(json_object))
        self.assertIn(list(json_items(self.test_dict))[0], json_items(json_object))
        self.assertNotIn('key_which_doesnt_exist', json_object)
        self.assertNotIn('key_which_doesnt_exist', json_keys(json_object))
        self.assertNotIn('key_which_doesnt_exist', json_values(json_object))
        self.assertNotIn('key_which_doesnt_exist', json_items(json_object))
        json_object = jsify(self.test_list)
        self.assertIn(0, json_object)
        self.assertIn('0', json_object)
        self.assertNotIn('1000', json_object)
        json_object = jsify(self.test_tuple)
        self.assertIn(0, json_object)
        self.assertIn('0', json_object)
        self.assertNotIn('1000', json_object)

    def test_copy(self):
        json_object = jsify(self.test_list)
        json_object_copy = json_object.copy()
        self.assertEqual(unjsify(json_object_copy), unjsify(json_object))
        json_object_copy[0] = None
        self.assertNotEqual(unjsify(json_object_copy), unjsify(json_object))

        json_object = jsify(self.test_tuple)
        self.assertEqual(unjsify(json_object.copy()), unjsify(json_object))

        json_object = jsify(self.test_dict)
        json_object_copy = json_copy(json_object, deep=True)
        self.assertEqual(unjsify(json_object_copy), unjsify(json_object))
        b = json_object_copy.a
        json_object_copy.a = None
        self.assertNotEqual(unjsify(json_object_copy), unjsify(json_object))

    def test_tuple_functions(self):
        json_object = jsify(self.test_tuple)
        self.assertEqual(json_object.count(1), self.test_tuple.count(1))
        self.assertEqual(json_object.index(1), self.test_tuple.index(1))

    def test_list_functions(self):
        test_list = self.test_list.copy()
        json_object = jsify(test_list).copy()
        self.assertEqual(json_object.count(1), test_list.count(1))
        self.assertEqual(json_object.index(1), test_list.index(1))
        json_object.append(10)
        test_list.append(10)
        self.assertEqual(unjsify(json_object), test_list)
        json_object.insert(2, 10)
        test_list.insert(2, 10)
        self.assertEqual(unjsify(json_object), test_list)
        json_object.remove(1)
        test_list.remove(1)
        self.assertEqual(unjsify(json_object), test_list)
        json_object.extend([9, 8, 7])
        test_list.extend([9, 8, 7])
        self.assertEqual(unjsify(json_object), test_list)
        json_object.pop(3)
        test_list.pop(3)
        self.assertEqual(unjsify(json_object), test_list)
        json_object.reverse()
        test_list.reverse()
        self.assertEqual(unjsify(json_object), test_list)
        for value in list(iter(json_object)):
            if isinstance(value, JsonDict):
                json_object.remove(value)
                test_list.remove(value)
        json_object.sort()
        test_list.sort()
        self.assertEqual(unjsify(json_object), test_list)
        json_object.clear()
        test_list.clear()
        self.assertEqual(unjsify(json_object), test_list)

    def test_dict_functions(self):
        test_dict = self.test_dict.copy()
        json_object = json_copy(jsify(test_dict))
        self.assertEqual(json_get(json_object, 'a'), test_dict.get('a'))
        self.assertListEqual(list(json_items(json_object)), list(test_dict.items()))
        self.assertListEqual(list(json_keys(json_object)), list(test_dict.keys()))
        self.assertListEqual(list(json_values(json_object)), list(test_dict.values()))
        json_pop(json_object, 'a')
        test_dict.pop('a')
        self.assertEqual(jsify(json_object), test_dict)
        json_popitem(json_object)
        test_dict.popitem()
        self.assertEqual(jsify(json_object), test_dict)
        json_setdefault(json_object, 'c', 8)
        json_setdefault(json_object, 'd', 8)
        test_dict.setdefault('c', 8)
        test_dict.setdefault('d', 8)
        self.assertEqual(jsify(json_object), test_dict)
        json_update(json_object, dict(z=1, n=2, m=3), u=7)
        test_dict.update(dict(z=1, n=2, m=3), u=7)
        self.assertEqual(jsify(json_object), test_dict)

    def test_json_dump(self):
        json_object = jsify(dict(a=1, b=2, c=jsify(self.test_dict), d=jsify(self.test_list),
                                 e=jsify(self.test_tuple), undef=Undefined))
        test_dict_with_undefined = dict(a=1, b=2, c=self.test_dict, d=self.test_list, e=self.test_tuple,
                                        undef=Undefined)
        test_dict_without_undefined = dict(a=1, b=2, c=self.test_dict, d=self.test_list, e=self.test_tuple)
        self.assertNotEqual(dumps(json_object, omit_undefined=False), dumps(test_dict_with_undefined))
        self.assertEqual(dumps(json_object, omit_undefined=False),
                         dumps(test_dict_with_undefined, omit_undefined=False))
        self.assertEqual(dumps(json_object), dumps(test_dict_without_undefined))
        self.assertNotEqual(dumps(json_object, omit_undefined=False), dumps(test_dict_without_undefined))

    def test_keys_values_items(self):
        json_object = jsify(self.test_dict)
        keys = json_keys(json_object)
        self.assertEqual(list(keys), list(self.test_dict.keys()))
        self.assertEqual(list(jsify(self.test_dict.keys())), list(self.test_dict.keys()))
        values = json_values(json_object)
        self.assertEqual(list(values), list(self.test_dict.values()))
        self.assertEqual(list(jsify(self.test_dict.values())), list(self.test_dict.values()))
        items = json_items(json_object)
        self.assertEqual(list(items), list(self.test_dict.items()))
        self.assertEqual(list(jsify(self.test_dict.items())), list(self.test_dict.items()))

    def test_pickle(self):
        json_object = jsify(self.test_list)
        json_object.append(self.test_literal)
        json_object.append(self.test_dict)
        json_object.append(self.test_tuple)
        pickled = pickle.dumps(json_object)
        depickled = pickle.loads(pickled)
        dir(depickled)
        self.assertEqual(depickled, json_object)

    def test_undefined(self):
        json_object = jsify(self.test_dict)
        self.assertEqual(Undefined, None)
        self.assertNotEqual(Undefined, 0)
        self.assertTrue(Undefined is not True)
        self.assertTrue(Undefined is not False)
        self.assertTrue(Undefined != True)
        self.assertTrue(Undefined != False)
        self.assertTrue(Undefined == None)
        self.assertTrue(Undefined is not None)
        self.assertEqual(json_object.not_defined_property, Undefined)
        self.assertEqual(json_object.not_defined_property.fghjj.dsffsd['42'], Undefined)

    def test_dict_call(self):
        json_object = jsify(self.test_dict)
        json_object('unexisting', dict, dict(a=1, b=2)).c = 3
        self.assertTrue(json_object.unexisting.a == 1)
        self.assertTrue(json_object.unexisting.b == 2)
        self.assertTrue(json_object.unexisting.c == 3)
        json_object('unexisting', dict, dict(a=3, b=4)).c = 5
        self.assertTrue(json_object.unexisting.a == 1)
        self.assertTrue(json_object.unexisting.b == 2)
        self.assertTrue(json_object.unexisting.c == 5)

    def test_iterator(self):
        dict_iterator = JsonIterator(self.test_dict)
        for json_key, native_key in zip(dict_iterator, self.test_dict.keys()):
            self.assertEqual(json_key, native_key)
        list_iterator = JsonIterator(self.test_list)
        for json_value, native_value in zip(list_iterator, self.test_list):
            self.assertEqual(json_value, native_value)
        tuple_iterator = JsonIterator(self.test_tuple)
        for json_value, native_value in zip(tuple_iterator, self.test_tuple):
            self.assertEqual(json_value, native_value)
        dict_iterator = JsonIterator(jsify(self.test_dict))
        for json_key, native_key in zip(dict_iterator, self.test_dict.keys()):
            self.assertEqual(json_key, native_key)
        list_iterator = JsonIterator(jsify(self.test_list))
        for json_value, native_value in zip(list_iterator, self.test_list):
            self.assertEqual(json_value, native_value)
        tuple_iterator = JsonIterator(jsify(self.test_tuple))
        for json_value, native_value in zip(tuple_iterator, self.test_tuple):
            self.assertEqual(json_value, native_value)

    def test_properties_exist(self):
        result = properties_exist(self.test_dict, 'b', 'b')
        self.assertTrue(result)
        self.assertEqual(result.unjsified, self.test_dict['b']['b'])
        self.assertEqual(result.jsified, jsify(self.test_dict['b']['b']))
        self.assertFalse(properties_exist(self.test_dict, 'a', 'b'))

    def test_jsified_camelized_function(self):

        @jsified_function(result_original=True)
        @camelized_function(replace=dict(last_parameter='last'))
        def test_function_original(first_parameter, second_parameter, last):
            return [first_parameter.value, second_parameter.value, last.value]

        input_parameters = dict(firstParameter=dict(value=1), second_parameter=dict(value=2),
                                lastParameter=dict(value=(3, jsify([1, 2]))))
        result = test_function_original(**input_parameters)
        self.assertEqual(result, [1, 2, (3, jsify([1, 2]))])
        self.assertNotIsInstance(result, JsonObject)
        self.assertIsInstance(result[2][1], JsonObject)

        @jsified_function(result_deep_original=True)
        @camelized_function(replace=dict(last_parameter='last'))
        def test_function_deep_original(first_parameter, second_parameter, last):
            return [first_parameter.value, second_parameter.value, last.value]

        input_parameters = dict(firstParameter=dict(value=1), second_parameter=dict(value=2),
                                lastParameter=dict(value=(3, jsify([1, 2]))))
        result = test_function_deep_original(**input_parameters)
        self.assertEqual(result, [1, 2, (3, [1, 2])])
        self.assertNotIsInstance(result, JsonObject)
        self.assertNotIsInstance(result[2][1], JsonObject)

        @jsified_function
        @camelized_function(replace=dict(last_parameter='last'))
        def test_function(first_parameter, second_parameter, last):
            return [first_parameter.value, second_parameter.value, last.value]

        input_parameters = dict(firstParameter=dict(value=1), second_parameter=dict(value=2),
                                lastParameter=dict(value=(3, jsify([1, 2]))))
        result = test_function(**input_parameters)
        self.assertEqual(result, [1, 2, (3, [1, 2])])
        self.assertIsInstance(result, JsonObject)
