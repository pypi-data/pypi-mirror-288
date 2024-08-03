from setuptools import setup, find_packages

setup(
    name='s1280238_learn',  # パッケージの名前
    version='0.1',  # パッケージのバージョン
    packages=find_packages(),  # パッケージを自動的に見つけて含める
    install_requires=[
        'pami',  # 依存関係として含めるパッケージ
    ],
    author='yuuuuuuuuri',  # あなたの名前
    author_email='yuuri0406@icloud.com',  # あなたのメールアドレス
    description='A learning package',  # パッケージの簡単な説明
    url='https://github.com/yuuuuuuuuri/s1280238_learn',  # GitHubリポジトリのURL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)