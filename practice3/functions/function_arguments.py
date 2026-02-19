def my_function(name = "friend"):
  print("Hello", name)

my_function("Emil")
my_function("Tobias")
my_function()
my_function("Linus")


def my_function1(fname, lname):
  print(fname + " " + lname)

my_function1("Emil", "Refsnes")


def my_function2(animal, name):
  print("I have a", animal)
  print("My", animal + "'s name is", name)

my_function2(animal = "dog", name = "Buddy")


def my_function3(animal, name, age):
  print("I have a", age, "year old", animal, "named", name)

my_function3("dog", name = "Buddy", age = 5)