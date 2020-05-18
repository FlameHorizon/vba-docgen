class ModuleDoc():
    """Represents markdown document on the module level."""

    def __init__(self, namespace, description = ''):
        self.namespace = namespace
        self.methods = {}
        self.description = description

    def build(self):
        output = ('# ' + self.namespace + ' module\n\n')
        if (self.description != ''):
            output = ('# ' + self.namespace + ' module\n\n' + self.description + '\n\n')

        if len(self.methods) > 0:
            output += ('# Methods\n\n'
                       '|Name|Description|\n'
                       '|-|-|\n')

            for name in self.methods:
                args = self.__format_args(self.methods[name][0])
                desc = self.methods[name][1]
                output += f'|[{name} ({args})](./{name}.md)|{desc}|\n'

        return output

    def __format_args(self, args):
        if isinstance(args, list):
            return ', '.join(args)
        else:
            return args

    def addMethod(self, name, args, desc = ''):
        self.methods.update({name: [args, desc]})
