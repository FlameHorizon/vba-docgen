class ModuleDoc():
    """Represents markdown document on the module level."""

    def __init__(self, name):
        self.name = name
        self.methods = {}

    def build(self):
        output = '# ' + self.name + ' module\n\n'
        if len(self.methods) > 0:
            output += ('# Methods\n\n'
                       '|Name|Description|\n'
                       '|-|-|\n')

            for name in self.methods:
                output += f'|[{name} ({self.__format_args(self.methods[name])})](./{name}.md)||\n'

        return output

    def __format_args(self, args):
        if isinstance(args, list):
            return ', '.join(args)
        else:
            return args

    def addMethod(self, name, args):
        self.methods.update({name: args})
