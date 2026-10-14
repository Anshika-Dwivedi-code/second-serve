
from flask import Flask, render_template, request
import pymysql
from werkzeug.security import generate_password_hash

app = Flask(__name__)


# Connect to MySQL database
def get_db_connection():
    return pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="",
        database="second_serve",
        connect_timeout=10
    )


# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Donate Food
@app.route("/donate-food", methods=["GET", "POST"])
def donate_food():
    if request.method == "POST":
        print("DONATION FORM POST RECEIVED", flush=True)

        donor_name = request.form.get("donor_name")
        food_name = request.form.get("food_name")
        quantity = request.form.get("quantity")
        address = request.form.get("address")
        contact = request.form.get("contact")

        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """INSERT INTO donations
                (donor_name, food_name, quantity, address, contact)
                VALUES (%s, %s, %s, %s, %s)""",
                (donor_name, food_name, quantity, address, contact)
            )
            conn.commit()

        except Exception as e:
            if conn is not None:
                conn.rollback()
            print("DONATION DATABASE ERROR:", repr(e), flush=True)
            return "Donation failed. Check the VS Code terminal.", 500

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

        return """
        <h1>Donation Submitted Successfully!</h1>
        <p>Your donation details have been saved.</p>
        <a href="/">Back to Home</a>
        """

    return render_template("donate_food.html")


# Need Food
@app.route("/need-food", methods=["GET", "POST"])
def need_food():
    if request.method == "POST":
        print("FOOD REQUEST POST RECEIVED", flush=True)

        ngo_name = request.form.get("ngo_name")
        contact_person = request.form.get("contact_person")
        food_required = request.form.get("food_required")
        quantity = request.form.get("quantity")
        address = request.form.get("address")
        contact = request.form.get("contact")

        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """INSERT INTO food_requests
                (ngo_name, contact_person, food_required,
                 quantity, address, contact)
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (
                    ngo_name,
                    contact_person,
                    food_required,
                    quantity,
                    address,
                    contact
                )
            )
            conn.commit()

        except Exception as e:
            if conn is not None:
                conn.rollback()
            print("FOOD REQUEST DATABASE ERROR:", repr(e), flush=True)
            return "Food request failed. Check the VS Code terminal.", 500

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

        return """
        <h1>Food Request Submitted!</h1>
        <p>Your food request has been saved.</p>
        <a href="/">Back to Home</a>
        """

    return render_template("need_food.html")


# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        print("LOGIN FORM POST RECEIVED", flush=True)

        return """
        <h1>Login Form Submitted</h1>
        <p>Actual account verification is not implemented yet.</p>
        <a href="/">Back to Home</a>
        """

    return render_template("login.html")


# NGO Registration
@app.route("/ngo-register", methods=["GET", "POST"])
def ngo_register():
    if request.method == "POST":
        print("NGO REGISTRATION POST RECEIVED", flush=True)

        ngo_name = request.form.get("ngo_name")
        contact_person = request.form.get("contact_person")
        email = request.form.get("email")
        phone = request.form.get("phone")
        registration_number = request.form.get("registration_number")
        address = request.form.get("address")
        password = request.form.get("password")

        if not password:
            return "Password is required.", 400

        password_hash = generate_password_hash(password)

        conn = None
        cursor = None

        try:
            print("Step 1: Connecting to MySQL...", flush=True)

            conn = get_db_connection()

            print("Step 2: MySQL connected successfully!", flush=True)

            cursor = conn.cursor()

            print("Step 3: Cursor created successfully!", flush=True)

            cursor.execute(
                """INSERT INTO ngo_registrations
                (ngo_name, contact_person, email, phone,
                 registration_number, address, password)
                VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (
                    ngo_name,
                    contact_person,
                    email,
                    phone,
                    registration_number,
                    address,
                    password_hash
                )
            )

            conn.commit()

            print("Step 4: NGO registration saved!", flush=True)

        except Exception as e:
            if conn is not None:
                conn.rollback()

            print("NGO REGISTRATION ERROR:", repr(e), flush=True)

            return (
                "Registration failed. Please check the VS Code terminal.",
                500
            )

        finally:
            if cursor is not None:
                cursor.close()

            if conn is not None:
                conn.close()

        return """
        <h1>NGO Registration Successful!</h1>
        <p>Your registration details have been saved.</p>
        <a href="/">Back to Home</a>
        """

    return render_template("ngo_register.html")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
