from setuptools import setup

setup(
    name='MVDOSINT',
    version='0.1',
    description='Модуль MVDOSINT',
    author='Ваше имя',
    author_email='ваш_email@example.com',
    packages=['mvdosint'],
    install_requires=['pip', 'setuptools'],
    entry_points={
        'console_scripts': [
            'cybermvd = mvdosint.mvd:main'
        ],
    }
)
