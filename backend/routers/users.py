from fastapi import APIRouter, Depends
from backend.database import get_db
from backend.auth import get_current_user, require_admin
import csv, io
from fastapi.responses import StreamingResponse
from backend import models

router = APIRouter()

@router.get('/me')
def me(current_user = Depends(get_current_user)):
    return current_user

@router.get('/download/users')
def download_users(admin = Depends(require_admin), db=Depends(get_db)):
    users = db.query(models.User).all()
    def gen():
        buf = io.StringIO(); w = csv.writer(buf)
        w.writerow(['id','username','email','role','created_at'])
        yield buf.getvalue(); buf.seek(0); buf.truncate(0)
        for u in users:
            w.writerow([u.id, u.username, u.email, u.role, u.created_at.isoformat()])
            yield buf.getvalue(); buf.seek(0); buf.truncate(0)
    return StreamingResponse(gen(), media_type='text/csv', headers={'Content-Disposition':'attachment; filename=users.csv'})
