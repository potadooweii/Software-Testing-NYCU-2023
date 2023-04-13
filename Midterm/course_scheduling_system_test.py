import unittest
from unittest.mock import Mock, patch
from course_scheduling_system import CSS


class CSSTest(unittest.TestCase):
    @patch.object(CSS, "check_course_exist")
    def setUp(self, mock_check_course_exist: Mock):
        # stub
        pass

    @patch.object(CSS, "check_course_exist")
    def test_q1_1(self, mock_check_course_exist: Mock):
        mock_check_course_exist.return_value = True
        css = CSS()

        with self.subTest():
            course = ('ST', 'Monday', 1, 2)
            ret = css.add_course(course)
            # Check return value
            self.assertTrue(ret)
        
            ret = css.get_course_list()
            # Verify Result
            self.assertEqual(len(ret), 1)
            self.assertEqual(ret[0], course)

    @patch.object(CSS, "check_course_exist")
    def test_q1_2(self, mock_check_course_exist: Mock):
        mock_check_course_exist.return_value = True
        css = CSS()

        with self.subTest():
            course = ('ST', 'Monday', 1, 2)
            ret = css.add_course(course)
            self.assertTrue(ret)
            ret = css.add_course(course)
            self.assertFalse(ret)
        
            ret = css.get_course_list()
            self.assertEqual(len(ret), 1)
            self.assertEqual(ret[0], course)
    
    @patch.object(CSS, "check_course_exist")
    def test_q1_3(self, mock_check_course_exist: Mock):
        mock_check_course_exist.return_value = False
        css = CSS()

        with self.subTest():
            course = ('ST', 'Monday', 1, 2)
            ret = css.add_course(course)
            # Check return value
            self.assertFalse(ret)
        
            ret = css.get_course_list()
            # Verify Result
            self.assertEqual(len(ret), 0)

    @patch.object(CSS, "check_course_exist")
    def test_q1_4(self, mock_check_course_exist: Mock):
        mock_check_course_exist.return_value = True
        css = CSS()
        
        with self.subTest():
            with self.assertRaises(TypeError):
                course = ('ST', 'Monday', 2, 1)
                ret = css.add_course(course)
            with self.assertRaises(TypeError):
                course = (1, 'Monday', 1, 2)
                ret = css.add_course(course)
            with self.assertRaises(TypeError):
                course = ('ST', 'XXX', 1, 2)
                ret = css.add_course(course)
    
    @patch.object(CSS, "check_course_exist")
    def test_q1_5(self, mock_check_course_exist: Mock):
        mock_check_course_exist.return_value = True
        css = CSS()

        with self.subTest():
            course1 = ('ST', 'Monday', 1, 2)
            course2 = ('DL', 'Tuesday', 1, 2)

            css.add_course(course1)
            css.add_course(course2)
            css.remove_course(course2)

            ret = css.get_course_list()
            self.assertEqual(len(ret), 1)
            self.assertEqual(ret[0], course1)
            self.assertEqual(mock_check_course_exist.call_count, 3)

            print('')
            print(css)

    @patch.object(CSS, "check_course_exist")
    def test_q1_6(self, mock_check_course_exist: Mock):
        mock_check_course_exist.return_value = True
        css = CSS()

        with self.subTest():
            course = ('ST', 'Monday', 1, 2)

            css.add_course(course)

            bad_courses = [
                ('DL', 'Monday', 1, 2)
            ]

            for bad_course in bad_courses:
                ret = css.add_course(bad_course)
                self.assertFalse(ret)

            css.remove_course(course)
            ret = css.remove_course(course)
            self.assertFalse(ret)



if __name__ == "__main__": # pragma no cover
    unittest.main()
