from crawler import Crawler
from smell_detector import SmellDetector
from metrics_extractor import Metrics
from typed_ast import ast3
import ast
import asttokens
from tqdm import tqdm
import pandas as pd
crawler = Crawler()
smell_detector = SmellDetector()
metrics = Metrics()

repo = crawler.clone_next()
print(repo)
add_header = True
while repo is not None:
        smells = []
        files_info = []
        for path in tqdm(crawler.list_files()):
                names = {}
                with open(path, encoding='utf-8') as stream:
                        try:
                                source = stream.read()
                        except UnicodeDecodeError:
                                continue
                        source_lines = source.split('\n')
                        #repo_name = repo.full_name.split('/')[-1]
                        raw_data = repo._rawData
                        description = raw_data['description'].replace(',',' ')
                        repo_name = raw_data['full_name']
                        forks_count = raw_data['forks_count']
                        watchers_count = raw_data['watchers_count']
                        relative_file_path = stream.name.split(repo_name)[-1]
                        file_nof_lines = len(source_lines)
                        clean_relative_path = relative_file_path.split(repo_name.split('/')[-1])[-1]
                        files_info.append({'repo':repo_name,'file':clean_relative_path,'nof_lines':file_nof_lines,'score':raw_data['score'],'created_at':raw_data['created_at']})
                        try:
                                tree = ast.parse(source, stream.name)
                        except SyntaxError: #There's a syntax error on the code
                                continue
                        atok = asttokens.ASTTokens(source, parse=True)

                        tree_walker = iter(ast.walk(atok.tree))
                        is_attribution = False
                        is_short_lived_comprehension = False
                        for node in tree_walker:
                                is_shallow_copy = False
                                if type(node) is ast.Assign:
                                        is_attribution = True


                                        left_value = node.targets[0]
                                        left_value_name = None
                                        if isinstance(left_value,ast.Attribute):
                                                if isinstance(left_value.value,ast.Name):
                                                        left_value_name = left_value.value.id + '.' + left_value.attr
                                                else:
                                                        left_value_name = None #TODO use recursive attribute finding

                                        elif isinstance(left_value, ast.Name):
                                                left_value_name = left_value.id

                                        if left_value_name is not None:
                                                value_type = node.value
                                                mutables = [ast.List,ast.Set,ast.Dict]
                                                r_value = node.value
                                                if type(r_value) in mutables:
                                                        names[left_value_name] = True
                                                elif type(r_value) == ast.Name:
                                                        if r_value.id in names:
                                                                names[left_value_name] = names[r_value.id]
                                                                is_shallow_copy = True

                                if type(node) is ast.comprehension:
                                        if not is_attribution:
                                                is_short_lived_comprehension = True
                                if type(node) not in [ast.ListComp,ast.Assign, ast.FunctionDef,ast.ClassDef,ast.comprehension,ast.Import,ast.ImportFrom]:
                                        continue
                                interval = atok.get_text_range(node)
                                if 'first_token' in node.__dict__:
                                        start_line = node.first_token.start[0]
                                else:
                                        continue

                                line_url = repo.html_url+'/tree/master'+relative_file_path+f'#L{start_line}'
                                txt = atok.get_text(node)
                                info = {
                                                'repo':repo_name,
                                                'description':description,
                                                'url':line_url,
                                                'line':start_line,
                                                #'txt': description,
                                                'forks_count': forks_count
                                        }


                                if isinstance(node,ast.ListComp):
                                        is_nested_list_comprehension = smell_detector.is_nested_list_comprehension(node)
                                        if is_nested_list_comprehension:
                                                info['smell'] = 'nested_list_comprehension'
                                                smells.append(info)\


                                if isinstance(node,ast.comprehension):
                                        is_avoidable_indexing_iterator = smell_detector.is_avoidable_indexing_iterator(node)
                                        if is_avoidable_indexing_iterator:
                                                info['smell'] = 'avoidable_indexing_iterator'
                                                smells.append(info)


                                if isinstance(node,ast.ImportFrom):
                                        is_import_shotgun = smell_detector.is_import_shotgun(node)
                                        if is_import_shotgun:
                                                info['smell'] = 'import_shotgun'
                                                smells.append(info)


                                if isinstance(node, ast.FunctionDef):
                                        txt_lines = txt.split('\n')
                                        nof_lines = len(txt_lines)
                                        nof_parameters = len(node.args.args)

                                        is_long_method = smell_detector.is_long_method(nof_lines)
                                        if is_long_method:
                                                info['smell'] = 'long_method'
                                                info['name'] = node.name
                                                info['nof_lines'] = nof_lines
                                                smells.append(info)

                                        is_long_param_list = smell_detector.is_long_param_list(nof_parameters)
                                        if is_long_param_list:
                                                info['smell'] = 'long_parameter_list'
                                                info['name'] = node.name
                                                smells.append(info)

                                        is_mutable_default_param = smell_detector.is_mutable_default_param(node.args.defaults)
                                        if is_mutable_default_param:
                                                info['smell'] = 'mutable_default_param'
                                                info['name'] = node.name
                                                smells.append(info)


                                if is_shallow_copy:
                                        info['smell'] = 'shallow_copy'
                                        try:
                                                info['name'] = path.split('/')[-1]
                                        except:
                                                breakpoint()
                                        smells.append(info)


                                if is_short_lived_comprehension:
                                        info['smell'] = 'short_lived_comprehension'
                                        try:
                                                info['name'] = path.split('/')[-1]
                                        except:
                                                breakpoint()
                                        info['nof_lines'] = nof_lines
                                        smells.append(info)
                                        is_short_lived_comprehension = False



        if add_header:
                mode = 'w'
                add_headers = True
                add_header = False
        else:
                mode = 'a'
                add_headers = False
        if len(smells) > 0:
                df = pd.DataFrame(smells,columns=smells[0].keys())
                #df.drop(columns=['txt'],inplace=True)
                smell_name_col = df.pop('smell')
                df.insert(1, 'smell', smell_name_col)
                df.to_csv('smells.csv',mode=mode,header=add_headers,index=False)
        if len(files_info) > 0:
                df = pd.DataFrame(files_info,columns=files_info[0].keys())
                df.to_csv('files_info.csv',mode=mode,header=add_headers,index=False)

        try:
                repo = crawler.clone_next()
        except:
                repo = None