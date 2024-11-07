import sys
import os
from io import StringIO
import re
from importlib import import_module
import pathlib

class PyzaChecker:
    def test_repeater(func):
        def wrapper(self, test_no = None):
            if test_no is None:
                test_nos = [i + 1 for i in range(len(self.input_strs))]
            elif isinstance(test_no, int):
                test_nos = [test_no]
            else:
                test_nos = test_no
            
            for test_no in test_nos:
                func(self, test_no)
        return wrapper
    
    def __init__(self, main_script_name = None, test_data_path = None):
        if main_script_name is not None:
            self.main_script = main_script_name
        else:
            self.main_script = 'main'

        if test_data_path is not None:
            test_data_path = pathlib.Path(test_data_path)
        else:
            # カレントディレクトリをsys.pathに加える
            curdir = os.getcwd()
            if curdir not in sys.path:
                sys.path.append(curdir)
            test_data_path = 'test_data.txt'

        with open(test_data_path, mode = 'r', encoding='utf-8') as f:
            input_strgs = f.read()

        input_strs, output_strs = self.read_input_data(input_strgs)

        self.input_strs = input_strs
        self.output_strs = output_strs

    @test_repeater
    def run_test(self, test_no):
        print(f'===== Test NO {test_no} =======')
        print('** Input_Data **')
        print(self.input_strs[test_no - 1])

        # 出力をキャッチする準備
        io = StringIO()
        sys.stdout = io

        self.run_main_script(test_no)
        test_output = io.getvalue() # 出力をキャッチ

        # 出力を標準出力に戻す
        sys.stdout = sys.__stdout__

        print('** main_output **')
        print(test_output)

        if test_output == self.output_strs[test_no - 1]:
            print('>> Correct.')
        else:
            print('>> InCorrect.')
            print('>> Correct Output is')
            print(self.output_strs[test_no - 1])

    @test_repeater
    def run_main_script(self, test_no):
        # 入力値を設定して標準入力にセット
        input_string = self.input_strs[test_no - 1]
        sys.stdin = StringIO(input_string)

        mod = import_module(self.main_script) # メインスクリプトを実行

        sys.modules.pop(self.main_script) # モジュールを削除

    @test_repeater
    def debug(self, test_no):
        print(f'===== Test NO {test_no} =======')
        print('** Input_Data **')
        print(self.input_strs[test_no - 1])
        print('** main_output **')
        self.run_main_script(test_no)
        print('\n')

    @test_repeater
    def check_input(self, test_no):
        print(f'===== Input Data of Test NO {test_no} =======')
        print(self.input_strs[test_no - 1])
    
    @test_repeater
    def check_correct_output(self, test_no):
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
    
