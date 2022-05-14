import unittest
from main import person_by_number, shelf_by_number, del_shelf, add_doc, add_shelf, del_doc, move_doc, \
    compare_docs_dirs, documents, directories

class TestPerson_by_number(unittest.TestCase):

    def setUp(self):
        print("method setUp")

    def tearDown(self):
        print("method tearDown")

    def test_1(self):
        self.assertEqual(person_by_number(documents, '123'), "Геннадий Завывакин")

    def test_2(self):
        self.assertEqual(person_by_number(documents, '10006'), 'Аристарх Павлов')

    def test_3(self):
        self.assertNotEqual(person_by_number(documents, '10006'), 'Василий Гупкин')


class TestShelf_by_number(unittest.TestCase):

    def setUp(self):
        print("method setUp")

    def tearDown(self):
        print("method tearDown")

    def test_1(self):
        self.assertEqual(shelf_by_number(directories, None, '123'), None)

    def test_2(self):
        self.assertEqual(shelf_by_number(directories, None, '10006'), ('2', '10006'))

    def test_3(self):
        self.assertNotEqual(shelf_by_number(directories, None, '10006'), '1')


class TestDel_shelf(unittest.TestCase):

    def setUp(self):
        del_shelf(directories)
        print("method setUp")

    def tearDown(self):
        print("method tearDown")

    def test_1(self):
        self.assertNotIn('4', directories.keys())

    def test_2(self):
        self.assertIn('2', directories.keys())


class TestAdd_doc(unittest.TestCase):

    def setUp(self):
        add_doc(documents, directories, 'passport', '123456', 'Николя', '5', 'y')
        print("method setUp")

    def tearDown(self):
        del_doc('123456')
        print("method tearDown")

    def test_1(self):
        self.assertIn('5', directories.keys())

    def test_2(self):
        self.assertIn({'type': 'passport', 'number': '123456', 'name': 'Николя'}, documents)


class TestAdd_shelf(unittest.TestCase):

    def setUp(self):
        print("method setUp")

    def tearDown(self):
        del_shelf()
        print("method tearDown")

    def test_1(self):
        add_shelf(directories, '5', None)
        self.assertIn('5', directories.keys())

    def test_2(self):
        self.assertEqual(add_shelf(directories, None, None), 'Please use numbers')

    def test_3(self):
        self.assertEqual(add_shelf(directories, '-1', None), 'Negative not allowed')

    def test_4(self):
        self.assertEqual(add_shelf(directories, '2', None), 'Already exists')

    def test_5(self):
        self.assertEqual(add_shelf(directories, '10', 'add'), '10')


class TestDel_doc(unittest.TestCase):
    del_doc('11-2')

    def setUp(self):
        print("method setUp")

    def tearDown(self):
        print("method tearDown")

    def test_1(self):
        for item in documents:
            self.assertNotEqual(item['number'], '11-2')
        print('Test 1 Passed')

    def test_2(self):
        for item in directories.values():
            self.assertNotIn('11-2', item)
        print('Test 2 Passed')

    def test_3(self):
        self.assertEqual(del_doc('678567865'), 'There"s no such document')


class TestMove_doc(unittest.TestCase):
    move_doc(directories, '2', '098765', '11', 'yes')

    def setUp(self):
        print("method setUp")

    def tearDown(self):
        print("method tearDown")

    def test_1(self):
        self.assertIn('098765', directories['11'])

    def test_2(self):
        self.assertNotIn('098765', directories['2'])

    def test_3(self):
        self.assertEqual(move_doc(directories, '2', '098765', '8', 'q'), 'q')


class TestCompare_docs_dirs(unittest.TestCase):

    def setUp(self):
        print("method setUp")

    def tearDown(self):
        print("method tearDown")

    def test_1(self):
        self.assertEqual(compare_docs_dirs(documents, directories), ({'123'}, {'5455 028765', '098765'}))

    def test_2(self):
        self.assertNotEqual(compare_docs_dirs(documents, directories), ({'11-2'}, {'5455 028765', '10006'}))