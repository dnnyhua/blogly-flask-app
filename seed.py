from models import User, Post, Tag, PostTag, db
from app import app

db.drop_all()
db.create_all()


u1 = User(first_name='Harry', last_name='Bach')
u2 = User(first_name='Mary', last_name='Jane')
u3 = User(first_name='Patrick', last_name='Star')


post1 = Post(title="Top Fruits", content="My top 5 fruits to eat...", user_id ='1')
post2 = Post(title="Top Pizza Restaurants", content="My top 5 pizza restaurants...", user_id='1')
post3 = Post(title="Where to travel this fall", content="New York is worth the visit in the fall.", user_id='1')

post4 = Post(title="Space", content="So much we will never see in one life time.", user_id='2')
post5 = Post(title="Safest car to drive", content="Thinking about buying a car?", user_id='2')


tag1 = Tag(name='pizza')
tag2 = Tag(name='travel')
tag3 = Tag(name='food')
tag4 = Tag(name='fruits')
tag5 = Tag(name='car')
tag6 = Tag(name='space')
tag7 = Tag(name='new york')


ptag1 = PostTag(post_id='1', tag_id ='4') 
ptag2 = PostTag(post_id='1', tag_id ='3') 
ptag3 = PostTag(post_id='2', tag_id ='1') 
ptag4 = PostTag(post_id='2', tag_id ='3') 
ptag5 = PostTag(post_id='3', tag_id ='7') 
ptag6 = PostTag(post_id='3', tag_id ='2') 
ptag7 = PostTag(post_id='4', tag_id ='6') 
ptag8 = PostTag(post_id='5', tag_id ='5') 


db.session.add_all([u1,u2,u3])
db.session.commit()

db.session.add_all([post1, post2, post3, post4, post5])
db.session.commit()

db.session.add_all([tag1, tag2, tag3, tag4, tag5, tag6, tag7])
db.session.commit()

db.session.add_all([ptag1, ptag2, ptag3, ptag4, ptag5, ptag6, ptag7, ptag8])
db.session.commit()


