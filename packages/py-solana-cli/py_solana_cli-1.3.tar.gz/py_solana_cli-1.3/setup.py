from setuptools import setup

setup(name='py_solana_cli',
      version='1.3',
      description='SolanaCLI on Python',
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      packages=['py_solana_cli'],
      install_requires=[
        'requests'
      ],
      author_email='hzhz191119111911@gmail.com',
      classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
      ],
      zip_safe=False)

