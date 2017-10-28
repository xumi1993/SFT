from setuptools import setup, find_packages

setup(
    name = "sft",
    version = "0.1.1",
    url = 'https://github.com/xumi1993/SFT',
    author = 'Mijian Xu',
    author_email = 'gomijianxu@gmail.com',
    packages = find_packages(),
    package_dir = {'sft':'sft'},
    entry_points = {'console_scripts':[
            'get_events = sft.get_events:main',
            'get_resp = sft.get_resp:main',
            'get_stations = sft.get_stations:main',
            'get_synthetics = sft.get_synthetics:main',
            'get_timeseries = sft.get_timeseries:main',
            'get_traveltime = sft.get_traveltime:main'
            ],
            },
    install_requires = ['progressive', 'blessings'],
    include_package_data=True,
    zip_safe=False
)
