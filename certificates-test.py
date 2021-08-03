from jinja2 import Environment, PackageLoader, select_autoescape
import pdfkit
import mariadb
import sys

# this is a throwaway server so not considering security
test = {'name': '', 'course': ''}
try:
    conn = mariadb.connect(
        user="root",
        password="root",
        host="127.0.0.1",
        port=3306,
        database="test"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB: {e}")

cur = conn.cursor(named_tuple=True)
cur.execute("SELECT firstname, lastname, course FROM certificate LIMIT 1")
for (firstname, lastname, course) in cur:
    test['name'] = firstname + ' ' + lastname
    test['course'] = course

env = Environment(
    loader=PackageLoader("certificates-test"),
    autoescape=select_autoescape()
)

template = env.get_template("certificate.html")
with open("certificate.html", "w") as html:
    html.write(template.render(**test))

pdfkit.from_file("certificate.html", "certificate.pdf")
