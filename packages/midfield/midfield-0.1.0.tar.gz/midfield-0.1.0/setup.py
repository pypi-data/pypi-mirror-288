from setuptools import setup, find_packages

setup(
    name='midfield',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    description='A package to validate prompts using an external API.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://midfield.ai',
    author='Midfield Team',
    author_email='admin@midfield.ai',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
