import random
import unittest
from main import MWare


class TestMiddlewareOperations(unittest.TestCase):
    test = None
    test_size = 100

    @classmethod
    def setUpClass(cls):
        random.seed(10)
        cls.random_key = random.randint(0, 9)
        cls.test = MWare()
        cls.test_uids = [i for i in range(cls.test_size)]
        cls.test_names = [f'N-:{str(i)}' for i in range(cls.test_size)]
        cls.test_emails = [f'@Email-:{str(i)}' for i in range(cls.test_size)]

    def test_set_get_single(self):
        self.assertEqual(self.test.set_to(key=self.random_key, name='single_set_name', email='single_set_email'), 'OK')
        expected = [{'name': 'single_set_name', 'email': 'single_set_email'}]
        self.assertEqual(expected, self.test.get_single(key_list=[self.random_key]))

    def test_set_get_multiples(self):
        self.assertEqual('OK',
                         self.test.set_multiples(key_list=self.test_uids, name_list=self.test_names,
                                                 email_list=self.test_emails))
        total_kv_pairs = len(self.test.get_multiple(key_list=self.test_uids))
        self.assertEqual(len(self.test_uids), total_kv_pairs)
        self.assertEqual(len(self.test.get_multiple(key_list=[0, 1, 2, 3])), 4)

    def test_update_get_values(self):
        self.test.update_values(key_list=[0, 1, 88], name='updated_names', email='updated_emails',
                                test='test_field_update')
        expected = {'name': 'updated_names', 'email': 'updated_emails', 'test': 'test_field_update'}
        actual = self.test.get_multiple(key_list=[0, 1, 88])
        for d in actual:
            self.assertDictEqual(expected, d)

    def test_get_range(self):
        self.test.update_values(key_list=[90, 91, 92], name='range_names', email='range_emails')
        actual = self.test.get_range(start=90, end=92)
        expected = {'name': 'range_names', 'email': 'range_emails'}
        for d in actual:
            self.assertDictEqual(expected, d)

    def test_get_fields(self):
        # the orders of values fetched is not preserved
        # but the order of fields is preserved
        actual_first = self.test.get_fields(key_list=[3], field_list=['email', 'name'])
        self.assertEqual([f'@Email-:{str(3)}', 'N-:3'], actual_first[0])

        actual_second = self.test.get_fields(key_list=[33], field_list=['name', 'email'])
        self.assertEqual(['N-:33', f'@Email-:{str(33)}'], actual_second[0])

    def test_del_keys_fields(self):
        self.test.del_fields(key_list=[10, 11], fields=['email'])
        actual = self.test.get_multiple(key_list=[10, 11])
        expected = [{'name': 'N-:11'}, {'name': 'N-:10'}]

        self.assertDictEqual(expected[0], actual[0])
        self.assertDictEqual(expected[1], actual[1])

        self.test.del_single(key_list=[27])
        self.assertEqual([{}], self.test.get_single(key_list=[27]))

    @classmethod
    def tearDownClass(cls) -> None:
        print(cls.test.key_space_inf())
        # flush_all()


def flush_all():
    m_ware = MWare()
    m_ware.flush_all()
    print(m_ware.key_space_inf())
