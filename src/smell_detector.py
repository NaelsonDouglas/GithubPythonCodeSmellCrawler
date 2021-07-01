import configparser
import ast

configs = configparser.ConfigParser()
configs.read('configs.ini')
MAX_METHOD_LINES = configs.getint('long_method', 'max_method_lines')

MAX_METHOD_PARAMETERS = configs.getint('long_param_list', 'max_method_parameters')


class SmellDetector:
    def is_long_method(self, nof_lines):
        return nof_lines > MAX_METHOD_LINES

    def is_nested_list_comprehension(self, list_compr_top_node):
        list_compr_tree = iter(ast.walk(list_compr_top_node))
        list_compr_subnode = -1
        list_compr_counter = 0
        while list_compr_subnode is not None and list_compr_counter <= 1:
            try:
                list_compr_subnode = next(list_compr_tree)
                if isinstance(list_compr_subnode, ast.comprehension):
                    list_compr_counter += 1
            except StopIteration:  # There are no more nodes on the subtree
                list_compr_subnode = None
        return list_compr_counter > 1

    def is_long_param_list(self, amount_parameters):
        return amount_parameters > MAX_METHOD_PARAMETERS

    def is_mutable_default_param(self, default_values):
        mutables = [ast.List, ast.Set, ast.Dict]
        for value in default_values:
            if type(value) in mutables:
                return True
        return False

    def is_avoidable_indexing_iterator(self, comprehension_node):
        comprehension_tree = iter(ast.walk(comprehension_node))
        comprehension_subnode = -1
        while comprehension_subnode is not None:
            try:
                comprehension_subnode = next(comprehension_tree)
                iterator = comprehension_subnode.iter
                if 'func' in iterator.__dict__:
                    func = iterator.func
                    if 'id' in func.__dict__ and func.id == 'range':
                        if len(iterator.args) > 0:
                            iterator_args = iterator.args
                            if 'func' in iterator_args[0].__dict__:
                                if 'id' in iterator_args[0].func.__dict__:
                                    arg_id = iterator_args[0].func.id
                                    if arg_id == 'len':
                                        return True
                return False
            except StopIteration:  # There are no more nodes on the subtree
                comprehension_subnode = None

    def is_import_shotgun(self, import_node):
        import_tree = iter(ast.walk(import_node))
        import_subnode = next(import_tree)
        return import_subnode.names[0].name == '*'
