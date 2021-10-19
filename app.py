"""
Assignment 8: Booking site
"""

from flask import Flask, request, render_template, g, session
import mysql.connector, os, datetime

confID = 100001
counter = 0

app = Flask(__name__)
app.debug = True
app.secret_key = os.urandom(24)

app.config["DATABASE_USER"] = "root"
app.config["DATABASE_PASSWORD"] = "root"
app.config["DATABASE_DB"] = "dat310"
app.config["DATABASE_HOST"] = "localhost"

def get_db():
    if not hasattr(g, "_database"):
        g._database = mysql.connector.connect(
            host=app.config["DATABASE_HOST"], user=app.config["DATABASE_USER"],
            password=app.config["DATABASE_PASSWORD"], database=app.config["DATABASE_DB"])
    return g._database

def slett_data():
    db = get_db()
    cur = db.cursor()
    sql = "DELETE FROM booking"
    try:
        cur.execute(sql)
        db.commit()
    except mysql.connector.Error as err:
        return render_template("error.html", msg="Error deleting data")
    finally:
        cur.close()

def hent_confID():
    db = get_db()
    cur = db.cursor()
    sql = "SELECT * FROM booking WHERE booking_id=(SELECT MAX(booking_id) FROM booking)"
    try:
        cur.execute(sql)
        db.commit()
    except mysql.connector.Error as err:
        return render_template("error.html", msg="Error getting data")
    finally:
        cur.close()


@app.teardown_appcontext
def teardown_db(error):
    """Closes the database at the end of the request."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
    


@app.route("/")
def index():
    """Index page that shows a list of properties"""

    global counter
    if counter == 0: #Used to delete data at startup
        slett_data()
        
    db = get_db()
    cur = db.cursor()
    try:
        property = []
        sql = "SELECT property_id, property_name, property_location, property_description, property_details, property_photo FROM property"
        cur.execute(sql)
        for (property_id, property_name, property_location, property_description, property_details, property_photo) in cur:
            property.append({
                "property_id": property_id,
                "property_name": property_name,
                "property_location": property_location,
                "property_description": property_description,
                "property_details": property_details,
                "property_photo": property_photo
            })
        return render_template("index.html", property=property)
    except mysql.connector.Error as err:
        return render_template("error.html", msg="Error querying data")
    finally:
        cur.close()

    return render_template("index.html")


def get_property(property_id):
    """Loads a property from the database."""
    # TODO: look up property from database
    db = get_db()
    cur = db.cursor()
    try:
        sql = "SELECT * FROM property WHERE property_id = {propId}".format(propId = property_id)
        cur.execute(sql)
        for (property_id,property_name, property_location, property_description, property_details, property_photo) in cur:
            property_data = {
                "property_id": property_id,
                "property_name": property_name,
                "property_location": property_location,
                "property_description": property_description,
                "property_details": property_details,
                "property_photo": property_photo
            }
    except mysql.connector.Error as err:
        print(err)
    finally:
        cur.close()
    print(property_data)
    return property_data


@app.route("/property/<int:property_id>")
def property(property_id):
    """Product page"""
    return render_template("property.html", property=get_property(property_id))


@app.route("/book", methods=["POST"])
def book():
    """Booking process"""
    action = request.form.get("action")

    if action == "do_1":
        # TODO: check booking details, if all correct show confirmation form,
        # otherwise show order form again (with filled-in values remembered)
                
        fornavn = request.form.get("fornavn")
        etternavn = request.form.get("etternavn")
        email = request.form.get("email")
        telephone = request.form.get("telephone")
        postcode = request.form.get("postcode")
        city = request.form.get("city")
        street = request.form.get("street")
        country = request.form.get("country")
        comment = request.form.get("comment")
        
        session["fornavn"] = request.form.get("fornavn")
        session["etternavn"] = request.form.get("etternavn")
        session["email"] = request.form.get("email")
        session["telephone"] = telephone
        session["postcode"] = postcode
        session["city"] = city
        session["street"] = street
        session["country"] = country
        session["comment"] = comment

        if fornavn is None or fornavn == "":
            return render_template("booking_1.html")
        elif etternavn is None or etternavn == "":
            return render_template("booking_1.html")
        elif email is None or email == "":
            return render_template("booking_1.html")
        elif telephone is None or telephone == "":
            return render_template("booking_1.html")
        elif postcode is None or postcode == "":
            return render_template("booking_1.html")
        elif city is None or city == "":
            return render_template("booking_1.html")
        elif street is None or street == "":
            return render_template("booking_1.html")
        elif country is None or country == "":
            return render_template("booking_1.html")
        else:
            session["fornavn"] = request.form.get("fornavn")
            session["etternavn"] = request.form.get("etternavn")
            session["email"] = request.form.get("email")
            session["telephone"] = telephone
            session["postcode"] = postcode
            session["city"] = city
            session["street"] = street
            session["country"] = country
            session["comment"] = comment

            return render_template("booking_2.html")

    elif action == "do_2":
        if request.form.get("confirm") == "1":  # check if booking is confirmed
            # TODO: save booking in database and return confirmation number
        
            prop_id = request.form.get("property_id")
            check_in = request.form.get("checkin")
            check_out = request.form.get("checkout")
            fornavn = request.form.get("fornavn")
            etternavn = request.form.get("etternavn")
            email = request.form.get("email")
            telephone = request.form.get("telephone")
            postcode = request.form.get("postcode")
            city = request.form.get("city")
            street = request.form.get("street")
            country = request.form.get("country")
            comment = request.form.get("comment")

            global confID
            global counter
            db = get_db()
            cur = db.cursor()
            sql = "INSERT INTO booking (booking_id, property_id, checkin, checkout, fornavn, etternavn, email, telephone, postcode, city, street, country, _comment) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"               
            try:
                cur.execute(sql, (confID, prop_id, check_in, check_out, fornavn, etternavn, email, telephone, postcode, city, street, country, comment))
                db.commit()
                return render_template("booking_3.html", booking_id=confID)
            except mysql.connector.Error as err:
                print(err)
            finally:
                cur.close()
                confID = confID + 1
                counter = counter + 1
                session.clear()

        else:
            return render_template("booking_2.html", err="You need to agree to the terms and conditions to confirm the order.")
    else:
        # TODO: display form asking for details
        session["property_id"] = request.form.get("property_id")
        session["checkin"] = request.form.get("checkin")
        session["checkout"] = request.form.get("checkout")

        return render_template("booking_1.html")

@app.route("/terms", methods=["GET","POST"])
def terms():
    return render_template("terms.html")

if __name__ == "__main__":
    app.run()
