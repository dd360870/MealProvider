from datetime import date, datetime, timedelta

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.model import Restaurant, Order
from flaskr.view.auth import login_required

bp = Blueprint('home', __name__)

@bp.route('/')
def index():
    restaurants = Restaurant.getAll()
    return render_template('home/index.html', restaurants=restaurants)

@bp.route('/orders')
@login_required
def orders(datestr=None):
    datestr = request.args.get('datestr')

    arg_year = date.today().year
    arg_month = date.today().month

    if datestr is not None:
        try:
            t = datetime.strptime(datestr, "%Y-%m")
            arg_year = t.year
            arg_month = t.month
        finally:
            pass

    orders = Order.getHistory(g.user.id, arg_year, arg_month)
    months = Order.getGroupByMonth(g.user.id)

    context = {
        'orders': orders,
        'months': months,
        'arg_year': arg_year,
        'arg_month': arg_month,
    }

    return render_template('home/order.html', **context)

#@bp.route('/create', methods=('GET', 'POST'))
#@login_required
#def create():
#    if request.method == 'POST':
#        title = request.form['title']
#        body = request.form['body']
#        error = None
#
#        if not title:
#            error = 'Title is required.'
#
#        if error is not None:
#            flash(error)
#        else:
#            db = get_db()
#            db.execute(
#                'INSERT INTO post (title, body, author_id)'
#                ' VALUES (?, ?, ?)',
#                (title, body, g.user['id'])
#            )
#            #db.commit()
#            return redirect(url_for('blog.index'))
#
#    return render_template('blog/create.html')
#
#def get_post(id, check_author=True):
#    post = get_db().execute(
#        'SELECT p.id, title, body, created, author_id, username'
#        ' FROM post p JOIN user u ON p.author_id = u.id'
#        ' WHERE p.id = ?',
#        (id,)
#    ).fetchone()
#
#    if post is None:
#        abort(404, f"Post id {id} doesn't exist.")
#
#    if check_author and post['author_id'] != g.user['id']:
#        abort(403)
#
#    return post
#
#@bp.route('/<int:id>/update', methods=('GET', 'POST'))
#@login_required
#def update(id):
#    post = get_post(id)
#
#    if request.method == 'POST':
#        title = request.form['title']
#        body = request.form['body']
#        error = None
#
#        if not title:
#            error = 'Title is required.'
#
#        if error is not None:
#            flash(error)
#        else:
#            db = get_db()
#            db.execute(
#                'UPDATE post SET title = ?, body = ?'
#                ' WHERE id = ?',
#                (title, body, id)
#            )
#            #db.commit()
#            return redirect(url_for('blog.index'))
#
#    return render_template('blog/update.html', post=post)
#
#@bp.route('/<int:id>/delete', methods=('POST',))
#@login_required
#def delete(id):
#    get_post(id)
#    db = get_db()
#    db.execute('DELETE FROM post WHERE id = ?', (id,))
#    #db.commit()
#    return redirect(url_for('blog.index'))