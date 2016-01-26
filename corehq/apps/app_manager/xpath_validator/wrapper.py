from collections import namedtuple
from corehq.apps.app_manager.xpath_validator.config import get_xpath_validator_path
from corehq.apps.app_manager.xpath_validator.exceptions import XpathValidationError
from dimagi.utils.subprocess_manager import subprocess_context

XpathValidationResponse = namedtuple('XpathValidationResponse', ['is_valid', 'message'])


def validate_xpath(xpath):
    with subprocess_context() as subprocess:
        path = get_xpath_validator_path()
        p = subprocess.Popen(['node', path], stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate(xpath)
        exit_code = p.wait()
        if exit_code == 0:
            return XpathValidationResponse(is_valid=True, message=None)
        elif exit_code == 1:
            return XpathValidationResponse(is_valid=False, message=stdout)
        else:
            raise XpathValidationError(
                "{path} failed with exit code {exit_code}:\n{stderr}"
                .format(path=path, exit_code=exit_code, stderr=stderr))