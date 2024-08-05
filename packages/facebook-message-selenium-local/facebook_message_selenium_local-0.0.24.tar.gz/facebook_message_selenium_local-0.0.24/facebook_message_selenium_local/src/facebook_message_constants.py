from logger_local.LoggerComponentEnum import LoggerComponentEnum


class FacebookMessageSeleniumLocalConstants:
    """This is a class of all the constants of FacebookMessage"""

    DEVELOPER_EMAIL = 'david.w@circ.zone'

    FACEBOOK_MESSAGE_SELENIUM_LOCAL_PYTHON_PACKAGE_COMPONENT_ID = 293
    FACEBOOK_MESSAGE_SELENIUM_LOCAL_PYTHON_COMPONENT_NAME = 'facebook message selenium'
    FACEBOOK_MESSAGE_SELENIUM_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME = 'FacebookMessage local Python package'

    FACEBOOK_MESSAGE_SELENIUM_LOCAL_PYTHON_CODE_LOGGER_OBJECT = {
        'component_id': FACEBOOK_MESSAGE_SELENIUM_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
        'component_name': FACEBOOK_MESSAGE_SELENIUM_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME,
        'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
        'developer_email': DEVELOPER_EMAIL
    }
    FACEBOOK_MESSAGE_SELENIUM_LOCAL_PYTHON_TEST_LOGGER_OBJECT = {
        'component_id': FACEBOOK_MESSAGE_SELENIUM_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
        'component_name': FACEBOOK_MESSAGE_SELENIUM_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME,
        'component_category': LoggerComponentEnum.ComponentCategory.Unit_Test.value,
        'testing_framework': LoggerComponentEnum.testingFramework.pytest.value,
        'developer_email': DEVELOPER_EMAIL
    }

    # TODO Please import from general system_id.py (where shall we create this?)
    FACEBOOK_SYSTEM_ID=2
    DEFAULT_MESSAGE = 'Test'
    DEFAULT_USERNAME = 'david.w@circ.zone'

    FACEBOOK_MESSAGE_SELENIUM_API_TYPE_ID=18
