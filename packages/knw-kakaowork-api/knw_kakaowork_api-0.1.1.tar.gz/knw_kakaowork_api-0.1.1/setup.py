from setuptools import setup, find_packages

setup(
    name='knw_kakaowork_api',
    version='0.1.1',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='archon.oh',
    author_email='archon.oh@knworks.co.kr',
    url='https://github.com/daumsong/kakaowork_api',
    install_requires=['requests',],
    packages=find_packages(exclude=[]),
    keywords=['knw','kakaowork', 'kakaoworkapi', 'work'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
)
