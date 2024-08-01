from setuptools import setup, find_packages

setup(
    name='auraflow_client',
    version='0.1.3',
    author='Usama Ali',
    author_email='usamaali012@gmail.com',
    packages=find_packages(),
    description='An auraflow_client library for interacting with the AuraFlow API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'requests>=2.31.0',
        'python-dotenv==1.0.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License'
    ],
    python_requires='>=3.8',
)
