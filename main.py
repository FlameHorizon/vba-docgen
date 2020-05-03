import os
import module_parser



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

    SOURCE_PATH = 'E:\\root\\software\\repos\\vba-doc-py\\inputs'
    modules = get_modules(SOURCE_PATH)

    OUTPUT_PATH = 'E:\\root\\software\\repos\\vba-doc-py\\output'
    if os.path.exists(OUTPUT_PATH):
        delete_folder_content(OUTPUT_PATH)
    else:
        os.mkdir(OUTPUT_PATH)

    docs = []
    for mod in modules:
        docs.append(module_parser.ModuleParser().make(mod))

    for i in range(0, len(docs)):
        f = open(f'{OUTPUT_PATH}\\markdown{i}.md', 'w+')
        f.write(docs[i])
        f.close()

    pass

    # For each public method in module, one markdown file will be created.