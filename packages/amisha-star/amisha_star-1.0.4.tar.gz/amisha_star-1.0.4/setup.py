from setuptools import setup, find_packages

long_description = ""
with open("README.md") as fid:
    long_description = fid.read()
print(find_packages())

setup(
    name='amisha-star',
    version='1.0.4',
    description='A package for printing various star patterns.',
    long_description="long_description", 
    long_description_content_type='text/plain',  
    author='Amisha',  
    author_email='amishaagarwal397@gmail.com', 
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.12',
    ],
    keywords='printing star pattern',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[],

)
