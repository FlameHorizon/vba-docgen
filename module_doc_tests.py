import unittest
from module_doc import ModuleDoc


class TestModuleDoc(unittest.TestCase):
    def test_init(self):
        self.assertEqual(ModuleDoc('example').namespace, 'example')

    def test_buildReturnsDocumentWithName(self):
        doc = ModuleDoc('example')
        self.assertEqual('# example module\n\n', doc.build())

    def test_buildReturnsDocumentWithDescription(self):
        doc = ModuleDoc('example', 'This is a module description')
        self.assertEqual(
            '# example module\n\nThis is a module description\n\n', doc.build())

    def test_addMethod(self):
        doc = ModuleDoc('example')
        doc.addMethod('Test', {'Foo': 'String'}, 'Test description')
        self.assertTrue('Test' in doc.methods)
        self.assertEqual(['String'], list(doc.methods['Test'][0].values()))
        self.assertEqual('Test description', doc.methods['Test'][1])

    def test_buildReturnsSubDeclaration(self):
        doc = ModuleDoc('example')
        doc.addMethod("Start", {})

        expected = ('# example module\n\n'
                    '# Methods\n\n'
                    '|Name|Description|\n'
                    '|---|---|\n'
                    '|[Start ()](./Start.md)||\n')

        actual = doc.build()
        self.assertEqual(expected, actual)

    def test_buildReturnsSubDeclarationWithArg(self):
        doc = ModuleDoc('example')
        doc.addMethod('Start', {'Foo': 'String'})

        expected = ('# example module\n\n'
                    '# Methods\n\n'
                    '|Name|Description|\n'
                    '|---|---|\n'
                    '|[Start (String)](./Start.md)||\n')

        actual = doc.build()
        self.assertEqual(expected, actual)

    def test_buildReturnsSubDeclarationWithArgs(self):
        doc = ModuleDoc('example')
        doc.addMethod('Start', {'Foo1': 'String', 'Foo2': 'Long'})

        expected = ('# example module\n\n'
                    '# Methods\n\n'
                    '|Name|Description|\n'
                    '|---|---|\n'
                    '|[Start (String, Long)](./Start.md)||\n')

        actual = doc.build()
        self.assertEqual(expected, actual)

    def test_buildReturnsValueWhenManyDeclarations(self):
        doc = ModuleDoc('example')
        doc.addMethod('Start', {})
        doc.addMethod('Finish', {})

        expected = ('# example module\n\n'
                    '# Methods\n\n'
                    '|Name|Description|\n'
                    '|---|---|\n'
                    '|[Finish ()](./Finish.md)||\n'
                    '|[Start ()](./Start.md)||\n')

        self.assertEqual(expected, doc.build())

    def test_buildReturnsValueWhenDescriptionAvailable(self):
        doc = ModuleDoc('example')
        doc.addMethod('Foo', {}, 'This is example method description')

        expected = ('# example module\n\n'
                    '# Methods\n\n'
                    '|Name|Description|\n'
                    '|---|---|\n'
                    '|[Foo ()](./Foo.md)|This is example method description|\n')

        self.assertEqual(expected, doc.build())


if __name__ == "__main__":
    unittest.main()
