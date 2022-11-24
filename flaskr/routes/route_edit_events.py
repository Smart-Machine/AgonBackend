def route_edit_events(app, mysql):
    from flask import request
    from flask.json import jsonify

    @app.route("/editEvent", methods = ["POST", "GET"])
    def edit_event():
        if request.method == "POST":
            columns = {
                "EventName": request.form.get("eventName"),
                "EventDate": request.form.get("eventDate"),
                "EventTime": request.form.get("eventTime"),
                "EventPlace": request.form.get("eventPlace"),
                "EventDescription": request.form.get("eventDescription"),
                "EventPhoneNumber": request.form.get("eventPhoneNumber")
            }
            newline = '\n'
            cursor = mysql.connection.cursor()
            cursor.execute(
            f"""
            UPDATE
                EventsT
            SET
                {newline.join(f"{k}='{v}'," for k, v in columns.items() if v)[:-1]}
            WHERE EventId = {request.form.get("eventId")};
            """)
            results = cursor.fetchall()
            mysql.connection.commit()
            cursor.close()

            return jsonify({
                "status": "OK",
                "description": "Event created.",
                "response": {
                    "updated": "success"
                }
            })
