from setuptools import setup, find_packages

setup(
        name='educat-log',
        version='0.2.0',
        packages=find_packages(),
        include_package_data=True,
        description='Modifed version of django-simple-history',
        long_description=open('README.rst').read(),
        long_description_content_type='text/markdown',
        author='Thiago Henrique',
        author_email='thiago@educat.app.br',
        url='https://github.com/devthz/django-simple-history',
        classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
        ],
        install_requires=[
            'django>=2.2',  # e quaisquer outras dependências
        ],
        python_requires='>=3.6',
    )