import logging
from unittest.mock import MagicMock

from .MockDecorator import MockDecorator

try:
    import zExceptions
    from AccessControl import ModuleSecurityInfo

    security = ModuleSecurityInfo('zms.unibe.helpers.system')  # allow module import in RestrictedPython
except:
    security = MagicMock()  # fallback if no Zope/ZMS context available
    security.public = MagicMock(wraps=MockDecorator())

LOGGER = logging.getLogger('zms.unibe.helpers.system')


print('Helper: zms.unibe.helpers.system.is_authorized')
@security.public
def is_authorized(context,
                  roles: str | list[str] | tuple[str],
                  acquired: bool = False,
                  raise_exception: bool = True) -> bool:
    """
    Helper function to be used in custom Python Scripts or External Methods.
    The execution of such code can thus be limited to users with explicit set
    roles in the given context/client. It can be restricted even for
    ZMSAdministrators and Managers in upper hierarchy levels, e.g., if the
    data is confidential and should not be exposed without explicit permission.

    The user is granted access if they have created the object in the given context.

    Use Case:
     -> assert is_authorized(self, ('ZMSAdministrator', 'ZMSEditor'), acquired=False)
        /manage_survey_data of a specific ZMSSurveyJS should only be
        accessible for users with roles explicitly set in the according client,
        even if they are global ZMSAdministrators or Managers.

    The function determines authorization by comparing the roles assigned to the
    authenticated user in the current context and the roles set within the client's
    object path hierarchy. It may raise an exception if the user is not authorized.

    Args:
        context (object): The context in which the authorization check is performed.
        roles (list of str): List of roles to check against the user's roles.
        acquired (bool, optional): Indicates whether to include roles acquired
            from parent contexts. Defaults to False.
        raise_exception (bool, optional): Determines if an exception should be
            raised when the user is not authorized. Defaults to True.

    Returns:
        bool: True if the user is authorized, otherwise False.

    Raises:
        zExceptions.Unauthorized: If the user is not authorized and
            raise_exception is set to True.
    """
    auth_user = context.REQUEST.get('AUTHENTICATED_USER')

    if context.attr('created_uid') == str(auth_user):
        return True

    try:  # available only in ZMS context
        sec_users = context.getSecurityUsers(acquired=acquired)
        nodes = sec_users.get(str(auth_user), {}).get('nodes', {})
        obj_path_breadcrumbs = context.breadcrumbs_obj_path(portalMaster=acquired)
    except AttributeError:
        nodes = {}
        obj_path_breadcrumbs = []

    # Check if one of the given roles is assigned to the authenticated user
    # and the role is set in the path hierarchy of the current client
    # or in a parent hierarchy if acquired is True.
    obj_path_roles = []
    for obj_path in obj_path_breadcrumbs:
        obj_path_uid = f'{{${obj_path.get_uid()}}}'
        obj_path_roles.extend(nodes.get(obj_path_uid, {}).get('roles', []))

    if isinstance(roles, str):
        roles = (roles,)  # make tuple to avoid search for 'Manager' in string
    has_role_in_obj_path = len([x for x in roles if x in set(obj_path_roles)]) > 0
    has_role_manager = (('Manager' in roles) and
                        ('Manager' in auth_user.getRolesInContext(context)))

    if has_role_in_obj_path or has_role_manager:
        return True
    if raise_exception:
        raise zExceptions.Unauthorized
    return False


print('Helper: zms.unibe.helpers.system.is_dev_or_test')
@security.public
def is_dev_or_test(context) -> bool:

    url = context.REQUEST.get('URL', '')

    return (
            url.startswith('https://edit.cmstest')  # 1, 2, 3, ...
            or url.startswith('https://edit.cmsint.')
            or url.startswith('http://localhost:')
            or url.startswith('http://127.0.0.1:')
    )

# Apply security assertions by ModuleSecurityInfo()
# https://zope.readthedocs.io/en/latest/zdgbook/Security.html#external-modulesecurityinfo-declarations
security.apply(globals())
