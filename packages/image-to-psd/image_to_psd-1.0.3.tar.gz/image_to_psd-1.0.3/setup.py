from setuptools import setup, find_packages

setup(
    name='image_to_psd',
    version='1.0.3',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'colorthief',
        'scikit-learn',
        'Pillow',
        'colormath',
        'wand',
        'colorama',
    ],
    tests_require=[
        'unittest',
    ],
    entry_points={
        'console_scripts': [
            # Define any command-line scripts here
        ],
    },
    author='Yatharth Doshi',
    author_email='',
    description='A library for processing images and saving layers as PSD',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yatharth-doshi/PSD_Generator',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)