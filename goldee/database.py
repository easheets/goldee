from goldee.models import db, User, Category

# insert, Get, Update

def insertSimple(insertModel):
    try:
        db.session.add(insertModel)
        db.session.commit()
    except:
        raise

'''
def testDBEverything():
    try:
        user = User()
        user.FirstName = 'Bob'
        user.LastName = 'Yes'
        user.Email = 'Bob@bob'
        user.Address1 = 'y'
        user.City = 's'
        user.State = 'YO'
        user.Zip = 12345
        user.Picture = 'yes/yes/yes.jpg'
        user.HashValue = 'asldkjfhlsado'
        db.session.add(user)
        db.session.commit()
    except:
        raise

    try:
        userQuery = db.session.query(User.FirstName, User.Zip).all()
        print(userQuery)
    except:
        raise

    try:
        db.session.query(User).delete()
        db.session.commit()
    except:
        raise
'''

def getSubcategories(categoryID):
    try:
        subcategoriesQuery = db.session.query(Subcategory.SubcategoryID, Subcategory.Name).\
         filter_by(Subcategory.CategoryID == categoryID).\
         order_by(Subcategory.Name).all()
        subcategories = [(subcategory.SubcategoryID, subcategory.Name) for subcategory in subcategoriesQuery]
        return subcategories
    except:
        raise


def getCategories():
    try:
        categoriesQuery = db.session.query(Category.CategoryID, Category.Name).\
         order_by(Category.Name).all()
        categories = []
        for cat in categoriesQuery:
           category = Category()
           category.CategoryID = cat.CategoryID
           category.Name = cat.Name
           categories.add(Category)
        #categories = [(category.CategoryID, category.Name) for category in categoriesQuery]
        return categories
    except:
        raise

#def insertSubcategories():


def getPost(postID):
    try:
        #tmp = Post.PostID
        #Post.PostID = postID
        postQuery = db.session.query(Post.PostID, Post.AuthorName, Post.Title, Post.Description, Post.Picture, Post.CategoryID, Post.Date, Post.Type).\
	filter(Post.PostID == postID).one()
    except:
        raise
    return postQuery
        #post = Post()
        #post.PostID = postQuery.PostID
        #post.Title = postQuery.Title
        #post.Description = postQuery.Description
        #post.CategoryID = postQuery.CategoryID
        #post.AuthorName = postQuery.AuthorName
        #post.postDate = postQuery.Date
        #post.Picture


