try:
    import MySQLdb
except:
    import pymysql

    pymysql.install_as_MySQLdb()
    import MySQLdb

db = MySQLdb.connect(
    host="127.0.0.1",
    user="lab6",
    passwd="lab6",
    db="lab6",
    charset="utf8"
)

cursor = db.cursor(MySQLdb.cursors.DictCursor)
cursor.execute("""INSERT INTO lab_tutor
               (lastname, firstname, middlename, birthday, sex)
               VALUES
               (%s, %s, %s, %s, %s),
               (%s, %s, %s, %s, %s),
               (%s, %s, %s, %s, %s)""",
               ("Муслимов", "Петр", "Ренатович", "1965-09-09", True,
                "Ананасов", "Федор", "Сергеевич", "1971-08-16", True,
                "Хилякова", "Анна", "Львовна", "1987-04-19", False)
               )

db.commit()

cursor.execute("SELECT * FROM lab_tutor")

tutors = cursor.fetchall()

for tutor in tutors:
    print("{}: {} {} {}, {}, {}".format(tutor['id'],
                                        tutor['firstname'],
                                        tutor['lastname'],
                                        tutor['middlename'],
                                        "М" if tutor['sex'] else "Ж",
                                        tutor['birthday'].strftime("%d %m %Y")))

cursor.execute("DELETE FROM lab_tutor WHERE 1=1")
db.commit()

cursor.close()
db.close()
