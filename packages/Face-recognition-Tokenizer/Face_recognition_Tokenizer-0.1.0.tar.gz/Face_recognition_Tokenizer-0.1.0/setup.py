# setup.py

from setuptools import setup, find_packages

setup(
    name='Face_recognition_Tokenizer',
    version='0.1.0',
    description='A toolkit for facial recognition and mapping using OpenCV and Dlib.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Nguthirukar/face_recognition_toolkit',
    author='NguthiruKar',
    author_email='nguthirukariuki54@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'opencv-python',
        'dlib',
        'numpy',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
