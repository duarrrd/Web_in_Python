from flask import render_template, flash, redirect, url_for
from app import db
from flask_login import login_required, current_user
from ..pic_upd import save_picture
from .forms import PostForm
from .models import Post, EnumTypes
from . import posts_bp


@posts_bp.route('/', methods=["GET"])
def posts_page():
    return render_template("posts/posts.html", posts=Post.query.all())

@posts_bp.route("/new", methods=["GET", "POST"])
@login_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():

        new_post = Post(
            title=form.title.data,
            text=form.text.data,
            image=save_picture(form.image.data,
                               f'{posts_bp.root_path}/static') if form.image.data else None,
            type=EnumTypes(int(form.type.data)).name,
            enabled=form.enabled.data,
            user_id=current_user.id
        )
        try:
            db.session.add(new_post)
            db.session.commit()
            flash('Post added!', category='success')
            return redirect(url_for("posts.posts_page", id=new_post.id))
        except:
            db.session.rollback()
            flash('Error!', category='danger')

        return redirect(url_for("posts.add_post"))

    return render_template("posts/create_post.html", form=form)

@posts_bp.route('/<int:id>', methods=["GET"])
def post_page(id):
    post = Post.query.get_or_404(id)
    if not post.enabled and post.user.id != current_user.id:
        return redirect(url_for("posts.posts_page"))

    return render_template("posts/post.html", post=post)


@posts_bp.route("/update/<int:id>", methods=["GET", "POST"])
def update_post(id):
    post = Post.query.get_or_404(id)

    if current_user.id != post.user.id:
        return redirect(url_for("posts.posts_page", id=id))

    form = PostForm(obj=post)

    if form.validate_on_submit():

        post.title = form.title.data
        post.text = form.text.data
        post.type = form.type.data
        post.enabled = form.enabled.data

        if form.image.data:
            post.image = save_picture(form.image.data, f'{posts_bp.root_path}/static')

        try:
            db.session.commit()
            flash(f'Post({post.id}) updated!', category='success')
            return redirect(url_for("posts.post_page", id=id))
        except:
            db.session.rollback()
            flash('Error!', category='danger')

        return redirect(url_for("posts.update_post", id=id))

    form.type.data = str(post.type.value)
    form.enabled.data = post.enabled
    return render_template("posts/update_post.html", form=form, post=post)


@posts_bp.route("/delete/<int:id>", methods=["POST"])
def delete_post(id):
    post = Post.query.get_or_404(id)

    if current_user.id == post.user.id:
        try:
            db.session.delete(post)
            db.session.commit()
            flash(f'Post({post.id}) deleted!', category='success')
        except:
            db.session.rollback()
            flash('Error!', category='danger')

    return redirect(url_for("posts.posts_page"))