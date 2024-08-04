# my_extension.py
import random
import subprocess

from IPython import get_ipython
from .general_check import check, check_syntax
from IPython.core.magic import Magics, magics_class, line_magic
from .global_variable_check import check_global_variable_content
from .local_variable_check import check_local_variable_content
from .structure_check import check_structure

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
        # Get the cell content up to this point
        ip = get_ipython()
        response_lines = ip.user_ns['_ih'][-1].strip().splitlines()
        response_lines.pop()
        response = '\n'.join(response_lines)
        task_name = line.strip()
        check_list, answer = self.solutions[task_name]
        if self.modules == "":
            self.modules = CONFIG['modules']
        evaluation_function(response, answer, check_list, self.modules)

    @line_magic
    def load_module(self, line):
        ip = get_ipython()
        module_lines = ip.user_ns['_ih'][-1].strip().splitlines()
        module_lines.pop()
        modules = ('\n'.join(module_lines)).strip()
        self.modules = modules
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
    if isinstance(check_list, str):
        check_list = [var.strip() for var in check_list.split(',')]
    is_defined = True
    if len(check_list) == 0:
        is_defined = False
    wrong_msg = random.choice(["The response is not correct: ", "The code has some problems: ", "Wrong: "])
    correct_msg = random.choice(["Good Job!", "Well Done!", "Awesome"])

    # the missing module should be imported manually:
    response = f"{modules}\n{response}"
    answer = f"{modules}\n{answer}"

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
            return
    else:
        if check_each_letter(response, answer):
            print(correct_msg)
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
                return

        is_correct, feedback = check_local_variable_content(response, answer, remaining_check_list)
        if is_correct:
            if feedback != "NotDefined":
                print(correct_msg)
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
