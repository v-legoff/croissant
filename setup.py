from setuptools import setup

setup(
    name='croissant',
    version='0.3',
    author="Vincent Le Goff",
    author_email="vincent.legoff.srs@gmail.com",
    packages=[
            'croissant.language',
            'croissant.language.exceptions',
            'croissant.language.keyword',
            'croissant.organization',
            'croissant.output',
            'croissant.step',
            'croissant.step.exceptions',
            'croissant.story',
            'croissant.tests'
    ],
    py_modules = ['croissant.bin'],
    entry_points={
        'console_scripts': [
                'croissant = croissant.bin:launch',
        ],
    },
)
