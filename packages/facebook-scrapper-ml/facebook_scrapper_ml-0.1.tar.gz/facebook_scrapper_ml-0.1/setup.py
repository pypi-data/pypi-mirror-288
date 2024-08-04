from setuptools import setup, find_packages

setup(
    name='facebook_scrapper_ml',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'joblib',
        'numpy',
        'pandas',
        'scikit-learn',
        'scipy',
        'selenium',
        'streamlit',
        'webdriver-manager',
        'matplotlib',
        'fastapi',
        'pydantic',
        'uvicorn'

    ],
    package_data={
        '': ['data/*', 'tests/*'],
    },
    description='Facebook Scrapper',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Intended Audience :: Education',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
)
