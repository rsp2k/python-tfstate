# -*- coding: utf-8 -*-

# Python stdlib
import unittest
import json

# Python tfstate
from tfstate.base import Tfstate, TfstateModule

# Functional tests
from functional_tests.base import BaseFunctionalTest


class TfstateFileFunctionalTest(BaseFunctionalTest):
    def load_tfstate_data_from_file(self):
        tfstate_file = open(self.tfstate_path, 'r')
        tfstate_data = json.load(tfstate_file)
        self.assertIsInstance(tfstate_data, dict)

        return tfstate_data

    def test_i_can_load_a_tfstate_file(self):
        # I want to load a tfstate file and check is a valid tfstate file
        tfstate_data = self.load_tfstate_data_from_file()
        # I check that contains a version attribute
        self.assertIn('version', tfstate_data)
        # I check that contains a serial attribute
        self.assertIn('serial', tfstate_data)
        # I check that contains a modules attribute
        self.assertIn('modules', tfstate_data)

    def test_i_can_load_a_tfstate_into_object(self):
        # I want to load a tfstate file and load its contents to a Tfstate object
        tfstate = Tfstate(self.tfstate_path)
        tfstate_data = self.load_tfstate_data_from_file()
        # I want to check that the version attribute is present and matches the original data
        self.assertEqual(tfstate.version, tfstate_data['version'], 'tfstate version does not match')
        # And that the serial is present too and matches as well
        self.assertEqual(tfstate.serial, tfstate_data['serial'], 'tfstate serial does not match')
        # And that the modules attribute is a list
        self.assertIsInstance(tfstate.modules, list, 'tfstate modules attribute is not a list')

    def test_i_can_get_a_list_of_module_objects(self):
        # I want to load a tfstate and get the list of module objects parsed
        tfstate = Tfstate(self.tfstate_path)
        # I want to check that the modules attribute is a list of module objects
        self.assertIsInstance(tfstate.modules, list, 'tfstate modules attribute is not a list')
        for module in tfstate.modules:
            self.assertIsInstance(module, TfstateModule, 'tfstate module class does not match')

    def test_i_can_get_module_attributes(self):
        # I want to load a tfstate, get a module and check its attributes
        tfstate = Tfstate(self.tfstate_path)
        # I get the first module from the tfstate
        self.assertGreaterEqual(len(tfstate.modules), 1, 'tfstate file does not contain modules')
        first_native_module = tfstate.native_data['modules'][0]
        first_module = tfstate.modules[0]
        self.assertEqual(first_module.path, first_native_module['path'], 'module path attribute does not match')
        self.assertEqual(
            first_module.outputs, first_native_module['outputs'], 'module outputs attribute does not match')
        self.assertEqual(
            first_module.resources, first_native_module['resources'], 'module resources attribute does not match')


def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(TfstateFileFunctionalTest))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())