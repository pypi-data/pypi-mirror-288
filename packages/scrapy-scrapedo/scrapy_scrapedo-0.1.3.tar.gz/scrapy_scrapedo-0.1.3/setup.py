from setuptools import setup

setup(
    name='scrapy-scrapedo',
    version='0.1.3',
    url='https://github.com/scrape-do/scrapy-do',
    description='Fundemantal Scrapy support for Scrape.do API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Scrape.do',
    author_email='hello@scrape.do',
    license='MIT',
    packages=['scrapydo'],
    classifiers=[ 
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development :: Libraries',
    'Topic :: Software Development :: Libraries :: Python Modules'
    ],  
    python_requires='>=3.8',
    install_requires=['scrapy'],
)
