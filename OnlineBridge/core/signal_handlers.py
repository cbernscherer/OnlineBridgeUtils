from OnlineBridge import app
from flask_sqlalchemy import models_committed

@models_committed.connect_via(app)
def on_models_committed(sender, changes):
    for obj, change in changes:
        if change == 'delete' and hasattr(obj, '__commit_delete__'):
            obj.__commit_delete__()