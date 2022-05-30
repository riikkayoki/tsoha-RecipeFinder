from db import (db as default_db)
from entities.quantity import Quantity

class QuantityRepository:
    def __init__(self, db=default_db):
        self._db = db

    def create_quantity(self, quantity):
        try:
            sql = "INSERT INTO Quantity (ingredient_quantity) VALUES (:quantity)"
            self._db.session.execute(sql, Quantity(quantity=quantity))
            self._db.session.commit()
        except:
            return False

    def add_quantity_to_recipe_ingredient(self):
        pass

    def modify_quantity(self):
        pass