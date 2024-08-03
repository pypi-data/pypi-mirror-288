from setuptools import setup, find_packages # type: ignore

with open('README.md', encoding='utf-8') as f:
    readme = f.read()

setup(
        name="log95",
        version="1.2",
        author="kuba201",
        description='Simple logger',
        long_description=readme,
        long_description_content_type='text/markdown',
        packages=find_packages(),
        url="https://flerken.zapto.org:1115/kuba/log95",
        install_requires=["colorama"],
        project_urls={
            'Source': 'https://flerken.zapto.org:1115/kuba/log95',
        },
        keywords=[],
        classifiers= [
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: 3.10",
            "Development Status :: 5 - Production/Stable",
        ]
)