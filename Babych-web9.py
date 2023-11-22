from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Date, Time, Enum, ForeignKey
# from sqlalchemy import func

Base = declarative_base()


class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)
    entry_date = Column(Date)

    def __str__(self):
        return f'Student: {self.id}, {self.name} \
            has been studing since {self.entry_date}'


class Teacher(Base):
    __tablename__ = 'teacher'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)
    hire_date = Column(Date)

    def __str__(self):
        return f'Teacher: {self.id}, {self.name} \
            has been working since {self.hire_date}'


class Subject(Base):
    __tablename__ = 'subject'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)

    def __str__(self):
        return f'Subject: {self.id}, {self.name}'


class Class_Management(Base):
    __tablename__ = 'class_management'
    id = Column(Integer, autoincrement=True, primary_key=True)
    designated_time = Column(Time)
    designated_weekday = Column(String,
                                Enum('1', '2', '3', '4', '5', '6', '7')
                                )
    subject_id = Column(Integer, ForeignKey('subject.id'))
    teacher_id = Column(Integer, ForeignKey('teacher.id'))
    classroom_id = Column(Integer, ForeignKey('classroom.id'))

    def __str__(self):
        return f'Class_Management: {self.id} \
            on {self.designated_weekday} at {self.designated_time}'


class Classroom(Base):
    __tablename__ = 'classroom'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)
    capacity = Column(Integer)

    def __str__(self):
        return f'Classroom: {self.id}, {self.name} \
            for {self.capacity} people'


class Class_Enrollment(Base):
    __tablename__ = 'class_enrollment'
    id = Column(Integer, autoincrement=True, primary_key=True)
    student_id = Column(Integer, ForeignKey('student.id'))
    class_id = Column(Integer, ForeignKey('class_management.id'))

    def __str__(self):
        return f'Class_Enrollment: {self.id}, {self.name}'


class Grade_Recording(Base):
    __tablename__ = 'grade_recording'
    id = Column(Integer, autoincrement=True, primary_key=True)
    student_id = Column(Integer, ForeignKey('student.id'))
    class_id = Column(Integer, ForeignKey('class_management.id'))
    grade = Column(Integer)


import psycopg2
   
from sqlalchemy import create_engine
DATABASE_URI = 'postgresql://{user}:{password}@{host}:{port}/{database}'
engine = create_engine(
    DATABASE_URI.format(
        host='localhost',
        database='postgres',
        user='postgres',
        password='password',
        port=5432,
    )
)
Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker
session = sessionmaker(bind=engine)
session = session()

""" enter the data """
student1 = Student(name='Student1', entry_date=Date(2023, 9, 20))
student2 = Student(name='Student2', entry_date=Date(2023, 9, 20))
session.add_all([student1, student2])
session.commit()

teacher1 = Teacher(name='Teacher1', hire_date=Date(2020, 9, 10))
teacher2 = Teacher(name='Teacher2', hire_date=Date(2020, 9, 10))
teacher3 = Teacher(name='Teacher3', hire_date=Date(2020, 9, 10))
session.add_all([teacher1, teacher2, teacher3])
session.commit()

subject1 = Subject(name='Math')
subject2 = Subject(name='English')
subject3 = Subject(name='Economics')
session.add_all([subject1, subject2, subject3])
session.commit()

classroom1 = Classroom(name='404', capacity=15)
classroom2 = Classroom(name='208', capacity=30)
session.add_all([classroom1, classroom2])
session.commit()

class_management1 = Class_Management(designed_time=Time(8, 30),
                                     designed_weekday=1, subject_id=1,
                                     teacher_id=1)
class_management2 = Class_Management(designed_time=Time(10, 30),
                                     designed_weekday=3, subject_id=1,
                                     teacher_id=1)
class_management3 = Class_Management(designed_time=Time(8, 30),
                                     designed_weekday=1, subject_id=2,
                                     teacher_id=2)
session.add_all([class_management1, class_management2,
                 class_management3])
session.commit()

class_enrollment1 = Class_Enrollment(student_id=1, class_id=1)
class_enrollment2 = Class_Enrollment(student_id=1, class_id=3)
class_enrollment3 = Class_Enrollment(student_id=1, class_id=2)
session.add_all([class_enrollment1, class_enrollment2,
                 class_enrollment3])
session.commit()

session.close()
