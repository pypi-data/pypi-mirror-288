import setuptools

PACKAGE_NAME = "whatsapp-message-vonage-local"
package_dir = PACKAGE_NAME.replace("-", "_")

setuptools.setup(
    name=PACKAGE_NAME,
    version='0.0.23',  # https://pypi.org/project/whatsapp-message-vonage-local
    author="Circles",
    author_email="info@circles.life",
    description="PyPI Package for Circles whatsapp-message-vonage-local",
    long_description="This is a package for sharing common whatsapp function used in different repositories",
    long_description_content_type="text/markdown",
    url=f"https://github.com/circles-zone/{PACKAGE_NAME}-python-package",
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'vonage>=3.11.0',
        'message-local>=0.0.123',
        'logger-local>=0.0.135',
        'database-mysql-local>=0.0.290',
        'api-management-local>=0.0.61',
        'python-sdk-remote>=0.0.93'
    ]
)
