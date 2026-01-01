def require_admin(payload: dict):
    if payload.get("role") != "admin":
        raise PermissionError("Admin only")

