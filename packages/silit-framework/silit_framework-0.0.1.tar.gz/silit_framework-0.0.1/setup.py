from setuptools import setup, find_packages

setup(
    name='silit_framework',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'silit=silit.commands:create_project',
        ],
    },
    install_requires=[
        'flask',
    ],
    package_data={
        'silit': ['templates/project/**', 'templates/project/app/**', 'templates/project/public/**', 'templates/project/routes/**', 'templates/project/config/**'],
    },
    author='Jiilan Nashrulloh Tanjung',
    author_email='jiilan3maret2008@gmail.com',
    description='SILIT: Scalable Interface for Lightweight Integrated Tooling, Framework for creating desktop applications with MVC structure using Python. Now Under Development.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/jiilanTj/silitframework',  # Ganti dengan URL repositori Anda
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
