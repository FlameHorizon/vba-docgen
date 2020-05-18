class MethodDoc():
    def __init__(self, namespace, method_sig):
        self.__namespace = namespace
        self.__method_sig = method_sig
        self.__description = ''
        self.__signature = ''
        self.__parameters = {}
        self.__return_type = ''
        self.__return_description = ''
        self.__errors = {}
        self.__example = ''

    def set_description(self, value):
        self.__description = value

    def set_signature(self, value):
        self.__signature = value

    def set_example(self, value):
        self.__example = value

    def get_namespace(self):
        return self.__namespace

    def get_method_sig(self):
        return self.__method_sig

    def build(self):
        output = ''
        output = f'# {self.__namespace}.{self.__method_sig} Method\n\n'

        if self.__description:
            output += f'{self.__description}\n\n'

        if self.__signature:
            output += f'```vb\n{self.__signature}\n```\n\n'

        if self.__parameters:
            output += '### Parameters\n\n'
            for name in self.__parameters:
                output += f'**{name}** `{self.__parameters[name][0]}` <br>\n'
                output += f'{self.__parameters[name][1]}\n\n'

        if self.__return_type:
            output += '### Returns\n\n'
            output += f'`{self.__return_type}` <br>\n'
            output += f'{self.__return_description}\n\n'

        if self.__errors:
            output += '### Errors\n\n'
            value_key = list(self.__errors)[0]
            output += f'`{value_key}` <br>\n'
            output += f'{self.__errors[value_key]}\n\n'

            if (len(self.__errors) > 1):
                self.__errors.pop(list(self.__errors.keys())[0])
                for name in self.__errors:
                    output += '-or-\n\n'
                    output += f'`{name}` <br>\n'
                    output += f'{self.__errors[name]}\n\n'

        if self.__example:
            output += '## Examples\n\n'
            output += self.__example

        return output

    def add_parameter(self, name, param_type, description):
        self.__parameters.update({name: [param_type, description]})

    def add_returns(self, param_type, description):
        self.__return_type = param_type
        self.__return_description = description

    def add_error(self, name, description):
        self.__errors.update({name: description})