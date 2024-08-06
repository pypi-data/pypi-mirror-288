"""
@Author: kang.yang
@Date: 2024/8/6 10:50
"""
import os
import sys
from . import __version__


ignore_content = '''report
screenshot
.idea
.pytest_cache
__pycache__
debug.py
venv
'''


api_run = '''import kytest


if __name__ == '__main__':
    kytest.main(
        host='',
        headers={},
        path='tests'
    )
'''

api_debug = '''import kytest


if __name__ == '__main__':
    kytest.main(
        host='',
        headers={},
        path='tests/test_demo.py'
    )
'''

app_run = '''import kytest


if __name__ == '__main__':
    kytest.main(
        did='',
        pkg='',
        path='tests'
    )
'''

app_debug = '''import kytest


if __name__ == '__main__':
    kytest.main(
        did='',
        pkg='',
        path='tests/test_demo.py'
    )
'''

web_run = '''import kytest


if __name__ == '__main__':
    kytest.main(
        web_host='',
        headers={},
        path='tests'
    )
'''

web_debug = '''import kytest


if __name__ == '__main__':
    kytest.main(
        web_host='',
        headers={},
        path='tests/test_web.py'
    )
'''


def create_scaffold(platform):
    """create scaffold with specified project name."""

    def create_folder(path):
        os.makedirs(path)
        msg = f"created folder: {path}"
        print(msg)

    def create_file(path, file_content=""):
        with open(path, "w", encoding="utf-8") as f:
            f.write(file_content)
        msg = f"created file: {path}"
        print(msg)

    # 新增测试数据目录
    create_folder("tests")
    create_folder("data")
    create_file('.gitignore', ignore_content)
    create_file('requirements.txt', f'kytest=={__version__}')
    create_file(os.path.join('tests', 'test_demo.py'), '# 根据项目demo编写用例脚本')
    # 新增安卓测试用例
    if platform in ("android", "ios"):
        create_file('run.py', app_run)
        create_file('debug.py', app_debug)
    elif platform == "web":
        create_file('run.py', web_run)
        create_file('debug.py', web_debug)
    elif platform == "api":
        create_file('run.py', api_run)
        create_file('debug.py', api_debug)
    else:
        print("请输入正确的平台: android、ios、web、api")
        sys.exit()
