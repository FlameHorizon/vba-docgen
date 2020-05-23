import unittest
import module_parser


class TestModuleParser(unittest.TestCase):
    def test_DetectModuleName(self):
        parser = module_parser.ModuleParser()
        code = 'Attribute VB_Name = \"Example\"'
        self.assertEqual('# Example module\n\n', parser.make(code).build())

    def test_MakeReturnsPublicMethods(self):
        parser = module_parser.ModuleParser()
        code = ('Attribute VB_Name = \"Example\"\n'
                'Public Sub Foo1()\n'
                'End Sub\n'
                'Public Function Foo2() As String\n'
                'End Function')

        expected = ('# Example module\n\n'
                    '# Methods\n\n'
                    '|Name|Description|\n'
                    '|-|-|\n'
                    '|[Foo1 ()](./Foo1.md)||\n'
                    '|[Foo2 ()](./Foo2.md)||\n')
        self.assertEqual(expected, parser.make(code).build())

    def test_MakeReturnsMethodsWithArgs(self):
        code = ('Attribute VB_Name = \"Example\"\n'
                'Public Sub Foo1(ByVal Account As String)\n'
                'End Sub\n'
                'Public Function Foo2(ByVal Dt As Date, ByVal City As String) As String\n'
                'End Function\n'
                'Public Sub Foo3(ParamArray Args As Variant())\n'
                'End Sub\n'
                'Public Sub Foo4(ByVal Items As VBA.Collection)\n'
                'End Function\n')

        expected = ('# Example module\n\n'
                    '# Methods\n\n'
                    '|Name|Description|\n'
                    '|-|-|\n'
                    '|[Foo1 (String)](./Foo1.md)||\n'
                    '|[Foo2 (Date, String)](./Foo2.md)||\n'
                    '|[Foo3 (ParamArray Variant())](./Foo3.md)||\n'
                    '|[Foo4 (VBA.Collection)](./Foo4.md)||\n')

        parser = module_parser.ModuleParser()
        self.assertEqual(expected, parser.make(code).build())

    def test_MakeReturnsMethodWithLineContinuationSymbol(self):
        code = ('Attribute VB_Name = \"Example\"\n'
                'Public Sub Foo1(ByVal Bar1 As String, _\n'
                '                ByVal Bar2 As String)\n'
                'End Sub')

        expected = ('# Example module\n\n'
                    '# Methods\n\n'
                    '|Name|Description|\n'
                    '|-|-|\n'
                    '|[Foo1 (String, String)](./Foo1.md)||\n')

        parser = module_parser.ModuleParser()
        self.assertEqual(expected, parser.make(code).build())

    def test_MakeReturnsMethodWithDefaultNumeric(self):
        code = ('Attribute VB_Name = \"Example\"\n'
                'Public Sub Foo1(Optional ByVal Bar1 As Long = 123)\n'
                'End Sub')

        expected = ('# Example module\n\n'
                    '# Methods\n\n'
                    '|Name|Description|\n'
                    '|-|-|\n'
                    '|[Foo1 (Long)](./Foo1.md)||\n')

        parser = module_parser.ModuleParser()
        self.assertEqual(expected, parser.make(code).build())

    def test_MakeReturnsMethodWithDefaultString(self):
        code = ('Attribute VB_Name = \"Example\"\n'
                'Public Sub Foo1(Optional ByVal Bar1 As String = "abc")\n'
                'End Sub')

        expected = ('# Example module\n\n'
                    '# Methods\n\n'
                    '|Name|Description|\n'
                    '|-|-|\n'
                    '|[Foo1 (String)](./Foo1.md)||\n')

        parser = module_parser.ModuleParser()
        self.assertEqual(expected, parser.make(code).build())

    def test_MakeReturnsMethodWithDefaultEnumValue(self):
        code = ('Attribute VB_Name = \"Example\"\n'
                'Public Sub Foo1(Optional ByVal Bar1 As Operation = Operation.Stop)\n'
                'End Sub')

        expected = ('# Example module\n\n'
                    '# Methods\n\n'
                    '|Name|Description|\n'
                    '|-|-|\n'
                    '|[Foo1 (Operation)](./Foo1.md)||\n')

        parser = module_parser.ModuleParser()
        self.assertEqual(expected, parser.make(code).build())

    def test_MakeReturnsMethodWithDefaultStringComa(self):
        code = ('Attribute VB_Name = \"Example\"\n'
                'Public Sub Foo1(Optional ByVal Bar1 As String = ",")\n'
                'End Sub')

        expected = ('# Example module\n\n'
                    '# Methods\n\n'
                    '|Name|Description|\n'
                    '|-|-|\n'
                    '|[Foo1 (String)](./Foo1.md)||\n')

        parser = module_parser.ModuleParser()
        self.assertEqual(expected, parser.make(code).build())

    def test_MakeReturnsModuleWithDescription(self):
        code = ('Attribute VB_Name = \"Example\"')

        descriptions = {'Example': 'Sample description of a module'}

        expected = ('# Example module\n\n'
                    'Sample description of a module\n\n')

        parser = module_parser.ModuleParser()
        self.assertEqual(expected, parser.make(code, descriptions).build())

    def test_MakeReturnsMethodWithDescription(self):
        code = ('Attribute VB_Name = \"Example\"\n'
                'Public Sub Foo1()\n'
                'End Sub\n'
                'Public Sub Foo2(ByVal Bar As Boolean)\n'
                'End Sub\n')

        descriptions = {'Example.Foo1 ()': {'short-description': 'Foo1 description'},
                        'Example.Foo2 (Boolean)': {'short-description': 'Foo2 description'}}

        expected = ('# Example module\n\n'
                    '# Methods\n\n'
                    '|Name|Description|\n'
                    '|-|-|\n'
                    '|[Foo1 ()](./Foo1.md)|Foo1 description|\n'
                    '|[Foo2 (Boolean)](./Foo2.md)|Foo2 description|\n')

        parser = module_parser.ModuleParser()
        self.assertEqual(expected, parser.make(code, descriptions).build())

    def test_MakeReturnsMethodWhenFuctionReturnsVariantArray(self):
        code = ('Attribute VB_Name = \"Foo\"\n'
                'Public Function Bar() As Variant()\n'
                'End Function\n')

        descriptions = {'Foo.Bar ()': {'short-description': 'Bar description'}}

        expected = ('# Foo module\n\n'
                    '# Methods\n\n'
                    '|Name|Description|\n'
                    '|-|-|\n'
                    '|[Bar ()](./Bar.md)|Bar description|\n')

        parser = module_parser.ModuleParser()
        self.assertEqual(expected, parser.make(code, descriptions).build())


if __name__ == "__main__":
    unittest.main()
