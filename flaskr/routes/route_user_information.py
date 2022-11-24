def route_user_information(app, mysql):
    from flask import request
    from flask.json import jsonify

    @app.route("/getUserInfoById", methods = ["POST", "GET"])
    def get_user_info_by_id():
        if request.method == "GET":
            cursor = mysql.connection.cursor()
            cursor.execute(
            f"""
            SELECT
                *
            FROM
                UsersT
            WHERE
                UserId = {request.args.get("id")}
            """)
            results = cursor.fetchall()
            mysql.connection.commit()
            cursor.close()

            return jsonify({
                "status": "OK",
                "description": "Given information about user by ID.",
                "response": {
                        "user_id": f"{results[0][0]}",
                        "user_first_name": f"{results[0][1]}",
                        "user_last_name": f"{results[0][2]}",
                        "user_name": f"{results[0][3]}",
                        "user_email": f"{results[0][5]}",
                        "user_phone_number": f"{results[0][6]}",
                        "user_birthday": f"{results[0][7]}",
                        "user_credits": f"{results[0][8]}",
                        "user_filter_id": f"{results[0][9]}",
                        "user_joined_events_ids": f"{results[0][10]}",
                        "user_owned_events_ids": f"{results[0][11]}"
                }
            })
