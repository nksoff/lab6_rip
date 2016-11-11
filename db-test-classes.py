try:
    import MySQLdb
except:
    import pymysql

    pymysql.install_as_MySQLdb()
    import MySQLdb


import random

class Connection:
    def __init__(self, user, password, db, host=''):
        self.user = user
        self.password = password
        self.db = db
        self._connection = None

    @property
    def connection(self):
        self.connect()
        return self._connection

    def close(self):
        if self._connection:
            self._connection.close()

    def connect(self):
        if not self._connection:
            self._connection = MySQLdb.connect(
                host="127.0.0.1",
                user=self.user,
                passwd=self.password,
                db=self.db,
                charset="utf8"
            )


class Tutor:
    def __init__(self, db, lastname, firstname, middlename, birthday, sex, id=None):
        self.db = db
        self.lastname = lastname
        self.firstname = firstname
        self.middlename = middlename
        self.birthday = birthday
        self.sex = sex
        self._id = id

    def save(self):
        cursor = self.db.connection.cursor()
        if self._id is None:
            cursor.execute(
                "INSERT INTO lab_tutor (lastname, firstname, middlename, birthday, sex) VALUES(%s, %s, %s, %s, %s)",
                (self.lastname, self.firstname, self.middlename, self.birthday, self.sex))
            self._id = self.db.connection.insert_id()

        else:
            cursor.execute(
                "UPDATE lab_tutor SET lastname = %s, firstname = %s, middlename = %s, birthday = %s, sex = %s WHERE id = %s",
                (self.lastname, self.firstname, self.middlename, self.birthday, self.sex, self._id)
            )

        self.db.connection.commit()
        cursor.close()

    @staticmethod
    def select_all(db):
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM lab_tutor")

        entities = cursor.fetchall()

        entities = map(
            lambda x: Tutor(db, x['lastname'], x['firstname'], x['middlename'], x['birthday'], x['sex'], x['id']),
            entities)

        cursor.close()

        return entities

    @staticmethod
    def clear_all(db):
        cursor = db.connection.cursor()
        cursor.execute("DELETE FROM lab_tutor WHERE 1=1")
        db.connection.commit()
        cursor.close()

    def __repr__(self):
        return "#{}: {} {} {} {} {}".format(self._id, self.lastname, self.firstname, self.middlename, self.birthday,
                                            self.sex)


class Course:
    def __init__(self, db, name, full_name, tutor_id, id=None):
        self.db = db
        self.name = name
        self.full_name = full_name
        self.tutor_id = tutor_id._id if isinstance(tutor_id, Tutor) else tutor_id
        self._id = id

    def save(self):
        cursor = self.db.connection.cursor()
        if self._id is None:
            cursor.execute(
                "INSERT INTO lab_course (name, full_name, tutor_id) VALUES(%s, %s, %s)",
                (self.name, self.full_name, self.tutor_id))
            self._id = self.db.connection.insert_id()

        else:
            cursor.execute(
                "UPDATE lab_course SET name = %s, full_name = %s, tutor_id = %s WHERE id = %s",
                (self.name, self.full_name, self.tutor_id, self._id)
            )

        self.db.connection.commit()
        cursor.close()

    @classmethod
    def select_all(self, db, tutor_id):
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM lab_course WHERE tutor_id = %s", (tutor_id))

        entities = cursor.fetchall()

        entities = map(lambda x: Course(db, x['name'], x['full_name'], x['tutor_id'], x['id']), entities)

        cursor.close()

        return entities


    @staticmethod
    def clear_all(db):
        cursor = db.connection.cursor()
        cursor.execute("DELETE FROM lab_course WHERE 1=1")
        db.connection.commit()
        cursor.close()

    def __repr__(self):
        return "#{}: {} {} {}".format(self._id, self.name, self.full_name, self.tutor_id)


db = Connection("lab6", "lab6", "lab6", "127.0.0.1")

t = Tutor(db, "L", "F", "M", None, True)
t.save()

tutors = list(Tutor.select_all(db))
print(tutors)

t.lastname = "Last"
t.firstname = "First"
t.save()

tutors = list(Tutor.select_all(db))
print(tutors)

course = Course(db, "Name" + str(random.randint(1, 10000)), "Fullname", tutors[0])
print(course)
course.save()
print(course)

courses = list(Course.select_all(db, tutors[0]._id))
print(courses)

Course.clear_all(db)
Tutor.clear_all(db)

db.close()
