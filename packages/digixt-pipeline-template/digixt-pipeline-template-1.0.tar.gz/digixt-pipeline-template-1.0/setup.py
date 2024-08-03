from setuptools import setup, find_packages

# Get all directories and files recursively
def package_files(directory):
    import os
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths
 
extra_files =package_files('digixt_pipeline_template/pyspark_template')

setup(
    name='digixt-pipeline-template',
    version='1.0',
    description='DigiXT standard pipeline tempate package',
    author='Merhawi Kiflemariam',
    author_email='merhawi@saal.ai',
    packages=find_packages(),
    package_data={'': extra_files},
    entry_points={
        'console_scripts': [
            'digixt-pipeline-template=digixt_pipeline_template.__main__:main'
        ]
    },
    install_requires=[
        # Add any dependencies here
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
