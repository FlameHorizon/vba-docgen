class MethodParser():
    def make(self, code):
        return f'# {self.__get_method_name(code)}\n\n```vb\n{code}\n```'

    def __get_method_name(self, ln):
        method_type = 'Sub' if ' Sub ' in ln else 'Function'
        name_start = len(f'Public {method_type} ')
        open_parenthesis = ln.index('(')
        return ln[name_start:open_parenthesis]
