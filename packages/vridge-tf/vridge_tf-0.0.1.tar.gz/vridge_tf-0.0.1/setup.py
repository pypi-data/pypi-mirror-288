from setuptools import setup, find_packages

setup(
    name='vridge_tf',
    version='0.0.1',
    description='vridge 텐서플로우 패키지',
    author='byungchan',
    author_email='bgk@vazilcompany.com',
    install_requires=['tensorflow==2.6.0',
                      'keras==2.6.0',
                      'numpy==1.19.2',
                      ],
    packages=find_packages(exclude=[]),
    keywords=['vazil', 'vazilcompany', 'vridge', 'vridge_tf'],
    python_requires='>=3.7, <3.8',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.7'
    ],
)
