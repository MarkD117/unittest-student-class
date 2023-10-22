import unittest
from student import Student
from datetime import timedelta
# patch is required to mock our method
from unittest.mock import patch


class TestStudent(unittest.TestCase):

    # adding the @classmethod decorator to a method  and passing
    # ‘cls’ as a method parameter will make it a class method
    # which acts on the class instead of an instance of the class.

    # setUpClass() method will be called at the very beginning of
    # the tests. Unlike setUp() which gets called the the beginning
    # of each individual test.
    @classmethod
    def setUpClass(cls):
        print("set up class")

    # setUp method allows us to create our class instance
    # of student at the beginning of every test method.
    # This method will allow us to create temp files and
    # connect to databases
    def setUp(self):
        print("setup")
        self.student = Student("John", "Doe")

    # tearDownClass() method will be called once at the very end
    # of the tests. Unlike tearDown() which gets called the the
    # end of each individual test. This method could be used
    # to destroy a test database for example
    @classmethod
    def tearDownClass(cls):
        print("tear down Class")

    # tearDown method allows us to manipulate code at the
    # end of of every test method. Usually this deletes
    # removes temp files and closes database connetions
    def tearDown(self):
        print("tear down")

    def test_full_name(self):
        print("test_full_name")
        self.assertEqual(self.student.full_name, "John Doe")

    def test_alert_santa(self):
        print("test_alert_santa")
        self.student.alert_santa()
        self.assertTrue(self.student.naughty_list)

    def test_email(self):
        print("test_email")
        self.assertEqual(self.student.email, "john.doe@email.com")

    def test_apply_extension(self):
        print("test_apply_extension")
        old_end_date = self.student.end_date
        self.student.apply_extension(5)
        self.assertEqual(
            self.student.end_date, old_end_date + timedelta(days=5))

    def test_course_schedule_success(self):
        # mocking a get request using a context manager. A decorator may
        # also be used.This creates an object called ‘mocked_get’ which
        # we can use to test the get request functionality. We imported
        # the student class at the top of the file so we use
        # "student.requests.get" to access it.
        with patch("student.requests.get") as mocked_get:
            # mocking a successful request
            mocked_get.return_value.ok = True
            mocked_get.return_value.text = "Success"

            # assigning the result of calling the course_schedule method
            # to a variable called schedule.
            schedule = self.student.course_schedule()
            # Checking if the value returns "Success"
            self.assertEqual(schedule, "Success")

    def test_course_schedule_failed(self):
        """
        In the path "student" comes from the name of the file student.py
        If you have named the file something else - it will need to match
        eg, students.py would need "students.requests.get"
        """
        with patch("student.requests.get") as mocked_get:
            # mocking an unsuccessful request
            mocked_get.return_value.ok = False

            schedule = self.student.course_schedule()
            # checking if the method returns "Something went wrong!"
            # as the return_value.ok was False
            self.assertEqual(schedule, "Something went wrong!")


if __name__ == "__main__":
    unittest.main()
