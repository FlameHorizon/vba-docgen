import unittest
import module_parser


class TestModuleParser(unittest.TestCase):
    def test_DetectModuleName(self):
        parser = module_parser.ModuleParser()
        code = 'Attribute VB_Name = \"Example\"'
        self.assertEqual('# Example module\n\n', parser.make(code))

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
        self.assertEqual(expected, parser.make(code))

    def test_MakeReturnsMethosWithArgs(self):
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
                    '|[Foo3 (Variant())](./Foo3.md)||\n'
                    '|[Foo4 (VBA.Collection)](./Foo4.md)||\n')

        parser = module_parser.ModuleParser()
        self.assertEqual(expected, parser.make(code))


if __name__ == "__main__":
    unittest.main()
