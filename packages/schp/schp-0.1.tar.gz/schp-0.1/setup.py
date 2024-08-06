from setuptools import setup, find_packages


install_requires = [
    'pillow', 
    'tqdm', 
    'Ninja', 
    'opencv-python', 
    'torch', 
    'torchvision', 
    'torchaudio', 
    'gdown', 
]


setup(
    name='schp', 
    version='0.1',
    packages=find_packages(),
    package_data={
        'schp': [
            'modules/src/*.h',
            'modules/src/*.cpp',
            'modules/src/*.cu',
            'modules/src/utils/*.h',
            'modules/src/utils/*.cuh',
        ],
    },
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
        ],
    },
    author='BbChip0103',
    author_email='bbchip13@gmail.com',
    description='Package of Self Correction for Human Parsing',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/BbChip0103/Self-Correction-Human-Parsing',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    keywords="human, parser, clothes, segmentation",
)
