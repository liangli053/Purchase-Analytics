import unittest
import os
from purchase_analytics import Department, Report, get_prod_dept_map, process_order_prod


class TestPurchase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ Create some toy input/output files for testing """
        with open("./products_test.csv", 'w') as fout:
            fout.write("product_id,product_name,aisle_id,department_id\n"
                       "1,egg,21,101\n"
                       "2,french toast,22,102\n")

        with open("./order_products1_test.csv", 'w') as fout:
            fout.write("order_id,product_id,add_to_cart_order,reordered\n"
                       "1,1,2,1\n"
                       "1,2,1,1\n"
                       "2,2,1,1\n"
                       "2,1,2,1\n")

        with open("./order_products2_test.csv", 'w') as fout:
            fout.write("order_id,product_id,add_to_cart_order,reordered\n"
                       "1,2,2,0\n"
                       "1,2,1,0\n"
                       "2,2,1,0\n"
                       "2,2,2,0\n")

        with open("./sample_output_test.csv", 'w') as fout:
            fout.write("department_id,number_of_orders,number_of_first_orders,percentage\n"
                       "102,4,4,1.00\n")

    @classmethod
    def tearDownClass(cls):
        """ Delete all test files"""
        for file in os.listdir():
            if file.endswith('_test.csv'):
                os.remove(file)

    def setUp(self):
        self.PRODUCTS_PATH = "./products_test.csv"
        self.ORDER1_PATH = "./order_products1_test.csv"
        self.ORDER2_PATH = "./order_products2_test.csv"
        self.SAMPLE_OUTPUT = "./sample_output_test.csv"
        self.report = Report()

    def tearDown(self):
        pass

    def test_get_prod_dept_map(self):
        """ Test if the {product id : department id} constructed from "products.csv" file is correct" """
        res = get_prod_dept_map(self.PRODUCTS_PATH)
        expected = {1: 101, 2: 102}
        self.assertEqual(res, expected)

    def test_process_order_prod(self):
        """ Test if the order data can be corrected read and calculated"""
        mapping = get_prod_dept_map(self.PRODUCTS_PATH)
        process_order_prod(self.ORDER1_PATH, mapping, self.report)
        # length of report.departments should be 2
        self.assertEqual(len(self.report.departments), 2)
        # test the results after reading the orders log
        self.report.sort_depts()
        dept1, dept2 = self.report.depts_sorted[0], self.report.depts_sorted[1]
        res1 = [dept1.ID, dept1.orders, dept1.first_orders, dept1.percentage]
        res2 = [dept2.ID, dept2.orders, dept2.first_orders, dept2.percentage]
        expected1, expected2 = [101, 2, 0, 0.0], [102, 2, 0, 0.0]
        self.assertEqual(res1, expected1)
        self.assertEqual(res2, expected2)

    def test_output(self):
        """ Test the output file content and format """
        mapping = get_prod_dept_map(self.PRODUCTS_PATH)
        process_order_prod(self.ORDER2_PATH, mapping, self.report)
        # length of report.departments should be 1, since products in department 101 have never been ordered
        self.assertEqual(len(self.report.departments), 1)
        # Test the output file. Only department 102 should be written
        self.report.write_to_file("./report_test.csv")
        res = open('./report_test.csv', 'r')
        expected = open(self.SAMPLE_OUTPUT, 'r')
        self.assertEqual(res.read() == expected.read(), True)
        res.close()
        expected.close()


if __name__ == "__main__":
    unittest.main()
