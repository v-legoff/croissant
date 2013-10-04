from distutils.core import setup

setup(
    name='croissant',
    version='0.2',
    author="Vincent Le Goff",
    author_email="vincent.legoff.srs@gmail.com",
    packages=[
            'croissant.language',
            'croissant.language.exceptions',
            'croissant.language.keyword',
            'croissant.organization',
            'croissant.output',
            'croissant.project',
            'croissant.step',
            'croissant.step.exceptions',
            'croissant.story',
            'croissant.tests'
    ],
)
