from logger_local.LoggerComponentEnum import LoggerComponentEnum


class FacebookLocalConstants:
    DEVELOPER_EMAIL = 'neomi.b@circ.zoce'

    COMPONENT_ID = 245
    COMPONENT_NAME = 'Profile facebook selenium scraper'

    CODE_LOGGER_OBJECT = {
        'component_id': COMPONENT_ID,
        'component_name': COMPONENT_NAME,
        'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
        'developer_email': DEVELOPER_EMAIL
    }

    TEST_LOGGER_OBJECT = {
        'component_id': COMPONENT_ID,
        'component_name': COMPONENT_NAME,
        'component_category': LoggerComponentEnum.ComponentCategory.Unit_Test.value,
        'developer_email': DEVELOPER_EMAIL
    }

    UNKNOWN_FACEBOOK_ID = 0
