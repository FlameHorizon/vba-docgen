import unittest
import method_parser


class TestModuleDoc(unittest.TestCase):
    def test_makeReturnsSub(self):
        desc = {'Foo.Bar ()': {'description': 'Test description',
                               'example': 'Test example'}}
        code = ('Attribute VB_Name = \"Foo\"\n'
                'Public Sub Bar()\n\n'
                'End Sub')

        expected = ('# Foo.Bar Method\n\n'
                    'Test description\n\n'
                    '```vb\n'
                    'Public Sub Bar()\n'
                    '```\n\n'
                    '## Examples\n\n'
                    'Test example')

        actual = method_parser.MethodParser().make(code, desc)[0].build()
        self.assertEqual(expected, actual)

    def test_makeReturnsSubWithOneParameter(self):
        desc = {'Foo.Bar (String)': {'description': 'Test description',
                                     'example': 'Test example',
                                     'parameters': {'Arg1': 'Test Arg1 description'}}}
        code = ('Attribute VB_Name = \"Foo\"\n'
                'Public Sub Bar(ByVal Arg1 As String)\n\n'
                'End Sub')

        expected = ('# Foo.Bar Method\n\n'
                    'Test description\n\n'
                    '```vb\n'
                    'Public Sub Bar(ByVal Arg1 As String)\n'
                    '```\n\n'
                    '### Parameters\n\n'
                    '**Arg1** `String` <br>\n'
                    'Test Arg1 description\n\n'
                    '## Examples\n\n'
                    'Test example')

        actual = method_parser.MethodParser().make(code, desc)[0].build()
        self.assertEqual(expected, actual)

    def test_makeReturnsSubWithManyParameters(self):
        desc = {'Foo.Bar (String, Long, Variant)': {'description': 'Test description',
                                     'example': 'Test example',
                                     'parameters': {'Arg1': 'Test Arg1 description',
                                                    'Arg2': 'Test Arg2 description',
                                                    'Arg3': 'Test Arg3 description'}}}
        code = ('Attribute VB_Name = \"Foo\"\n'
                'Public Sub Bar(ByVal Arg1 As String, ByVal Arg2 As Long, ByVal Arg3 As Variant)\n\n'
                'End Sub')

        expected = ('# Foo.Bar Method\n\n'
                    'Test description\n\n'
                    '```vb\n'
                    'Public Sub Bar(ByVal Arg1 As String, ByVal Arg2 As Long, ByVal Arg3 As Variant)\n'
                    '```\n\n'
                    '### Parameters\n\n'
                    '**Arg1** `String` <br>\n'
                    'Test Arg1 description\n\n'
                    '**Arg2** `Long` <br>\n'
                    'Test Arg2 description\n\n'
                    '**Arg3** `Variant` <br>\n'
                    'Test Arg3 description\n\n'
                    '## Examples\n\n'
                    'Test example')

        actual = method_parser.MethodParser().make(code, desc)[0].build()
        self.assertEqual(expected, actual)

    def test_makeReturnsFunction(self):
        desc = {'Foo.Bar ()': {'description': 'Test description',
                               'example': 'Test example',
                               'returns': ['String', 'Test returns']}}
        code = ('Attribute VB_Name = \"Foo\"\n'
                'Public Function Bar() As String\n\n'
                'End Function')

        expected = ('# Foo.Bar Method\n\n'
                    'Test description\n\n'
                    '```vb\n'
                    'Public Function Bar() As String\n'
                    '```\n\n'
                    '### Returns\n\n'
                    '`String` <br>\n'
                    'Test returns\n\n'
                    '## Examples\n\n'
                    'Test example')
        actual = method_parser.MethodParser().make(code, desc)[0].build()
        self.assertEqual(expected, actual)

    def test_makeReturnsSubWithError(self):
        desc = {'Foo.Bar ()': {'description': 'Test description',
                               'errors': [
                                   ['OnInvalidArgumentError', 'Test OnInvalidArgumentError'],
                                   ['OnNotImplementedError', 'Test OnNotImplementedError']]}}
        code = ('Attribute VB_Name = \"Foo\"\n'
                'Public Sub Bar()\n\n'
                'End Sub')

        expected = ('# Foo.Bar Method\n\n'
                    'Test description\n\n'
                    '```vb\n'
                    'Public Sub Bar()\n'
                    '```\n\n'
                    '### Errors\n\n'
                    '`OnInvalidArgumentError` <br>\n'
                    'Test OnInvalidArgumentError\n\n'
                    '-or-\n\n'
                    '`OnNotImplementedError` <br>\n'
                    'Test OnNotImplementedError\n\n')

        actual = method_parser.MethodParser().make(code, desc)[0].build()
        self.assertEqual(expected, actual)

    def test_makeReturnsNoDocumentWhenMethodIsNotDefinedInDescription(self):
        desc = {}
        code = ('Attribute VB_Name = \"Foo\"\n'
                'Public Sub Bar()\n\n'
                'End Sub')
                
        actual = method_parser.MethodParser().make(code, desc)
        self.assertEqual(0, len(actual))

    def test_makeReturnsDocumentWhenMethodWithLineContinuationSymbol(self):
        desc = {'Foo.Bar (String, Long, Variant)': {'description': 'Test description',
                                     'example': 'Test example',
                                     'parameters': {'Arg1': 'Test Arg1 description',
                                                    'Arg2': 'Test Arg2 description',
                                                    'Arg3': 'Test Arg3 description'}}}

        code = ('Attribute VB_Name = \"Foo\"\n'
                'Public Sub Bar(ByVal Arg1 As String, _\n'
                '               ByVal Arg2 As Long, _\n'
                '               ByVal Arg3 As Variant)\n'
                'End Sub')

        expected = ('# Foo.Bar Method\n\n'
                    'Test description\n\n'
                    '```vb\n'
                    'Public Sub Bar(ByVal Arg1 As String, ByVal Arg2 As Long, ByVal Arg3 As Variant)\n'
                    '```\n\n'
                    '### Parameters\n\n'
                    '**Arg1** `String` <br>\n'
                    'Test Arg1 description\n\n'
                    '**Arg2** `Long` <br>\n'
                    'Test Arg2 description\n\n'
                    '**Arg3** `Variant` <br>\n'
                    'Test Arg3 description\n\n'
                    '## Examples\n\n'
                    'Test example')

        actual = method_parser.MethodParser().make(code, desc)[0].build()
        self.assertEqual(expected, actual)

if __name__ == "__main__":
    unittest.main()
