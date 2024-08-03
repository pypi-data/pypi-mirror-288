from setuptools import setup, find_packages

setup(
    name='s1300231_learn',  # パッケージの名前
    version='0.1.0',           # バージョン
    packages=find_packages(),  # 自動的にパッケージを検索
    install_requires=[
        'pami',  # ここにpamiパッケージを追加
        # 他に必要な依存パッケージがあればここに追加
    ],
    # 他の必要な設定
    author='Akari Moriya',
    author_email='s1300231@u-aizu.ac.jp',
    description='A short description of your package',
    url='https://github.com/s1300231/s1300231_learn.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
