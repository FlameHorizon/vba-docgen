import re
import module_doc
import code_parser


class ModuleParser():
    """This parser is responsible for extracting information from raw VBA code
    which later, can be used for generating markdown document."""

    def make(self, code, descriptions={}):
        """If code does not contains methods definitions, methods section will not be created."""
        # Removes line continuation symbols from declarations
        # to make parsing easier.
        lines = code_parser.remove_continuations_symbols(code).split('\n')

        for ln in lines:
            if 'Attribute VB_Name = "' in ln:
                mod_name = self.__get_mod_name(ln)
                if (mod_name in descriptions):
                    doc = module_doc.ModuleDoc(
                        mod_name, descriptions[mod_name])
                else:
                    doc = module_doc.ModuleDoc(mod_name)

            elif 'Public Sub' in ln or 'Public Function' in ln:
                meth_name = self.__get_method_name(ln)

                args = self.__get_args(ln)
                formatted = self.__format_args(list(args.values()))
                key = mod_name + '.' + meth_name + f' ({formatted})'
                if (key in descriptions):
                    doc.addMethod(meth_name, args,
                                  descriptions[key]['short-description'])
                else:
                    doc.addMethod(meth_name, args)

        return doc

    def __get_mod_name(self, ln):
        dbl_qut = ln.index('\"') + 1
        mod_name = ln[dbl_qut: ln.rindex('\"')]
        return mod_name

    def __get_method_name(self, ln):
        method_type = 'Sub' if ' Sub ' in ln else 'Function'
        name_start = len(f'Public {method_type} ')
        open_parenthesis = ln.index('(')
        return ln[name_start:open_parenthesis]

    def __get_args(self, ln):
        return code_parser.get_args(ln)

    def __remove_defaults(self, ln):
        return re.sub(r' = (\"\w*\"|\w*\.\w*|\"\W*\"|\w*)', '', ln)

    def __format_args(self, args):
        if isinstance(args, list):
            return ', '.join(args)
        else:
            return args

    def __no_args(self, open_parentheses, close_parentheses):
        return open_parentheses + 1 == close_parentheses

    def __remove(self, text, start_index, count):
        """Returns a new string in which a specified number of characters in the current 
        instance beginning at a specified position have been deleted."""

        return text[:start_index] + text[start_index + count:]
