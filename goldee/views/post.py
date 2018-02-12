from flask import Blueprint, render_template, request
from werkzeug import secure_filename
import hashlib
import os

from goldee.database import insertSimple, activatePendingPost, getPost, getNewPostID
from goldee.forms import PostForm
from goldee.models import Post, PendingPost
from goldee.goldeeEmail import sendEmailNewPost

PostBP = Blueprint('/post', __name__, template_folder = "../frontEndFiles")

@PostBP.route('/new', methods = ['GET', 'POST'])
def newPost():
	form = PostForm()
	if form.validate_on_submit():
		post = Post()
		post.Status = 'Pending'
		post.PostType = form.postType.data
		post.Title = form.title.data
		post.Description = form.description.data
		post.CategoryID = form.category.data
		post.AuthorName = form.authorName.data
		post.Email = form.email.data
		post.Address1 = form.address1.data
		post.Address2 = form.address2.data
		post.City =  form.city.data
		post.State = form.state.data
		post.Zip = form.zipCode.data
		#post.Picture = form.picture.data.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(form.picture.data))) 
		insertSimple(post)

		postID = getNewPostID(post.AuthorName, post.Title, post.Description)
		postIDHash = hashlib.md5(postID).hexdigest()
		postLink = "www.gogoldee.com/post/new/" + postIDHash

		pendingPost = PendingPost()
		pendingPost.PostID = postID
		pendingPost.HashValue = postIDHash
		insertSimple(pendingPost)

		sendEmailNewPost(post.Email, post.AuthorName, post.Title, post.Description, postLink)
	return render_template('index.html', form = form)

@PostBP.route('/new/<postHash>', methods = ['GET'])
def newPendingPost(postHash):
	activatePendingPost(postHash)

@PostBP.route('/<postID>', methods = ['GET'])
def getPost(postID):
	post = getPost(postID) # may need to change how getPost is implemented b/c we might need to return model object instead of query object.
	return render_template('postPage.html', post = post)