import setuptools

description = "Asynchronous League Of Legends API Wrapper"
long_description = open("README.md").read()
version="1.0.0"

packages = ['lolbanana']

setuptools.setup(
    name='League of Bananas',
    version=version,
    description=description,
    long_description=long_description,
    url='https://github.com/bananaboy21/league-of-bananas',
    author='dat banana boi',
    author_email='kang.eric.hi@gmail.com',
    license='MIT',
    packages=packages,
    include_package_data=True,
    install_requires=['aiohttp>=2.0.0']
)
