import unittest
from method_doc import MethodDoc


class TestMethodDoc(unittest.TestCase):
    def test_init(self):
        expected = '# Foo.Bar () Method\n\n'
        actual = MethodDoc('Foo', 'Bar ()').build()
        self.assertEqual(expected, actual)

    def test_buildReturnsDocWithDescription(self):
        expected = ('# Foo.Bar () Method\n\n'
                    'Description of Foo.Bar\n\n')
        doc = MethodDoc('Foo', 'Bar ()')
        doc.set_description('Description of Foo.Bar')
        self.assertEqual(expected, doc.build())

    def test_buildReturnsDocWithSignature(self):
        expected = ('# Foo.Bar () Method\n\n'
                    'Description of Foo.Bar\n\n'
                    '```vb\n'
                    'Public Sub Bar ()\n'
                    '```\n\n')

        doc = MethodDoc('Foo', 'Bar ()')
        doc.set_description('Description of Foo.Bar')
        doc.set_signature('Public Sub Bar ()')

        self.assertEqual(expected, doc.build())

    def test_buildReturnsDocWhenOneArgument(self):
        expected = ('# Foo.Bar (Variant) Method\n\n'
                    'Description of Foo.Bar\n\n'
                    '```vb\n'
                    'Public Sub Bar (ByVal Item As Variant)\n'
                    '```\n\n'
                    '### Parameters\n\n'
                    '**Item** `Variant` <br>\n'
                    'Description of an item.\n\n')

        doc = MethodDoc('Foo', 'Bar (Variant)')
        doc.set_description('Description of Foo.Bar')
        doc.set_signature('Public Sub Bar (ByVal Item As Variant)')
        doc.add_parameter('Item', 'Variant', 'Description of an item.')

        self.assertEqual(expected, doc.build())

    def test_buildReturnsDocWhenAtLeastOneArgument(self):
        expected = ('# Foo.Bar (Variant, Variant) Method\n\n'
                    'Description of Foo.Bar\n\n'
                    '```vb\n'
                    'Public Sub Bar (ByVal Item As Variant, ByVal Item2 As Variant)\n'
                    '```\n\n'
                    '### Parameters\n\n'
                    '**Item** `Variant` <br>\n'
                    'Description of an item.\n\n'
                    '**Item2** `Variant` <br>\n'
                    'Description of an item2.\n\n')

        doc = MethodDoc('Foo', 'Bar (Variant, Variant)')
        doc.set_description('Description of Foo.Bar')
        doc.set_signature(
            'Public Sub Bar (ByVal Item As Variant, ByVal Item2 As Variant)')
        doc.add_parameter('Item', 'Variant', 'Description of an item.')
        doc.add_parameter('Item2', 'Variant', 'Description of an item2.')

        self.assertEqual(expected, doc.build())

    def test_buildReturnsDocWhenMethodIsFunctionZeroArgs(self):
        expected = ('# Foo.Bar () Method\n\n'
                    'Description of Foo.Bar\n\n'
                    '```vb\n'
                    'Public Function Bar () As String\n'
                    '```\n\n'
                    '### Returns\n\n'
                    '`String` <br>\n'
                    'Description of return value\n\n')

        doc = MethodDoc('Foo', 'Bar ()')
        doc.set_description('Description of Foo.Bar')
        doc.set_signature('Public Function Bar () As String')
        doc.add_returns('String', 'Description of return value')

        self.assertEqual(expected, doc.build())

    def test_buildReturnsDocWhenMethodIsFunctionAtLeastOneArg(self):
        expected = ('# Foo.Bar (Variant) Method\n\n'
                    'Description of Foo.Bar\n\n'
                    '```vb\n'
                    'Public Function Bar (ByVal Item As Variant) As String\n'
                    '```\n\n'
                    '### Parameters\n\n'
                    '**Item** `Variant` <br>\n'
                    'Description of an item.\n\n'
                    '### Returns\n\n'
                    '`String` <br>\n'
                    'Description of return value\n\n')

        doc = MethodDoc('Foo', 'Bar (Variant)')
        doc.set_description('Description of Foo.Bar')
        doc.set_signature(
            'Public Function Bar (ByVal Item As Variant) As String')
        doc.add_parameter('Item', 'Variant', 'Description of an item.')
        doc.add_returns('String', 'Description of return value')

        self.assertEqual(expected, doc.build())

    def test_buildReturnsDocWhenErrorDefined(self):
        expected = ('# Foo.Bar () Method\n\n'
                    'Description of Foo.Bar\n\n'
                    '```vb\n'
                    'Public Sub Bar ()\n'
                    '```\n\n'
                    '### Errors\n\n'
                    '`OnInvalidArgumentError` <br>\n'
                    'Description of error\n\n')

        doc = MethodDoc('Foo', 'Bar ()')
        doc.set_description('Description of Foo.Bar')
        doc.set_signature('Public Sub Bar ()')
        doc.add_error('OnInvalidArgumentError', 'Description of error')

        self.assertEqual(expected, doc.build())

    def test_buildReturnsDocWhenMultipleErrorsDefined(self):
        expected = ('# Foo.Bar () Method\n\n'
                    'Description of Foo.Bar\n\n'
                    '```vb\n'
                    'Public Sub Bar ()\n'
                    '```\n\n'
                    '### Errors\n\n'
                    '`OnInvalidArgumentError` <br>\n'
                    'Description of error\n\n'
                    '`OnArgumentOutOfRangeError` <br>\n'
                    'Description of error\n\n')

        doc = MethodDoc('Foo', 'Bar ()')
        doc.set_description('Description of Foo.Bar')
        doc.set_signature('Public Sub Bar ()')
        doc.add_error('OnInvalidArgumentError', 'Description of error')
        doc.add_error('OnArgumentOutOfRangeError', 'Description of error')

        self.assertEqual(expected, doc.build())

    def test_buildReturnsDocWithExample(self):
        expected = ('# Foo.Bar () Method\n\n'
                    'Description of Foo.Bar\n\n'
                    '```vb\n'
                    'Public Sub Bar ()\n'
                    '```\n\n'
                    '## Examples\n\n'
                    'This is an example.\n\n')

        doc = MethodDoc('Foo', 'Bar ()')
        doc.set_description('Description of Foo.Bar')
        doc.set_signature('Public Sub Bar ()')
        doc.set_example('This is an example.')

        self.assertEqual(expected, doc.build())

    def test_buildReturnDocWithRemarks(self):
        expected = ('# Foo.Bar () Method\n\n'
                    '### Remarks\n\n'
                    'This is an example.')

        doc = MethodDoc('Foo', 'Bar ()')
        doc.set_example('This is an example.')


if __name__ == "__main__":
    unittest.main()
