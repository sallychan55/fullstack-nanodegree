from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_setup import Base, Shop, ShoppingItem, User

engine = create_engine('sqlite:///shopitemswithusers.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create a user
User1 = User(name="Sally Skst", email="sallyskst@example.com", picture='')
session.add(User1)
session.commit()

# Create shops and items
shop1 = Shop(user_id=1, name="Sally's store")

session.add(shop1)
session.commit()

item = ShoppingItem(user_id=1, name="Head First Python", description="A book for python fundamentals",
                    price="26.50", category="Books", shop=shop1)

session.add(item)
session.commit()

item = ShoppingItem(user_id=1, name="Potable BBQ Grill",
                    description="RED: Coleman Road Trip Propane Portable Grill LXE",
                    price="130.20", category="Outdoors", shop=shop1)

session.add(item)
session.commit()

item = ShoppingItem(user_id=1, name="Stripe Sheath Dress",
                    description="M size: Tommy Hilfiger boardwalk stripe three quarter sleeve dress",
                    price="68.00", category="Clothing", shop=shop1)

session.add(item)
session.commit()

item = ShoppingItem(user_id=1, name="Exercise Ball",
                    description="Large balance ball promotes strength, agility, and balance",
                    price="9.88", category="Sports", shop=shop1)

session.add(item)
session.commit()

# Create another user
User1 = User(name="Yuki Skst", email="yukiskst@example.com", picture='')
session.add(User1)
session.commit()

shop2 = Shop(user_id=2, name="Yuki's sport store")

session.add(shop2)
session.commit()

item = ShoppingItem(user_id=2, name="Snowboard Helmet", description="Smith Optics Unisex Adult Holt Snow Sports Helmet",
                    price="66.50", category="Outdoors", shop=shop2)

session.add(item)
session.commit()

item = ShoppingItem(user_id=2, name="Trail Running Shoes",
                    description="12 size: New Balance Men's MTSUMV1 Trail Running Shoes",
                    price="79.20", category="Outdoors", shop=shop2)

session.add(item)
session.commit()

item = ShoppingItem(user_id=2, name="Warriors Replica ersey", description="M size: Curry S # 30",
                    price="38.99", category="Clothing", shop=shop2)

session.add(item)

print "added menu items!"
session.commit()
