import cgi

form = cgi.FieldStorage()

name = form.getvalue("name")
email = form.getvalue("email")
gender = form.getvalue("gender")
interests = form.getlist("interests")
country = form.getvalue("country")

print("Content-type: text/html\n")

print("<html>")
print("<head>")
print("<title>Form Submission Result</title>")
print("</head>")
print("<body>")
print("<h2>Form Submission Result</h2>")
print("<p><strong>Name:</strong> {}</p>".format(name))
print("<p><strong>Email:</strong> {}</p>".format(email))
print("<p><strong>Gender:</strong> {}</p>".format(gender))
print("<p><strong>Interests:</strong> {}</p>".format(", ".join(interests)))
print("<p><strong>Country:</strong> {}</p>".format(country))
print("</body>")
print("</html>")
