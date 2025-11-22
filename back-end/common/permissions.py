from rest_framework import permissions


class GlobalDefaultPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        
        model_permission_codename = self.__get_model_permission_codename(
            method=request.method,
            view=view,
        )

        if not model_permission_codename:
            return False

        return request.user.has_perm(model_permission_codename)

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.method in ["PUT", "PATCH", "DELETE"]:
            if hasattr(obj, "user"):
                return obj.user == request.user
        return True

    def __get_model_permission_codename(self, method, view):
        try:
            model_name = view.queryset.model._meta.model_name
            app_label = view.queryset.model._meta.app_label
            action = self.__get_action_sufix(method)
            return f"{app_label}.{action}_{model_name}"
        except AttributeError:
            return None

    def __get_action_sufix(self, method):
        method_actions = {
            "GET": "view",
            "POST": "add",
            "PUT": "change",
            "PATCH": "change",
            "DELETE": "delete",
            "OPTIONS": "view",
            "HEAD": "view",
        }
        return method_actions.get(method, "")
