from setuptools import setup, find_packages

setup(
    name='freezy',
    version='1.3.0',
    description='Automatic speed calculation through DLC coordinates.',
    author='Min Seok Kim',
    author_email='minseok.kim@brain.snu.ac.kr',
    url='https://github.com/minsmis/freezy',
    setup_requires=['numpy', 'pandas', 'plotly', 'openpyxl', 'pyqt6', 'pyqt6-webengine', 'pyqt6-webengine-qt6'],
    packages=find_packages(exclude=[]),
    keywords=['deeplabcut', 'mouse', 'speed', 'freezing'],
    python_requires='>=3.11',
    package_data={},
    classifiers=[
        'Programming Language :: Python :: 3.11'
    ]
)
