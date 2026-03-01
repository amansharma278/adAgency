def is_admin(user):
    return user.is_authenticated and user.role == "ADMIN"


def is_super_admin(user):
    return user.is_authenticated and user.role == "SUPERADMIN"


def is_device(user):
    return user.is_authenticated and user.role == "DEVICE"
