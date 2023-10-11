import cgi
import cgitb
import os

cgitb.enable()

form = cgi.FieldStorage()

cookie_str = os.environ.get('HTTP_COOKIE')
cookie_dict = {}
if cookie_str:
    cookie_list = cookie_str.split('; ')
    for cookie in cookie_list:
        key, value = cookie.split('=')
        cookie_dict[key] = value

count = int(cookie_dict.get('form_count', 0))

if 'delete_cookies' in form:
    count = 0
    print("Cookies deleted")

if form.getvalue('submit'):
    count += 1

name = form.getvalue("name")
email = form.getvalue("email")
gender = form.getvalue("gender")
interests = form.getlist("interests")
country = form.getvalue("country")

print("Content-type: text/html")
print("Set-Cookie: form_count={};".format(count))
print() 

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
print("<p>Number of forms submitted: {}</p>".format(count))
print('<p><a href="../index.html">Fill out a new form</a></p>')
print('<form method="POST">')
print('<input type="submit" name="submit" value="Submit Form">')
print('</form>')
print('<form method="POST">')
print('<input type="submit" name="delete_cookies" value="Delete Cookies">')
print('</form>')
print("</body>")
print("</html>")
