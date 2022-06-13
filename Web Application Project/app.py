import re
from select import select
from types import new_class
import uuid
from datetime import date, datetime, time

import mysql.connector
from colorama import Cursor
from flask import Flask, redirect, render_template, request, url_for
from mysql.connector import FieldType

import connect_nzoly

dbconn = None

app = Flask(__name__)


def getCursor():
    global dbconn
    global connection
    if dbconn == None:
        connection = mysql.connector.connect(user=connect_nzoly.dbuser, \
        password=connect_nzoly.dbpass, host=connect_nzoly.dbhost, \
        database=connect_nzoly.dbname, autocommit=True)
        dbconn = connection.cursor()
        return dbconn
    else:
        return dbconn


# ----------------------------------------------------------------------INTERFACE 1: ATHELETE--------------------------------------------------------------------------------------------------------------#

#----------- MAIN ROUTE----------#

@app.route("/")
def home():
    cur = getCursor()
    cur.execute("SELECT memberid, firstname, lastname from members;")
    select_result = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    print(f"{column_names}")
    return render_template('athlete_home_.html',dbresult=select_result,dbcols=column_names)



#----------- EVENTS PAST/FUTURE-----------#

@app.route("/athlete/events", methods=['GET','POST'])
def pastevents():
    id = request.args.get("memberid")
    cur = getCursor()
    cur.execute('select FirstName, LastName, e.EventName, Location, StageName, StageDate, if(PointsScored >= PointsToQualify,"Q","DNQ") as results from\
    event_stage as s inner join event_stage_results as r on s.StageID=r.StageID inner join events as e on s.eventID=e.EventID \
    inner join members as m on r.MemberID=m.MemberID where Qualifying = 1 and m.MemberID= %s \
    union \
    select FirstName, LastName, e.EventName, Location, StageName, StageDate, if(Position >3, Position, if(Position=3,"Bronze",if(Position=2,"Silver","Gold"))) as results from \
    event_stage as s inner join event_stage_results as r on s.StageID=r.StageID inner join events as e on s.eventID=e.EventID \
    inner join members as m on r.MemberID=m.MemberID where Qualifying = 0 and m.MemberID= %s order by EventName, StageDate, results ;',(id,id))
    dbresult = cur.fetchall()
    column_names_past = [desc[0] for desc in cur.description]

    cur = getCursor()
    cur.execute('select FirstName, LastName, e.EventName, Location, StageName, StageDate, if(PointsScored >= PointsToQualify,"Q","DNQ") as results from\
    event_stage as s inner join event_stage_results as r on s.StageID=r.StageID \
    inner join events as e on s.eventID=e.EventID inner join members as m on r.MemberID=m.MemberID \
    where Qualifying = 1 and m.MemberID= %s and StageDate > curdate() \
    union \
    select FirstName, LastName, e.EventName, Location, StageName, StageDate, if(Position >3, Position, if(Position=3,"Bronze",if(Position=2,"Silver","Gold"))) as results from\
    event_stage as s inner join event_stage_results as r on s.StageID=r.StageID \
    inner join events as e on s.eventID=e.EventID inner join members as m on r.MemberID=m.MemberID \
    where Qualifying = 0 and m.MemberID= %s and StageDate > curdate() order by EventName, StageDate, results;',(id,id))
    future_result = cur.fetchall()
    column_names_future = [desc[0] for desc in cur.description]
    return render_template('athlete_events_.html',psresult=dbresult, pscols=column_names_past, ftresult=future_result, ftcols=column_names_future, memberid=id)


#----------- UPDATE DETAILS--------------#

@app.route('/athlete/update', methods=['GET','POST'])
def athleteUpdate():
    if request.method == 'POST':
        memberid = request.form.get('memberid')
        teamid = request.form.get('teamid')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        city = request.form.get('city')
        birthdate = request.form.get('birthdate')
        cur = getCursor()
        cur.execute("UPDATE members SET teamid=%s, firstname=%s, lastname=%s, city=%s, birthdate=%s WHERE memberid=%s",(teamid, firstname,lastname,city,birthdate, str(memberid),))
        return redirect("/")
    else:
        id = request.args.get('memberid')
        if id == '':
            return redirect("/")
        else:
            cur = getCursor()
            cur.execute("SELECT * FROM members WHERE memberid=%s",(str(id),))
            select_result = cur.fetchone()
            print(select_result)
            return render_template('athlete_update_form.html',membersdetails = select_result)


# ----------------------------------------------------------------------INTERFACE 2: ADMIN --------------------------------------------------------------------------------------------------------------#


#----------- ADMIN ROUTE ----------- 

@app.route("/admin")
def admin():
    cur = getCursor()
    cur.execute("SELECT memberid, teamid, firstname, lastname, city, birthdate from members;")
    select_result = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    print(f"{column_names}")
    return render_template('admin_home_.html',dbresult=select_result,dbcols=column_names)


#----------- ADMIN UPDATE USER ----------- 

@app.route('/admin/userupdate', methods=['GET','POST'])
def adminUpdate():
    if request.method == 'POST':
        memberid = request.form.get('memberid')
        teamid = request.form.get('teamid')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        city = request.form.get('city')
        birthdate = request.form.get('birthdate')
        cur = getCursor()
        cur.execute("UPDATE members SET teamid=%s, firstname=%s, lastname=%s, city=%s, birthdate=%s WHERE memberid=%s",(teamid, firstname,lastname,city,birthdate, str(memberid),))
        return redirect("/admin")
    else:
        id = request.args.get('memberid')
        if id == '':
            return redirect("/admin")
        else:
            cur = getCursor()
            cur.execute("SELECT * FROM members WHERE memberid=%s",(str(id),))
            select_result = cur.fetchone()
            print(select_result)
            return render_template('admin_update_form.html',membersdetails = select_result)

#----------- ADMIN ADD USER ----------- 

@app.route("/admin/adduser", methods=['GET','POST'])
def updateadminform():
    if request.method == 'POST':
        memberid = request.form.get('memberid')
        teamid = request.form.get('teamid')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        city = request.form.get('city')
        birthdate = request.form.get('birthdate')
        cur = getCursor()
        cur.execute("INSERT INTO members(memberid, teamid, firstname, lastname, city, birthdate) VALUES (%s,%s,%s,%s,%s,%s);",(memberid,teamid, firstname, lastname, city, birthdate,))
        cur.execute("SELECT * FROM members WHERE memberid=%s",(str(memberid),))
        select_result = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        print(f"{column_names}")
        return render_template('admin_add_user_.html',dbresult=select_result,dbcols=column_names)
    else:
        return render_template('admin_add_user_.html')


#----------- ADD EVENTS  ------------------

@app.route("/admin/addevent", methods=['GET','POST'])
def eventform():
    if request.method == 'POST':
        eventid = request.form.get('eventid')
        eventname = request.form.get('eventname')
        sport = request.form.get('sport')
        nzteam = request.form.get('nzteam')
        cur = getCursor()
        cur.execute("INSERT INTO events(eventid, eventname, sport, nzteam) VALUES (%s,%s,%s,%s);",(eventid,eventname, sport, nzteam,))
        cur.execute("SELECT * FROM events where eventid=%s",(str(eventid),))
        select_result = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        print(f"{column_names}")
        return render_template('admin_event_form.html',dbresult=select_result,dbcols=column_names)
    else:
        return render_template('admin_event_form.html')

#-------------------AND EVENT_STAGE ----------------------

@app.route("/admin/addstage", methods=['GET','POST'])
def eventstageform():
    if request.method == 'POST':
        stageid = request.form.get('stageid')
        stagename = request.form.get('stagename')
        eventid = request.form.get('eventid')

        location = request.form.get('location')
        stagedate = request.form.get('stagedate')
        qualifying = request.form.get('qualifying')
        pointstoqualify = request.form.get('pointstoqualify')
        cur = getCursor()
        cur.execute("INSERT INTO event_stage(stageid, stagename, eventid, location, stagedate, qualifying, pointstoqualify ) VALUES (%s,%s,%s,%s,%s,%s,%s);",(stageid,stagename,eventid,location,stagedate,qualifying,pointstoqualify,))
        cur.execute("SELECT * FROM event_stage where stageid=%s",(str(stageid),))
        select_result = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        print(f"{column_names}")
        return render_template('add_event_stage_form.html',dbresult=select_result,dbcols=column_names)
    else:
        return render_template('add_event_stage_form.html')


#----------- ADMIN ADD SCORES  ----------- 

@app.route("/admin/nonqualify")
def nonqualify():
    cur = getCursor()
    cur.execute("""Select memberid, firstname, lastname, resultid,  pointsscored, position from (SELECT e.eventid, e.eventname, s.stagedate,\
        s.qualifying, s.location, s.stageid, s.pointstoqualify, s.stagename FROM events AS e INNER JOIN \
        event_stage AS s ON e.eventid = s.eventid) as selection1  \
        Join \
        (SELECT m.memberid, m.firstname, m.lastname, r.pointsscored, r.stageid, r.position,r.resultid FROM members AS m LEFT JOIN event_stage_results AS r ON m.memberid = r.memberid) as selection2 \
		ON selection1.stageid = selection2.stageid \
        where pointstoqualify > pointsscored;""")
    select_result = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    print(f"{column_names}")
    return render_template('admin_non_qualifying_list_.html',dbresult=select_result,dbcols=column_names)

@app.route("/admin/nonqualify/addscores",  methods=['GET','POST'])
def addscores():
    if request.method == 'POST':
        resultid = request.form.get('resultid')
        pointsscored = request.form.get('pointsscored')
        position = request.form.get('position')
        cur = getCursor()
        cur.execute("UPDATE event_stage_results SET pointsscored=%s, position=%s WHERE resultid=%s",(pointsscored, position, str(resultid),))
        return redirect("/admin/nonqualify")                            
    else:
        id = request.args.get('resultid')
        if id == '':
            return redirect("/admin/nonqualify")
        else:
            cur = getCursor()
            cur.execute("SELECT * FROM event_stage_results WHERE resultid=%s",(str(id),))
            new_result = cur.fetchone()
            print(new_result)
            return render_template('admin_non_qualified_addscores.html',scoressdetails = new_result)

#----------- ADMIN REPORT ----------- 

#----------- MEDALS NUMBER----------- 

@app.route("/admin/report/number")
def numberbymedal():
    cur = getCursor()
    cur.execute("""select memberid, firstname, lastname, resultid, eventname, if(Position >3, Position, if(Position=3,"Bronze",if(Position=2,"Silver","Gold")))as medaltype, position as number from\
    (select r.stageid, m.memberid, m.firstname, m.lastname, r.resultid, r.position from nzoly.event_stage_results as r\
    inner join members as m on r.memberid=m.memberid) as selection1\
    inner join\
    (select  e.eventid, s.stageid, e.eventname, s.qualifying, s.location, s.pointstoqualify, s.stagename from event_stage as s inner join events as e on s.eventid=e.eventid) as selection2\
    on selection1.StageID=selection2.StageID\
    where position < 4 order by eventname desc;""")   
    select_result = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    print(column_names)
    return render_template('report_count_by_medal.html',dbresult=select_result,dbcols=column_names)


#----------- ADMIN REPORT - BY FIRST NAME ----------- 

@app.route("/admin/report/listbyname")
def listMemberByTeam():
    cur = getCursor()
    cur.execute("select t.teamid, m.memberid, t.teamname, m.firstname, m.lastname from members as m \
	left join teams as t on m.teamid = t.teamid \
    order by m.firstname asc;")   
    select_result = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    select_result.sort(key=lambda column_names:(column_names[2]))
    i = 0                                                                                # Create a variable name i and equal to 0
    for x in select_result:                                                               # Create a variable name x and use for loop to arrange
        if x[0] != i:                                                                    # Use if statement to loop through by index of the values in the dblistMember where not equal to 0
            i = x[0]                                                                     # Set i equal to index value 1 where the if condition met
            print(f" \n{x[2]}: ")                                                        # Print the value using f-string to of the TeamName using index number 1
        print(f"   {x[3]},{x[4]}") 
    return render_template('report_team_by_firstname.html',dbresult=select_result,dbcols=column_names)


#----------- ADMIN REPORT - BY LAST NAME ----------- 

@app.route("/admin/report/listbylname")
def listMemberByLastName():
    cur = getCursor()
    cur.execute("Select t.teamid, m.memberid, t.teamname, m.firstname, m.lastname from members as m \
	left join teams as t on m.teamid = t.teamid \
    order by m.lastname asc;")   
    lselect_result = cur.fetchall()
    lcolumn_names = [desc[0] for desc in cur.description]
    lselect_result.sort(key=lambda column_names:(column_names[3]))
    i = 0                                                                                # Create a variable name i and equal to 0
    for x in lselect_result:                                                               # Create a variable name x and use for loop to arrange
        if x[0] != i:                                                                    # Use if statement to loop through by index of the values in the dblistMember where not equal to 0
            i = x[0]                                                                     # Set i equal to index value 1 where the if condition met
            print(f" \n{x[2]}: ")                                                        # Print the value using f-string to of the TeamName using index number 1
        print(f"   {x[3]},{x[4]}") 
    return render_template('report_team_by_lastname.html',dblresult=lselect_result,dblcols=lcolumn_names)


#----------- COUNT LIST FOR  EventName, StageDate, results----------- 

@app.route("/admin/report/countbyesr")
def countbyesrs():
    cur = getCursor()
    cur.execute('select COUNT(memberid) as count, eventname as name from\
    (select r.stageid, m.memberid, m.firstname, m.lastname, r.resultid, r.position, r.pointsscored from nzoly.event_stage_results as r\
    inner join members as m on r.memberid=m.memberid) as selection1\
    join\
    (select  e.eventid, s.stageid, e.eventname, s.qualifying, s.location, s.pointstoqualify, s.stagename from event_stage as s inner join events as e on s.eventid=e.eventid) as selection2\
    on selection1.StageID=selection2.StageID\
    group by eventname\
	UNION ALL\
	select COUNT(memberid), stagename as name from\
    (select r.stageid, m.memberid, m.firstname, m.lastname, r.resultid, r.position, r.pointsscored from nzoly.event_stage_results as r\
    inner join members as m on r.memberid=m.memberid) as selection1\
    join\
    (select  e.eventid, s.stageid, e.eventname, s.qualifying, s.location, s.pointstoqualify, s.stagename from event_stage as s inner join events as e on s.eventid=e.eventid) as selection2\
    on selection1.StageID=selection2.StageID\
	group by stagename\
    UNION ALL\
    select COUNT(memberid), if(position=3,"Bronze", if(position=2,"Silver","Gold")) as name from \
    (select r.stageid, m.memberid, m.firstname, m.lastname, r.resultid, r.position, r.pointsscored from nzoly.event_stage_results as r\
    inner join members as m on r.memberid=m.memberid) as selection1\
    join\
    (select  e.eventid, s.stageid, e.eventname, s.qualifying, s.location, s.pointstoqualify, s.stagename from event_stage as s inner join events as e on s.eventid=e.eventid) as selection2\
    on selection1.StageID=selection2.StageID\
    where qualifying = 0\
    group by position;')
    selection_result = cur.fetchall()
    selection_names = [desc[0] for desc in cur.description]
    print(selection_names)
    return render_template('report_countbyesr.html',selresult=selection_result,selcols=selection_names)

#----------- ADMIN REPORT - MEDAL AND SCORE LIST ----------- 

@app.route("/admin/report/selection")
def reportselection():
    cur = getCursor()
    cur.execute('select FirstName, LastName, e.EventName, Location, StageName, StageDate, if(PointsScored >= PointsToQualify,"Q","DNQ") as results from\
    event_stage as s inner join event_stage_results as r on s.StageID=r.StageID \
    inner join events as e on s.eventID=e.EventID inner join members as m on r.MemberID=m.MemberID \
    where Qualifying = 1  \
    union \
    select FirstName, LastName, e.EventName, Location, StageName, StageDate, if(Position >3, Position, if(Position=3,"Bronze",if(Position=2,"Silver","Gold"))) as results from\
    event_stage  as s inner join event_stage_results as r on s.StageID=r.StageID \
    inner join events as e on s.eventID=e.EventID inner join members as m on r.MemberID=m.MemberID \
    where Qualifying = 0  order by EventName, StageDate, results ;')
    selection_result = cur.fetchall()
    selection_names = [desc[0] for desc in cur.description]
    print(selection_names)
    return render_template('report_selection.html',selresult=selection_result,selcols=selection_names)


@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")
 

