from flask import Blueprint, render_template, request, redirect, flash

from goldee.models import Post, PendingPost, ReportedPost
from goldee.forms import PostForm, ReportForm, PostReplyForm
from goldee.database import insertSimple, activatePendingPost, getUserPost, reactivatePost, getPostDetails, insertNewPostAsPending
from goldee.goldeeEmail import sendEmailNewPost, sendEmailNewPostReply

# Creates blueprints for all routes with prefix /post
PostBP = Blueprint('/post', __name__, template_folder = "../frontEndFiles/dist")

# Mapped to /post/new endpoint
# Redirects on success
# Returns file at frontEndFiles/dist/static/newpost_form.html with rendered form
@PostBP.route('/new', methods = ['GET', 'POST'])
def newPost():
	form = PostForm()
	if form.validate_on_submit(): # if Post request and all fields validate
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

		'''
		create posthash for pending post
		Pending post entry only lives until the post is activated.
		Since we did not have user persistence, we needed a way to uniquely identify posts and keep access to them
		somewhat secure
		'''
		# Once application has user persistence, can remove PendingPost and keep activation behind @login_required so only
		# the user can change the post's properties (i.e. activate/reactivate/edit).
		try:
			postHash = insertNewPostAsPending(post)
			postLink = "www.gogoldee.com/post/new/" + postHash
		except:
			flash("We're sorry, something went wrong. Please try again.")
			return render_template('static/newpost_form.html', form = PostForm())

		sendEmailNewPost(post.Email, post.AuthorName, post.Title, post.Description, postLink)
		flash("Your post has been saved. Please check your email to confirm posting!")
		return redirect('/feedwall')
	return render_template('static/newpost_form.html', form = form)

# Activates a pending post. Only way to get to this link is through email
@PostBP.route('/new/<postHash>', methods = ['GET'])
def newPendingPost(postHash):
	postID = activatePendingPost(postHash)
	flash("Your post has been activated!")
	return redirect('/post/' + postID)

# Returns the post with the provided postID
@PostBP.route('/<postID>', methods = ['GET'])
def getPost(postID):
	post = getUserPost(postID)
	return render_template('static/getpost_form.html', post = post)

# Renews the post with the provided postID
@PostBP.route('/<postID>/renew', methods = ['GET'])
def renewPost(postID):
	reactivatePost(postID)
	return redirect('/post/' + postID)

# Returns a form to report the post with the provided postID and inserts into database
@PostBP.route('/<postID>/report', methods = ['GET', 'POST'])
def reportPost(postID):
	form = ReportForm()
	if form.validate_on_submit():
		report = ReportedPost()
		report.PostID = postID
		report.Reason = form.reason.data
		report.Body = form.body.data
		try:
			insertSimple(report)
		except:
			flash("We're sorry, something went wrong. Please try again.")
			return redirect('/' + postID + '/report') 

		flash("Your report has been submitted")
		return redirect('/')

	return render_template('static/reportpost_form.html', form = form)

# Returns a form to reply to the post with provided postID. Sends the post author an email.
@PostBP.route('/<postID>/reply', methods = ['GET', 'POST'])
def replyPost(postID):
	form = PostReplyForm()
	if form.validate_on_submit():
		post = getPostDetails(postID)
		toAddress = post.Email
		toName = post.AuthorName
		postHeadline = post.Title
		contactEmail = form.email.data
		contactName = form.authorName.data
		contactMessage = form.message.data

		sendEmailNewPostReply(toAddress, toName, postHeadline, contactEmail, contactName, contactMessage)

		flash("Your reply has been sent!")
		return redirect('/')
	
	return render_template('static/replypost_form.html', form = form)



