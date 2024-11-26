from setuptools import setup, find_packages
from setuptools.command.install import install
from sbf.service_binding_files import get_service_binding_root, get_service_binding_files, as_plain_list

class PostInstallCommand(install):
    def run(self):
        install.run(self)
        service_binding_root = get_service_binding_root()
        service_binding_files = get_service_binding_files(service_binding_root)
        raise Exception(as_plain_list(service_binding_files))

setup(
    name='sbf-tests',
    version='0.0.1',
    packages=find_packages(),
    cmdclass={
        'install': PostInstallCommand,
    },
)

