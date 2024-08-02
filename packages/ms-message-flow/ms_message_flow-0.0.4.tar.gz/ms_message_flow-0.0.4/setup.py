import setuptools

setuptools.setup(
    name="ms_message_flow",
    version="0.0.4",
    author="Cayo Slowik",
    author_email="cayo.slowik@brf.com",
    description="Sistema de envio de mensagens",
    url="https://dev.azure.com/brf-corp/Analytics-DataScience/_git/analytics-message-flow",
    packages=setuptools.find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "msal==1.28.0",
        "requests==2.31.0",
        "pymsteams==0.2.2",
        "urllib3==2.2.1"
    ],
)
