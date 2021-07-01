import ast


class Metrics:
    def compute_interval(self, node):
        min_lineno = -1
        max_lineno = -1
        for node in ast.walk(node):
            if hasattr(node, 'lineno'):
                min_lineno = min(min_lineno, node.lineno)
                max_lineno = max(max_lineno, node.lineno)
        return (min_lineno, max_lineno)

    def compute_nof_lines(self, min_lineno, max_lineno):
        if min_lineno > max_lineno:
            raise Exception('min_lineno must be smaller than max_lineno')
        return max_lineno - min_lineno

    def get_source(self, source, start_line, end_line):
        return source[start_line:end_line]
