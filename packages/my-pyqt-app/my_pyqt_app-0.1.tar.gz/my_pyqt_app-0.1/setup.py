from setuptools import setup, find_packages

setup(
    name='my_pyqt_app',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'PyQt5',
        # Add other dependencies here
    ],
    entry_points={
        'gui_scripts': [
            'my_pyqt_app = my_pyqt_app.main:main',
        ],
    },
)
