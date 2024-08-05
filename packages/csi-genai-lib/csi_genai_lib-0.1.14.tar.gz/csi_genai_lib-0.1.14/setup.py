# ##################################################################################################
#  Copyright (c) 2024.    Caber Systems, Inc.                                                      #
#  All rights reserved.                                                                            #
#                                                                                                  #
#  CABER SYSTEMS CONFIDENTIAL SOURCE CODE                                                          #
#  No license is granted to use, copy, or share this software outside of Caber Systems, Inc.       #
#                                                                                                  #
#  If used, attribution of open-source code is included where required by original author          #
#                                                                                                  #
#  Filename:  setup.py                                                                             #
#  Authors:  Rob Quiros <rob@caber.com>  rlq                                                       #
# ##################################################################################################

from setuptools import setup, find_packages

setup(
    name='csi_genai_lib',
    version='0.1.14',
    description='Caber GenAI Chat Capture Library',
    author='Rob Quiros',
    author_email='dev@caber.com',
    packages=find_packages(),
    # package_data={
    #     'csi_genai_lib': [
    #         '../csiMVP/Common/config.json',
    #         '../csiMVP/Common/init.py',
    #         '../csiMVP/Common/remote_open.py',
    #         '../csiMVP/Common/tf_config_load.py',
    #         '../csiMVP/Toolbox/aws_init.py',
    #         '../csiMVP/Toolbox/goodies.py',
    #         '../csiMVP/Toolbox/json_encoder.py',
    #         '../csiMVP/Toolbox/retry.py',
    #         '../csiMVP/Toolbox/sqs_init.py',
    #         '../csiMVP/Toolbox/supabase.py',
    #     ],
    # },
    install_requires=[
        # 'pandas==1.5.3',
        # 'numpy==1.26.4',
        # 'packaging==23.2',
        'boto3>=1.18.1',
        'smart-open[s3]>=5.1.0',
        'requests>=2.26.0',
        # 'requests_aws4auth>=1.1.1',
        'urllib3>=1.25.11',
        # 'frozendict',
        # 'dnspython==2.4.0',
        # 'netifaces2>=0.0.18',
        # 'python-nmap>=0.7.1'
    ],
)
