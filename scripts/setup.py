from setuptools import setup

setup(
    name='cutouts_soda',
    version='0.2.0',
    py_modules=['cutouts_soda','check_LoTSS_soda','sort_json_soda'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'cutouts_soda = cutouts_soda:cli',
            'sort_json_soda = sort_json_soda:cli',
            'check_LoTSS_soda = check_LoTSS_soda:cli',
        ],
    },
)