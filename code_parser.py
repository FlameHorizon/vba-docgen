import re


def get_args(ln):
    output = {}
    ln = __remove_defaults(ln)
    open_parentheses = ln.index('(')
    if (' Function ' in ln):
        close_parentheses = ln.rfind(')', 0, ln.rindex(' As '))
    else:
        close_parentheses = ln.rindex(')')

    if __no_args(open_parentheses, close_parentheses):
        return output

    # Remove surrounding parenthesis
    args = ln[open_parentheses + 1: close_parentheses]
    args_list = args.split(', ')

    for item in args_list:
        words = item.split(' ')
        if (words[0] == 'Optional'):
            arg_name = words[2]
            arg_type = words[4]

        elif (words[0] == 'ParamArray'):
            arg_name = words[1].replace('(', '').replace(')', '')
            arg_type = 'ParamArray ' + words[3]

        else:
            arg_name = words[1]
            arg_type = words[3]

        output.update({arg_name: arg_type})

    return output


def __remove_defaults(ln):
    return re.sub(r' = (\"\w*\"|\w*\.\w*|\"\W*\"|\w*)', '', ln)


def __no_args(open_parentheses, close_parentheses):
    return open_parentheses + 1 == close_parentheses


def remove_continuations_symbols(code):
    lines = re.sub(' _\n +', '', code)
    lines = re.sub('\,(?=\w)', ', ', lines)
    return lines
