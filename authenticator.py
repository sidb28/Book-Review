from flask import session, redirect, flash
from functools import wraps

def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
      if session.get('user_id'):
        return f(*args, **kwargs)
      else:
        flash("Please Log In to use this feature.")
        return redirect('/login')

  return wrap