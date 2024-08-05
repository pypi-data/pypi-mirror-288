from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize
import site
from setuptools.command.install import install
import os
import shutil

extensions = [
	Extension(
		"imagingai.ImagingAI",  # Module name
		["imagingai/ImagingAI.c"],  # Source file
	)
]

cythonize_options = {
	'compiler_directives': {
		'language_level': 3,
		'emit_code_comments': False,
	}
}

so_files_dir = os.path.join('.', 'extensions')
# List all .so files in the specified directory
so_files = [os.path.join(so_files_dir, f) for f in os.listdir(so_files_dir) if f.endswith('.so')]
site_packages_dir = os.path.join('.', 'extensions')

setup(
    name='imagingai',
    version='2.99',
    description='EKY Imaging AI Package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='ImagingAI',
    author_email='license@mit.edu',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
        'cryptography',
    ],
    ext_modules=cythonize(extensions, **cythonize_options),
	packages=['imagingai'],
    include_package_data=True,
    package_data={
        'imagingai': [
            'extensions/*.so',  # Use wildcard to include all .so files in the extensions directory
        ],
    },
    data_files=[
        (site_packages_dir, so_files), 
    ]
)