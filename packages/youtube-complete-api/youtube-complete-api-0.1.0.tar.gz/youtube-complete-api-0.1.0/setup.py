from setuptools import setup, find_packages

setup(
    name='youtube-complete-api',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A unified Python package for managing YouTube Data and Transcript APIs.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourgithubusername/youtube-complete-api',
    packages=find_packages(),
    install_requires=[
        'youtube-data-api',  # Make sure to use the correct package names if these are different
        'youtube-transcript-api'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    python_requires='>=3.6',
    keywords='youtube api data transcript video',  # Add relevant keywords
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/yourgithubusername/youtube-complete-api/issues',
        'Source': 'https://github.com/yourgithubusername/youtube-complete-api',
    },
)
