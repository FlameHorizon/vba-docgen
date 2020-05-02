import unittest
import method_parser


class TestModuleDoc(unittest.TestCase):
    def test_MakeReturnsSub(self):
        self.__test_declaration('Start', 'Public Sub Start()')

    def __test_declaration(self, name, declaration):
        expected = (f'# {name}\n\n'
                    '```vb\n'
                    f'{declaration}\n'
                    '```')
        self.assertEqual(
            expected, method_parser.MethodParser().make(declaration))

    def test_MakeReturnsSubWithArgument(self):
        self.__test_declaration('Start', 'Public Sub Start(ByVal Dt As Date)')

    def test_MakeReturnsFunc(self):
        self.__test_declaration('Start', 'Public Function Start() As Boolean')

    def test_MakeReturnsFuncWithArgs(self):
        self.__test_declaration(
            'Start', 'Public Function Start(ByVal Str As String, ByVal Value As String) As Boolean')


if __name__ == "__main__":
    unittest.main()
