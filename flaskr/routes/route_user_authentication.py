def route_user_authentication(app, mysql):
    from flask import request
    from flask.json import jsonify

    @app.route("/createUser", methods = ["POST", "GET"])
    def create_user():
        if request.method == "POST":
            cursor = mysql.connection.cursor()
            cursor.execute(
            f"""
            INSERT INTO UsersT (
                UserFirstName,
                UserLastName,
                UserName,
                UserPassword,
                UserEmail,
                UserPhoneNumber,
                UserBirthday
            ) VALUES (
                '{request.form.get("userFirstName")}',
                '{request.form.get("userLastName")}',
                '{request.form.get("userName")}',
                '{request.form.get("userPassword")}',
                '{request.form.get("userEmail")}',
                '{request.form.get("userPhoneNumber")}',
                '{request.form.get("userBirthday")}'
            );
            """)
            cursor.execute(
            f"""
            SELECT
                UserId
            FROM
                UsersT
            WHERE
                UserEmail LIKE '{request.form.get("userEmail")}' AND
                UserName LIKE '{request.form.get("userName")}'
            """)
            results = cursor.fetchall()
            mysql.connection.commit()
            cursor.close()

            user_id = results[0][0] if results else None

            return jsonify({
                "status": "OK",
                "description": "User created.",
                "response": {
                    "user_id": f"{user_id}"
                }
            })


    @app.route("/authenticateUser", methods = ["POST", "GET"])
    def authenticate_user():
        if request.method == "POST":
            cursor = mysql.connection.cursor()
            cursor.execute(
            f"""
            SELECT
                UserEmail,
                UserPassword,
                UserId
            FROM
                UsersT
            WHERE
                UserEmail LIKE '{request.form.get("userEmail")}' AND
                UserPassword LIKE '{request.form.get("userPassword")}'
            """)
            results = cursor.fetchall()
            mysql.connection.commit()
            cursor.close()

            if len(results) == 1:
                return jsonify({
                    "status": "OK",
                    "description": "Authenticated user.",
                    "response": {
                        "auth": "success",
                        "user_id": f"{results[0][2]}"
                    }
                })
            return jsonify({
                "status": "OK",
                "description": "Authenticated user.",
                "response": {
                    "auth": "unsuccess"
                }
            })


    @app.route("/checkEmailAvailability", methods = ["POST", "GET"])
    def check_email_availability():
        if request.method == "GET":
            cursor = mysql.connection.cursor()
            cursor.execute(
            f"""
            SELECT
                UserEmail
            FROM
                UsersT
            WHERE
                UserEmail LIKE '{request.args.get("email")}'
            """)
            results = cursor.fetchall()
            mysql.connection.commit()
            cursor.close()

            if not results:
                return jsonify({
                    "status": "OK",
                    "description": "Checked availability of given email.",
                    "response": {
                        "available": "true"
                    }
                })
            return jsonify({
                "status": "OK",
                "description": "Checked availability of given email.",
                "response": {
                    "available": "false"
                }
            })
