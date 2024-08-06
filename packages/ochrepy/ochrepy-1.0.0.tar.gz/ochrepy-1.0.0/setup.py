from setuptools import setup

with open("README.md") as f:
    long_description = f.read()

memcache_cache_reqs = [
    'pymemcache>=3.5.2'
]

extra_reqs = {
    'memcache': memcache_cache_reqs
}

setup(
    name='ochrepy',
    version='1.0.0',
    description='A light weight Python library for the Ochre Web API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Jopgood",
    author_email="jehopgood@gmail.com",
    project_urls={
        'Source': 'https://github.com/Jopgood/ochrepy',
    },
    python_requires='>3.8',
    install_requires=[
        "requests>=2.25.0",
        "urllib3>=1.26.0"
    ],
    extras_require=extra_reqs,
    license='MIT',
    packages=['ochrepy'])