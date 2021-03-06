try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
        'description': 'Hexapawan AI',
        'author': 'Michael Lane',
        'url': 'http://github.com/mikelane/hexapawn/',
        'download_url': 'https://github.com/mikelane/hexapawn.git',
        'author_email': 'mikelane@gmail.com',
        'version': '1.0',
        'install_requires': [
            'nose',
            'numpy'
        ],
        'packages': ['hexapawn'],
        'scripts': [],
        'name': 'hexapawn'
}

setup(**config)

