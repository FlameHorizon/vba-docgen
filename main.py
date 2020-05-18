import os
import json
import module_parser
import method_parser

def get_modules(folder_path):
    output = []
    for file in os.listdir(folder_path):
        if file.endswith(".bas"):
            f = open(folder_path + '\\' + file)
            output.append(f.read())

    return output


def delete_folder_content(folder_path):
    pass


if __name__ == "__main__":

    SOURCE_PATH = 'E:\\root\\software\\repos\\private\\Lapis\\src'
    modules = get_modules(SOURCE_PATH)

    OUTPUT_PATH = 'E:\\root\\software\\repos\\private\\vba-doc-py\\output'
    if os.path.exists(OUTPUT_PATH):
        delete_folder_content(OUTPUT_PATH)
    else:
        os.mkdir(OUTPUT_PATH)
    
    with open ('docs-def.json') as f: 
        descriptions = json.load(f)
    
    docs = []

    for mod in modules:
        mod_doc = module_parser.ModuleParser().make(mod, descriptions)
        dir_name = mod_doc.namespace
        if (os.path.exists(f'{OUTPUT_PATH}\\{dir_name}')) == False:
            os.mkdir(f'{OUTPUT_PATH}\\{dir_name}')
        
        f = open(f'{OUTPUT_PATH}\\{dir_name}\\{dir_name}.md', 'w+')
        f.write(mod_doc.build())
        f.close()

    for mod in modules:
        meth_docs = method_parser.MethodParser().make(mod, descriptions)
        for meth_doc in meth_docs:
            dir_name = meth_doc.get_namespace()
            meth_name = meth_doc.get_method_sig()
        
            f = open(f'{OUTPUT_PATH}\\{dir_name}\\{meth_name}.md', 'w+')
            f.write(meth_doc.build())
            f.close()
            