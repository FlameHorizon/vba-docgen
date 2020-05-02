class ModuleDoc():
    def __init__(self, name):
        self.name = name
        self.subs = {}

    def build(self):
        output = '# ' + self.name + ' module\n\n'
        if len(self.subs) > 0:
            output += ('# Methods\n\n'
                       '|Name|Description|\n'
                       '|-|-|\n')

            for name in self.subs:
                output += f'|[{name} ({self.__format_args(self.subs[name])})](./{name}.md)||\n'

        return output

    def __format_args(self, args):
        if isinstance(args, list):
            return ', '.join(args)
        else:
            return args

    def addMethod(self, name, args):
        self.subs.update({name: args})
