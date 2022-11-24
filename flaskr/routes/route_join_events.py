def route_join_events():
    from flask import request
    from flask.json import jsonify

    @app.route("/joinUserById")
    def route_join_events():
        cursor = mysql.connection.cursor()
        cursor.execute("")
        results = cursor.fetchall()
        mysql.connection.commit()
        cursor.close()

        return jsonify({
            "status": "OK",
            "description": "Joined user into an choosen event.",
            "response": {}
        })
