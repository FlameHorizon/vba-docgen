import os
import sys
import json
import shutil
import module_parser
import method_parser


def get_modules(folder_path, excluded):
    output = []
    for file in os.listdir(folder_path):
        base = os.path.basename(file)
        if base in excluded:
            continue

        elif file.endswith(".bas"):
            f = open(folder_path + '\\' + file)
            output.append(f.read())

    return output


def delete_folder_content(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def create_index(mods, descriptions):
    content = '# Index\n\n'

    for mod in mods:
        ns = module_parser.ModuleParser().make(mod, descriptions).namespace
        content += f'- [{ns}](.\{ns}\{ns}.md)\n'
    
    f = open(f'{dest}\\index.md', 'w+')
    f.write(content)
    f.close()


if __name__ == "__main__":

    src = sys.argv[1]
    dest = sys.argv[2]
    doc = sys.argv[3]
    excluded = [x.strip() for x in sys.argv[4].split(',')]

    modules = get_modules(src, excluded)
    
    if os.path.exists(dest):
        delete_folder_content(dest)
    else:
        os.mkdir(dest)

    with open(doc) as f:
        descriptions = json.load(f)

    docs = []

    create_index(modules, descriptions)

    for mod in modules:
        mod_doc = module_parser.ModuleParser().make(mod, descriptions)
        dir_name = mod_doc.namespace
        if (os.path.exists(f'{dest}\\{dir_name}')) == False:
            os.mkdir(f'{dest}\\{dir_name}')

        f = open(f'{dest}\\{dir_name}\\{dir_name}.md', 'w+')
        f.write(mod_doc.build())
        f.close()

    for mod in modules:
        meth_docs = method_parser.MethodParser().make(mod, descriptions)
        for meth_doc in meth_docs:
            dir_name = meth_doc.get_namespace()
            meth_name = meth_doc.get_method_sig()

            f = open(f'{dest}\\{dir_name}\\{meth_name}.md', 'w+')
            f.write(meth_doc.build())
            f.close()
