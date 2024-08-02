from setuptools import setup, find_packages

setup(
    name='vridgeai',
    version='0.2.8',
    description='vridgeai python package',
    author='byungchan',
    author_email='bgk@vazilcompany.com',
    install_requires=['tensorflow==2.6.0',
                      'keras==2.6.0',
                      'protobuf==3.20.0',
                      'numpy==1.19.3',
                      'matplotlib==3.3.4',
                      'python-dotenv',
                      'requests'
                      ],
    packages=find_packages(exclude=[]),
    keywords=['vazil', 'vazilcompany', 'vridge', 'vridgeai'],
    python_requires='>=3.7, <3.10',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
