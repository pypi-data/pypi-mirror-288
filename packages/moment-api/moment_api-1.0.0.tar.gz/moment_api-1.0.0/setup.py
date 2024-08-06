from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='moment_api',
    version='1.0.0',
    description='Moment API: Доступ к LLAMA3 без нагрузки на ваше железо',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Stung',
    author_email='liko.03@bk.ru',
    url='https://github.com/Stunfz',  # Замените на ссылку на ваш репозиторий
    packages=find_packages(),
    install_requires=['requests'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)