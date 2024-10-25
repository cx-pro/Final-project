from app.utils.imports import *
from app.models import UserM


def getUsers(): return {str(x.id): x for x in UserM.query.all()}
