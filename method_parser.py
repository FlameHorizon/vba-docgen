import re
import method_doc
import code_parser


class MethodParser():
    """Class responsible for parsing VBA methods (both Sub and Function)
    and turning them into specified markdown format."""

    def make(self, code, descriptions={}):

        # Format code such that line continuations symbols and
        # multiple spaces will be removed.
        lines = code_parser.remove_continuations_symbols(code)
        lines = lines.split('\n')

        output = []

        for ln in lines:
            if 'Attribute VB_Name = "' in ln:
                mod_name = self.__get_mod_name(ln)

            elif 'Public Sub' in ln or 'Public Function' in ln:
                meth_name = self.__get_method_name(ln)
                doc = method_doc.MethodDoc(mod_name, meth_name)

                args = self.__get_args(ln)
                formatted = self.__format_args(list(args.values()))
                unique_sig = mod_name + '.' + meth_name + f' ({formatted})'

                # If signature does not exists in the documentation, it means
                # user have to created a documentation for this method yet.
                # Skip line and move to next method.
                if (unique_sig not in descriptions):
                    continue

                json_doc = descriptions[unique_sig]

                doc.set_description(json_doc['description'])
                doc.set_signature(ln)

                for name in args:
                    doc.add_parameter(
                        name, args[name], json_doc['parameters'][name])

                if 'Public Function' in ln:
                    doc.add_returns(json_doc['returns']
                                    [0], json_doc['returns'][1])

                # Insert Errors section only if it was defined by user.
                if ('errors' in json_doc):
                    for name in json_doc['errors']:
                        doc.add_error(name[0], name[1])

                # Insert Example section only if it was defined by user.
                if ('example' in json_doc):
                    doc.set_example(json_doc['example'])

                if ('remarks' in json_doc):
                    doc.set_remarks(json_doc['remarks'])

                output.append(doc)

        return output

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
        """
            Returns dictionary where key is a name of parameter
            and value is parameter type.
        """
        return code_parser.get_args(ln)

    def __format_args(self, args):
        if isinstance(args, list):
            return ', '.join(args)
        else:
            return args
