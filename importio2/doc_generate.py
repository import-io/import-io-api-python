from jinja2 import Template, FileSystemLoader, Environment
templateLoader = FileSystemLoader(searchpath=".")
templateEnv = Environment(loader=templateLoader)

t = templateEnv.get_template("example.md")
print(t.render(something="World"))

t = templateEnv.get_template("example2.md")
numbers = []
numbers.append(1)
numbers.append(2)
numbers.append(3)
numbers.append(4)
numbers.append(5)
print(t.render(numbers=numbers))
