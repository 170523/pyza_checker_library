import sys
from io import StringIO
import re
from importlib import import_module
import pathlib

class PyzaChecker:
    def __init__(self, main_script_name = None, test_data_path = None):
        if main_script_name is not None:
            self.main_script = main_script_name
        else:
            self.main_script = 'main'

        if test_data_path is not None:
            test_data_path = pathlib.Path(test_data_path)
        else:
            test_data_path = 'test_data.txt'

        with open(test_data_path, mode = 'r', encoding='utf-8') as f:
            input_strgs = f.read()

        input_strs, output_strs = self.read_input_data(input_strgs)

        self.input_strs = input_strs
        self.output_strs = output_strs

    def run_test(self, test_no = None):
        if test_no is None:
            test_nos = [i + 1 for i in range(len(self.input_strs))]
        else:
            test_nos = [test_no]
    
        for test_no in test_nos:
            test_output = self._do_test(test_no)
            self.check_test_output(test_no)

            if test_output == self.output_strs[test_no - 1]:
                print('>> Correct.')
            else:
                print('>> InCorrect.')
                print('>> Correct Output is')
                print(self.output_strs[test_no - 1])

    def _do_test(self, test_no):

        input_string = self.input_strs[test_no - 1]
        sys.stdin = StringIO(input_string)

        io = StringIO()
        sys.stdout = io

        mod = import_module(self.main_script)

        test_output = io.getvalue()

        sys.stdout = sys.__stdout__
        sys.modules.pop(self.main_script)

        return test_output

    def check_test_output(self, test_no = None):
        if test_no is None:
            test_nos = [i + 1 for i in range(len(self.input_strs))]
        else:
            test_nos = [test_no]
    
        for test_no in test_nos:
            test_output = self._do_test(test_no)
            print(f'===== Test Output NO {test_no} =======')
            print(test_output)
            

    def check_input(self, test_no = None):
        if test_no is None:
            test_nos = [i + 1 for i in range(len(self.input_strs))]
        else:
            test_nos = [test_no]
        
        for test_no in test_nos:
            print(f'===== Input Data of Test NO {test_no} =======')
            print(self.input_strs[test_no - 1])
    
    def check_correct_output(self, test_no = None):
        if test_no is None:
            test_nos = [i + 1 for i in range(len(self.input_strs))]
        else:
            test_nos = [test_no]

        for test_no in test_nos:
            print(f'===== Correct Output of Test NO {test_no} =======')
            print(self.output_strs[test_no - 1])


    def read_input_data(self, input_string):
        input_examples = []
        output_examples = []
        
        # 正規表現パターンの定義
        pattern = r'入力例\d+\n([\s\S]*?)(?=\n出力例\d+|\Z)'
        matches = re.findall(pattern, input_string)
        
        for match in matches:
            input_example = match.strip() + '\n'
            input_examples.append(input_example)
        
        # 出力例を抽出するための正規表現パターン
        pattern = r'出力例\d+\n([\s\S]*?)(?=\n入力例\d+|\Z)'
        matches = re.findall(pattern, input_string)
        
        for match in matches:
            output_example = match.strip() + '\n'
            output_examples.append(output_example)
        
        return input_examples, output_examples