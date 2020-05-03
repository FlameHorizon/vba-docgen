import module_doc


class ModuleParser():
    """This parser is responsible for extracting information from raw VBA code
    which later, can be used for generting markdown document."""

    def make(self, code):
        lines = code.split('\n')

        for ln in lines:
            if 'Attribute VB_Name' in ln:
                dbl_qut = ln.index('\"') + 1
                name = ln[dbl_qut: ln.rindex('\"')]
                doc = module_doc.ModuleDoc(name)

            elif 'Public Sub' in ln or 'Public Function' in ln:
                doc.addMethod(self.__get_method_name(ln), self.__get_args(ln))

        return doc.build()

    def __get_method_name(self, ln):
        method_type = 'Sub' if ' Sub ' in ln else 'Function'
        name_start = len(f'Public {method_type} ')
        open_parenthesis = ln.index('(')
        return ln[name_start:open_parenthesis]

    def __get_args(self, ln):
        open_paranthesis = ln.index('(')
        close_paranthesis = ln.rindex(')')

        if self.__no_args(open_paranthesis, close_paranthesis):
            return ''

        # Remove surrounding paranthesis
        args = ln[open_paranthesis + 1: close_paranthesis]

        args_list = args.split(', ')
        output = []

        AS_KEYWORD_LENGTH = 4

        for item in args_list:
            as_keyword_start = item.index(" As ")
            arg_type = item[as_keyword_start + AS_KEYWORD_LENGTH:]
            output.append(arg_type)

        return output

    def __no_args(self, open_paranthesis, close_paranthesis):
        return open_paranthesis + 1 == close_paranthesis

    def __remove(self, text, start_index, count):
        return text[:start_index] + text[start_index + count:]
