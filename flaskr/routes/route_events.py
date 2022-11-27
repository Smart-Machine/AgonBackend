def route_events(app, mysql):
    from flask import request
    from flask.json import jsonify

    @app.route("/")
    def hello_api():
        return "Agon API"

    @app.route("/getEvent")
    def get_all_events():
        cursor = mysql.connection.cursor()
        cursor.execute(
        """
        SELECT
            *
        FROM
            EventsT
        WHERE
            EventStatusId <> 4;
        """)
        results = cursor.fetchall()
        mysql.connection.commit()
        cursor.close()

        return [{
            "status" : "OK",
            "description": "Events were given.",
            "response": {
                "event_id": row[0],
                "event_owner_name": row[1],
                "event_owner_id": row[2],
                "event_participants": row[3],
                "event_status_id": row[4],
                "event_filters_id": row[5],
                "event_name": row[6],
                "event_date": str(row[7]),
                "event_time": str(row[8]),
                "event_place": row[9],
                "event_number_of_people": row[10],
                "event_total_number_of_people": row[11],
                "event_description": row[12],
                "event_phone_number": row[13]
            }
        } for row in results]


    @app.route("/createEvent", methods = ["POST", "GET"])
    def create_event():
        filters = {
            "Volleyball": 1,
            "Football": 2,
            "Checkers": 3,
            "Chess": 4,
            "Basketball": 5,
            "Soccer": 6,
            "Golf": 7,
            "Cycling": 8,
            "Running": 9,
            "Tennis": 10,
            "Table Tennis": 11
        }

        if request.method == "POST":
            cursor = mysql.connection.cursor()
            cursor.execute(
            f"""
            INSERT INTO EventsT (
                EventOwnerName,
                EventOwnerId,
                EventParticipants,
                EventStatusId,
                EventFiltersId,
                EventName,
                EventDate,
                EventTime,
                EventPlace,
                EventNumberOfPeople,
                EventTotalNumberOfPeople,
                EventDescription,
                EventPhoneNumber,

            ) VALUES (
                '{request.form.get("eventOwnerName")}',
                {request.form.get("eventOwnerId")},
                '[]',
                3,
                {filters.get(request.form.get("eventFilter"))},
                '{request.form.get("eventName")}',
                '{request.form.get("eventDate")}',
                '{request.form.get("eventTime")}',
                '{request.form.get("eventPlace")}',
                {request.form.get("eventNumberOfPeople")},
                {request.form.get("eventTotalNumberOfPeople")},
                '{request.form.get("eventDescription")}',
                '{request.form.get("eventPhoneNumber")}'
            );
            """)
            cursor.execute(
            f"""
            SELECT
                EventId
            FROM
                EventsT
            WHERE
                EventOwnerId = {request.form.get("eventOwnerId")} AND
                EventName like '{request.form.get("eventName")}' AND
                EventDate = '{request.form.get("eventDate")}'
            """)
            results = cursor.fetchall()
            mysql.connection.commit()
            cursor.close()

            event_id = results[0][0] if results else None

            return jsonify({
                "status": "OK",
                "description": "Event created.",
                "response": {
                    "event_id": f"{event_id}"
                }
            })

    @app.route("/deleteEvent", methods = ["POST", "GET"])
    def delete_event():
        cursor = mysql.connection.cursor()
        cursor.execute(
        f"""
        UPDATE
            EventsT
        SET
            EventStatusId = 4
        WHERE
            EventId = {request.form.get("eventId")};
        """)
        results = cursor.fetchall()
        mysql.connection.commit()
        cursor.close()

        return jsonify({
            "status": "OK",
            "description": "Event deleted.",
            "response": {
                "event_id": f"{request.form.get('eventId')}"
            }
        })
