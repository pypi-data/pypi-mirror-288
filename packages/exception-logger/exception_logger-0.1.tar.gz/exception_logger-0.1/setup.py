from setuptools import setup, find_packages

setup(
    name="exception_logger",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask==2.0.3",
        "Werkzeug==2.0.2",
        "mysql-connector-python==8.0.27",
        "python-dotenv==0.19.2"
    ],
    # No entry_points needed for this setup
)
