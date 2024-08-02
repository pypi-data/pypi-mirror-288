from setuptools import find_packages, setup


packages = find_packages()

print(packages)

setup(
    name="flow_matching",
    version="0.0.1",
    packages=packages,
    setup_requires=["wheel"],
)