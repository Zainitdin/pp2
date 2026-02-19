class Father:
    def skills(self):
        print("Father: Gardening")

class Mother:
    def skills(self):
        print("Mother: Cooking")

class Child(Father, Mother):
    pass


c = Child()
c.skills()
