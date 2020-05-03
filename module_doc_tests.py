import unittest
from module_doc import ModuleDoc


class TestModuleDoc(unittest.TestCase):
    def test_init(self):
        self.assertEqual(ModuleDoc('example').name, 'example')

    def test_buildReturnsDocumentWithName(self):
        doc = ModuleDoc('example')
        self.assertEqual('# example module\n\n', doc.build())

    def test_addMethod(self):
        doc = ModuleDoc('example')
        doc.addMethod('Test', ['String'])
        self.assertTrue('Test' in doc.methods)
        self.assertEqual(['String'], doc.methods['Test'])

    def test_buildReturnsSubDeclaration(self):
        doc = ModuleDoc('example')
        doc.addMethod("Start", '')

        expected = ('# example module\n\n'
                    '# Methods\n\n'
                    '|Name|Description|\n'
                    '|-|-|\n'
                    '|[Start ()](./Start.md)||\n')

        actual = doc.build()
        self.assertEqual(expected, actual)

    def test_buildReturnsSubDeclarationWithArg(self):
        doc = ModuleDoc('example')
        doc.addMethod('Start', 'String')

        expected = ('# example module\n\n'
                    '# Methods\n\n'
                    '|Name|Description|\n'
                    '|-|-|\n'
                    '|[Start (String)](./Start.md)||\n')

        actual = doc.build()
        self.assertEqual(expected, actual)

    def test_buildReturnsSubDeclarationWithArgs(self):
        doc = ModuleDoc('example')
        doc.addMethod('Start', ['String', 'Long'])

        expected = ('# example module\n\n'
                    '# Methods\n\n'
                    '|Name|Description|\n'
                    '|-|-|\n'
                    '|[Start (String, Long)](./Start.md)||\n')

        actual = doc.build()
        self.assertEqual(expected, actual)

    def test_buildReturnsValueWhenManyDeclarations(self):
        doc = ModuleDoc('example')
        doc.addMethod('Start', '')
        doc.addMethod('Finish', '')

        expected = ('# example module\n\n'
                    '# Methods\n\n'
                    '|Name|Description|\n'
                    '|-|-|\n'
                    '|[Start ()](./Start.md)||\n'
                    '|[Finish ()](./Finish.md)||\n')

        self.assertEqual(expected, doc.build())


if __name__ == "__main__":
    unittest.main()
