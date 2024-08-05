from setuptools import setup, find_packages

setup(
    name='linkedin-job-search',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4'
    ],
    entry_points={
        'console_scripts': [
            'linkedin_search_job=linkedin_search_job.scraper:main',
        ],
    },
    author='Toshar Saini',
    author_email='tusharsaini503@gmail.com',
    description='A package Search jobs from Linkdin',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Tushar503/linkedin-search-job',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
