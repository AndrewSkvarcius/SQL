from models import User, Post, Tag, PostTag, db
from app import app

db.drop_all()
db.create_all()

user1 = User(first_name="Jack", last_name="The Ripper")
user2 = User(first_name="Freddy", last_name="Krueger",image_url="https://static.wikia.nocookie.net/villains/images/b/be/TheFreddy.png/revision/latest?cb=20211119081219")
user3 = User(first_name="Michael", last_name="Meyers",image_url="https://t2.gstatic.com/licensed-image?q=tbn:ANd9GcRtd6A5yHjIviCEFWLQWp7aOBeR9gFa7fqWRLgvycSEF0zyErbmAyBrkgg_kgQV6EVp")
user4 = User(first_name="Pin", last_name="Head",image_url="https://upload.wikimedia.org/wikipedia/en/f/fa/Hr3-pinhead2.png")
user5 = User(first_name="Jason", last_name="Voorhees")
user6 = User(first_name="Leather", last_name="Face")
user7 = User(first_name="Norman", last_name="Bates")
user8 = User(first_name="Jig", last_name="Saw")


post1 = Post(title="NightMares", content="Elm st is mine",user_id=2)
post2 = Post(title="Stabby", content="Stab stab stab",user_id=3)
post3 = Post(title="The Box", content="Pleasure Pain",user_id=4)
post4 = Post(title="Murder", content="Your're Mine",user_id=8)
post5 = Post(title="Chainsaw", content="It's Time",user_id=6)
post6 = Post(title="Hello", content="Time to die",user_id=3)
post7 = Post(title="Knife cuts", content="Slice N Dice",user_id=3)
post8 = Post(title="DayMares", content="Rainbows",user_id=3)


tag1 = Tag(name = "nightmares")
ptag1 = PostTag(post_id=1, tag_id=1)




db.session.add(user1)
db.session.add(user2)
db.session.add(user3)
db.session.add(user4)
db.session.add(user5)
db.session.add(user6)
db.session.add(user7)
db.session.add(user8)
db.session.commit()
db.session.add(post1)
db.session.add(post2)
db.session.add(post3)
db.session.add(post4)
db.session.add(post5)
db.session.add(post6)
db.session.add(post7)
db.session.add(post8)
db.session.commit()

db.session.add(tag1)
db.session.commit()
db.session.add(ptag1)
db.session.commit()

