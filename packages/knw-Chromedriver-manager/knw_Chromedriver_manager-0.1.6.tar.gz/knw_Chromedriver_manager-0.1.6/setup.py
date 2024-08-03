from setuptools import setup, find_packages

setup(
    name='knw_Chromedriver_manager',
    version='0.1.6',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='archon.oh',
    author_email='archon.oh@knworks.co.kr',
    url='https://github.com/daumsong/knw_webdriver_manager',
    install_requires=['requests',],
    packages=find_packages(exclude=[]),
    keywords=['knw','webdriver', 'manager', 'selenium'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
)
