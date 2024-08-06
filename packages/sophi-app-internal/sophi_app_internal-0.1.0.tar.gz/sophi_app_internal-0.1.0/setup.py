from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name='sophi-app-internal',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pyjwt',
        'cryptography',
        'python-jose',
        'pydantic',
        'azure-cosmos',
        'python-dotenv',
        'auth0-python',
        'google-api-python-client',
        'google-auth-oauthlib',
        'azure-storage-blob',
        'httpx'
    ],
    long_description=description,
    long_description_content_type="text/markdown"
)