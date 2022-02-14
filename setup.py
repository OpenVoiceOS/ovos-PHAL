from setuptools import setup

setup(
    name='ovos_PHAL',
    version='0.0.1',
    packages=['ovos_PHAL'],
    install_requires=["ovos_utils>=0.0.12", "ovos_workshop"],
    url='https://github.com/OpenVoiceOS/PHAL',
    license='apache-2.0',
    author='jarbasAi',
    author_email='jarbasai@mailfence.com',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'ovos_PHAL=ovos_PHAL.__main__:main'
        ]
    }
)
