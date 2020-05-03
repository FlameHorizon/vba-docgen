import re
import module_doc


class ModuleParser():
    """This parser is responsible for extracting information from raw VBA code
    which later, can be used for generating markdown document."""

    def make(self, code):
        # Removes line continuation symbols from declarations
        # to make parsing easier.
        lines = code.replace(' _\n', '').split('\n')

        for ln in lines:
            if 'Attribute VB_Name = "' in ln:
                dbl_qut = ln.index('\"') + 1
                name = ln[dbl_qut: ln.rindex('\"')]
                doc = module_doc.ModuleDoc(name)

            elif 'Public Sub' in ln or 'Public Function' in ln:
                without_default_values = re.sub(
                    r' = (\"\w*\"|\w*\.\w*|\"\W*\"|\w*)', '', ln)
                doc.addMethod(self.__get_method_name(without_default_values),
                              self.__get_args(without_default_values))

        return doc.build()

    def __get_method_name(self, ln):
        method_type = 'Sub' if ' Sub ' in ln else 'Function'
        name_start = len(f'Public {method_type} ')
        open_parenthesis = ln.index('(')
        return ln[name_start:open_parenthesis]

    def __get_args(self, ln):
        open_parentheses = ln.index('(')
        close_parentheses = ln.rindex(')')

        if self.__no_args(open_parentheses, close_parentheses):
            return ''

        # Remove surrounding parenthesis
        args = ln[open_parentheses + 1: close_parentheses]

        args_list = args.split(', ')
        output = []

        AS_KEYWORD = ' As '
        for item in args_list:
            as_keyword_start = item.index(AS_KEYWORD)
            arg_type = item[as_keyword_start + len(AS_KEYWORD):]
            output.append(arg_type)

        return output

    def __no_args(self, open_parentheses, close_parentheses):
        return open_parentheses + 1 == close_parentheses

    def __remove(self, text, start_index, count):
        """Returns a new string in which a specified number of characters in the current 
        instance beginning at a specified position have been deleted."""

        return text[:start_index] + text[start_index + count:]
