from setuptools import setup


setup(
    name='brynq_sdk_google_drive',
    version='0.2.0',
    description='Google Drive wrapper from BrynQ',
    long_description='Groogle Drive wrapper from BrynQ',
    author='BrynQ',
    author_email='support@brynq.com',
    packages=["brynq_sdk.google_drive"],
    license='BrynQ License',
    install_requires=[
        'brynq-sdk-brynq>=1',
        'google-api-python-client>=2,<3',
        'requests>=2,<=3'
    ],
    zip_safe=False,
)