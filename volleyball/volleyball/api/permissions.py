from rest_framework import permissions

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']


class DefaultCreatePermission(permissions.BasePermission):
    message = 'Creating not allowed.'

    def has_permission(self, request, view) -> bool:
        """
        Only allow staff to create
        Get requests are allowed for everyone

        :param request: django request
        :param view: api view
        :return: bool - if user has permission
        """
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff
