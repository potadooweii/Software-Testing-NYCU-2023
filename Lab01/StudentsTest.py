import sys
import unittest
import Students
import atexit


def exit_handler():  # pragma: no cover
    output = "".join(sys.stdout.buffer)
    sys.stdout = sys.__stdout__
    print("", file=sys.stderr, flush=True)
    print(output, flush=True)


atexit.register(exit_handler)


class ListStream:
    def __init__(self):
        self.buffer = []

    def write(self, text):
        self.buffer.append(text)


class Test(unittest.TestCase):
    students = Students.Students()

    user_names = ["John", "Mary", "Thomas", "Jane"]
    user_ids = []

    @classmethod
    def setUpClass(cls):
        sys.stdout = ListStream()

    # test case function to check the Students.set_name function
    def test_0_set_name(self):
        # TODO
        print("\nStart set_name test\n")

        for user_name in self.user_names:
            user_id = self.students.set_name(user_name)
            self.assertTrue((isinstance(user_id, int) and user_id >= 0))
            self.user_ids.append(user_id)
            print(f"{user_id} {user_name}")

        self.assertTrue(len(self.user_ids) == len(set(self.user_ids)))

        print("\nFinish set_name list")

    # test case function to check the Students.get_name function
    def test_1_get_name(self):
        # TODO
        print("\nStart get_name test\n")
        print(f"user_id length =  {len(self.user_ids)}")
        print(f"user_name length =  {len(self.user_names)}\n")

        for user_id in self.user_ids:
            user_name = self.students.get_name(user_id)
            self.assertEqual(user_name, self.user_names[user_id])
            print(f"id {user_id} : {user_name}")

        self.assertEqual(
            self.students.get_name(max(self.user_ids) + 1), "There is no such user"
        )
        print(f"id {len(self.user_ids)} : There is no such user")

        print("\nFinish get_name list")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
