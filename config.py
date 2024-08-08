#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 8000
    APP_ID = os.environ.get("MicrosoftAppId", "41a60c14-5134-47f8-9445-359395b74928")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "3cK8Q~Dh2l6xni8R2cucTOqKrIOOTnWSdJ6RMcqw")
    APP_TYPE = os.environ.get("MicrosoftAppType", "MultiTenantId")
    APP_TENANTID = os.environ.get("MicrosoftAppTenantId", "")
    MicrosoftAppPassword='41a60c14-5134-47f8-9445-359395b74928'
    MicrosoftId='3cK8Q~Dh2l6xni8R2cucTOqKrIOOTnWSdJ6RMcqw'