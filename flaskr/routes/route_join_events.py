def route_join_events(app, mysql):
    from flask import request
    from flask.json import jsonify

    @app.route("/joinUserById", methods = ["POST", "GET"])
    def route_join_events():
        if request.method == "POST":
            cursor = mysql.connection.cursor()
            cursor.execute(
            f"""
            SELECT
    	       EventParticipants
            FROM
            	EventsT
            WHERE
            	EventId = {request.form.get("eventId")};
            """)
            results = cursor.fetchall()
            mysql.connection.commit()
            cursor.close()
            event_participants_ids = results[0][0] if results else None

            cursor = mysql.connection.cursor()
            cursor.execute(
            f"""
            SELECT
            	UserJoinedEventsIds
            FROM
            	UsersT
            WHERE
            	UserId = {request.form.get("userId")};
            """)
            results = cursor.fetchall()
            mysql.connection.commit()
            cursor.close()
            user_joined_events_ids = results[0][0] if results else None

            event_participants_ids = event_participants_ids.strip("][").split(", ")
            user_joined_events_ids = user_joined_events_ids.strip("][").split(", ")

            event_participants_ids.append(request.form.get("userId"))
            user_joined_events_ids.append(request.form.get("eventId"))

            cursor = mysql.connection.cursor()
            cursor.execute(
            f"""
            UPDATE
                EventsT
            SET
                EventParticipants = '[{", ".join(e for e in event_participants_ids)}]'
            WHERE
            	EventId = {request.form.get("eventId")};
            """)
            results = cursor.fetchall()
            mysql.connection.commit()
            cursor.close()

            cursor = mysql.connection.cursor()
            cursor.execute(
            f"""
            UPDATE
                UsersT
            SET
                UserJoinedEventsIds = '[{", ".join(e for e in user_joined_events_ids)}]'
            WHERE
            	UserId = {request.form.get("userId")};
            """)
            results = cursor.fetchall()
            mysql.connection.commit()
            cursor.close()

            return jsonify({
                "status": "OK",
                "description": "Joined user into an choosen event.",
                "response": {}
            })
