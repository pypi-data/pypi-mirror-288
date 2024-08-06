import ast

import astor


class MethodParamBodyExtractor(ast.NodeVisitor):

    def extract_method_names(self, astree):

        for child in ast.iter_child_nodes(astree):

            if isinstance(child, ast.FunctionDef):
                self.method_list.append(child.name)
                self.extract_method_names(child)

    def __init__(self, astree):
        self.method_params_and_body_list = {}
        self.method_list = []
        self.extract_method_names(astree)

    def visit_FunctionDef(self, node):
        for method_name in self.method_list:
            if node.name == method_name:
                args = [arg.arg for arg in node.args.args]
                body_ast = ast.parse(''.join(astor.to_source(node) for node in node.body))
                transformer = ReturnToExitTransformer()
                transformed_ast = transformer.visit(body_ast)
                body = astor.to_source(transformed_ast)
                self.method_params_and_body_list[method_name] = (args, body)
            self.generic_visit(node)


class ReturnToExitTransformer(ast.NodeTransformer):
    def visit_Return(self, node):
        assign_node = ast.Assign(
            targets=[ast.Name(id='TMP', ctx=ast.Store())],
            value=node.value
        )
        exit_node = ast.Expr(
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id='sys', ctx=ast.Load()),
                    attr='exit',
                    ctx=ast.Load()
                ),
                args=[],
                keywords=[]
            )
        )
        return [assign_node, exit_node]


class MethodVisitor(ast.NodeVisitor):

    def extract_method_names(self, astree):

        for child in ast.iter_child_nodes(astree):

            if isinstance(child, ast.FunctionDef):
                self.method_list.append(child.name)
                self.extract_method_names(child)

    def __init__(self, astree):
        self.method_list = []
        self.extract_method_names(astree)
        self.method_body_dict = {}

    def visit_FunctionDef(self, node):
        if node.name in self.method_list:
            args = [arg.arg for arg in node.args.args]
            # Convert the entire function node to source code
            method_source = astor.to_source(node)
            self.method_body_dict[node.name] = method_source
        self.generic_visit(node)


def extract_params_and_body(code_str):
    astree = ast.parse(code_str)
    extractor = MethodParamBodyExtractor(astree)
    extractor.visit(astree)
    return extractor.method_params_and_body_list


def extract_names_and_body(code_str):
    astree = ast.parse(code_str)
    extractor = MethodVisitor(astree)
    extractor.visit(astree)
    return extractor.method_body_dict


def extract_method_names(astree):
    if astree is None:
        return []
    method_names = []
    for child in ast.iter_child_nodes(astree):
        if isinstance(child, ast.FunctionDef):
            method_names.append(child.name)
        method_names.extend(extract_method_names(child))
    return method_names


if __name__ == '__main__':
    code_str = """
def f():
    pass

def g():
    pass

def h():
    pass
    
    
    """
    print(extract_method_names(ast.parse(code_str)))
