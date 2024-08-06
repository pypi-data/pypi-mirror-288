from setuptools import setup, find_packages

setup(
    name='file-monitor-360',  # Ensure this name is unique
    version='0.1',
    packages=find_packages(),
    install_requires=[],  # Add any dependencies here
    scripts=[
        'main_process.py',
        'file_watcher.py',
        'restart_system.py',
        'error_monitor.py',
        'send_client_info.py'
    ],
    author='manishcode2',
    author_email='manish.singh@swapinfotech.com',
    description='A package for file watching and monitoring',
    # url='https://github.com/yourusername/file_watcher',  # Uncomment and set if available
)
