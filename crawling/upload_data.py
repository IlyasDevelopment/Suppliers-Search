from dotenv import load_dotenv
from models import Item, Product
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

BASE_DIR = Path(__file__).parents[0]
load_dotenv(os.path.join(BASE_DIR, ".env"))

engine = create_engine(os.environ["DB_URL"])
Session = sessionmaker(engine)

with Session() as session:

    session.query(Product).delete()
    session.query(Item).delete()

    with open("data/juridical_info.jl", "r", encoding="utf-8") as f:

        for line in f.readlines():

            row = eval(line.replace("null", "None"))

            for product in row["products"]:
                product_record = Product(domain=row["domain"], product=product)
                session.add(product_record)

            row.pop("products")
            item_record = Item(**row)
            session.add(item_record)

        session.commit()
