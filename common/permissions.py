from rest_permission import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    """1. Модератор **должен быть is_staff=True**
       2. Модератор **может просматривать, изменять и удалять** чужие продукты.
       3. Модератор ***не может создавать** продукты (>1запрещен метод POST)
    """
    def has_object_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method == 'POST' and request.user.is_staff:
            return True
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        owner = getattr(obj, 'owner', None)
        return owner == request.user