import random
import subprocess
from IPython.core.magic import Magics, magics_class, line_magic
from IPython import get_ipython

try:

    from .global_variable_check import check_global_variable_content, variable_content
    from .local_variable_check import check_local_variable_content
    from .structure_check import check_structure
    from .globals import set_global_var_dict, set_global_method_dict
    from .method_utils import extract_names_and_body
    from .general_check import check, check_syntax, add_missing_global_variables
except ImportError:
    from general_check import check, check_syntax
    from global_variable_check import check_global_variable_content, variable_content
    from local_variable_check import check_local_variable_content
    from structure_check import check_structure
    from globals import set_global_var_dict, set_global_method_dict
    from method_utils import extract_names_and_body



CONFIG = {
    'check_structure': False,
    'modules': ""
}


@magics_class
class MyMagics(Magics):
    def __init__(self, shell):
        super().__init__(shell)
        self.solutions = {}
        self.modules = ""

    @line_magic
    def load(self, line):
        """Load a Python script and extract variables."""
        script_name = line.strip()
        if not script_name:
            print("Please provide a script name.")
            return

        solutions = get_variables_from_pyscript(script_name)
        if not solutions:
            print(f"Could not load any variables from {script_name}.")
        else:
            try:
                self.solutions = solutions['solution']
            except KeyError:
                print("The variable 'solution' is not defined")
                return
            finally:
                print(f"Successfully loaded solutions from: {script_name}")

    @line_magic
    def check(self, line):

        response = get_response()
        task_name = line.strip()
        check_list, answer = self.solutions[task_name]
        if self.modules == "":
            self.modules = CONFIG['modules']
        evaluation_function(response, answer, check_list, self.modules)

    @line_magic
    def load_module(self, line):
        ip = get_ipython()
        cell_lines = ip.user_ns['_ih'][-1].strip().splitlines()
        cell_lines.pop()
        self.modules = "\n".join(cell_lines)
        print("Successfully loaded required modules")


def load_ipython_extension(ipython):
    ipython.register_magics(MyMagics)
    print("Successfully loaded the extension")


def get_variables_from_pyscript(file_path):
    with open(file_path, 'r') as file:
        script_content = file.read()
    variables = {}
    exec(script_content, globals(), variables)
    return variables


def evaluation_function(response, answer, check_list, modules):
    # it needs to append global variables from previous cells

    if isinstance(check_list, str):
        check_list = [var.strip() for var in check_list.split(',')]
    is_defined = True
    if len(check_list) == 0:
        is_defined = False
    wrong_msg = random.choice(["The response is not correct: ", "The code has some problems: ", "Wrong: "])
    correct_msg = random.choice(["Good Job!", "Well Done!", "Awesome"])

    # the missing module and previous global variables should be imported manually:
    response = f"{modules}\n{add_missing_global_variables(response, 'Response')}\n{response}"
    answer = f"{modules}\n{add_missing_global_variables(answer, 'Answer')}\n{answer}"


    general_feedback = check(response)
    is_correct_answer, msg = check_syntax(answer)
    if not is_correct_answer:
        print("SyntaxError: Please contact your teacher to give correct answer!")
        return
    if general_feedback != "General check passed!":
        print(wrong_msg + general_feedback)
        return

    if CONFIG['check_structure']:
        if not check_structure(response, answer):
            print(wrong_msg + "The methods or classes are not correctly defined.")
            return

    if msg:
        if not check_answer_with_output(response, msg):
            # if check_list != 0, it means that output is not the importance
            if len(check_list) == 0:
                error_feedback = "The output is different to given answer: \n"
                print(wrong_msg + error_feedback)
                return
        else:
            print(correct_msg)

            set_global_var_dict(variable_content(response), variable_content(answer))
            set_global_method_dict(extract_names_and_body(response), extract_names_and_body(answer))

            return
    else:
        if check_each_letter(response, answer):
            print(correct_msg)

            set_global_var_dict(variable_content(response), variable_content(answer))
            set_global_method_dict(extract_names_and_body(response), extract_names_and_body(answer))

            return

    if is_defined:

        is_correct, feedback, remaining_check_list, response = check_global_variable_content(response, answer,
                                                                                             check_list)
        if not is_correct:
            print(wrong_msg + feedback)
            return
        else:
            if len(remaining_check_list) == 0:
                print(correct_msg)

                set_global_var_dict(variable_content(response), variable_content(answer))
                set_global_method_dict(extract_names_and_body(response), extract_names_and_body(answer))

                return

        is_correct, feedback = check_local_variable_content(response, answer, remaining_check_list)
        if is_correct:
            if feedback != "NotDefined":
                print(correct_msg)

                set_global_var_dict(variable_content(response), variable_content(answer))
                set_global_method_dict(extract_names_and_body(response), extract_names_and_body(answer))

                return
        else:
            print(wrong_msg + feedback)
            return

    print("The AI feedback functionality will be implemented after permission and security check")


def config(check_structure: bool = False):
    CONFIG['check_structure'] = check_structure


def check_answer_with_output(response, output_msg):
    """
    The function is called iff the answer is unique. i.e. aList = [1,2,3,4,5] is the unique answer
    Notice that styles (at least they can pass general check) are NOT sensitive
    """
    try:
        res_result = subprocess.run(['python', '-c', response], capture_output=True, text=True)
        if res_result.returncode != 0:
            res_feedback = f"Error: {res_result.stderr.strip()}"
        else:
            res_feedback = res_result.stdout.strip()
    except Exception as e:
        res_feedback = f"Exception occurred: {str(e)}"
    return check_each_letter(res_feedback, output_msg)


def check_each_letter(response, answer):
    """
    The function is called iff the answer and the response are unique. i.e. aList = [1,2,3,4,5] is the unique answer and response
    Notice that styles (at least they can pass general check) are NOT sensitive
    """
    return answer.replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "") == response.replace(
        " ", "").replace("\t", "").replace("\n", "").replace("\r", "")


def load_module(modules):
    CONFIG['modules'] = modules
    print("Successfully loaded required modules")


def get_response():
    ip = get_ipython()

    cell_lines = ip.user_ns['_ih'][-1].strip().splitlines()
    cell_lines.pop()
    response_lines = cell_lines
    idx = -2
    while True:
        cell_lines = ip.user_ns['_ih'][idx].strip().splitlines()
        if "get_ipython()" in cell_lines[-1]:
            return ('\n'.join(response_lines)).strip()
        else:
            response_lines = cell_lines + response_lines
            idx -= 1
