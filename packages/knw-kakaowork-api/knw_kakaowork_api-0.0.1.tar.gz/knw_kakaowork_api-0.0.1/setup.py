from setuptools import setup, find_packages

setup(
    name='knw_kakaowork_api',
    version='0.0.1',
    description='케이앤웍스 카카오워크 API 모듈입니다.',
    author='archon.oh',
    author_email='archon.oh@knworks.co.kr',
    url='https://github.com/daumsong/kakaowork_api',
    install_requires=['requests',],
    packages=find_packages(exclude=[]),
    keywords=['knw','kakaowork', 'kakaoworkapi', 'work', 'kakao', 'pypi'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
)
