"""
    Author: Liang Li, Mar 28 2019
    Purpose: Based on Instacart orders, calculate, for each department,
    the number of times a product was requested, number of times a product
    was requested for the first time and a ratio of those two numbers.

    Inputs: Three strings specifying the path to in-/output files

    Output is written to ./output/report.csv
"""

from sys import argv


class Department:
    """
        Stores the data associated with each department that need to be written to the output file.
    """

    def __init__(self, dept_ID):
        """
            Arguments:
                dept_ID: int -- Department ID

            Attributes:
                self.ID: int -- Department ID
                self.orders: int -- Total number of orders
                self.first_orders: int -- Total number of first-time orders
                self.percentage: float -- Ratio between self.first_orders and self.orders
        """
        self.ID = dept_ID
        self.orders = 0
        self.first_orders = 0
        self.percentage = 0.0


class Report:
    """
        Stores a dict in which each Department object is indexed by department id, as well as a list of
        sorted Department objects. Several methods to sort Department objects and write output.
    """

    def __init__(self):
        """
            Attributes:
                self.departments: dict {int : Department} -- Mapping department ID to Department object
                self.depts_sorted: list [Department] -- List of Department objects sorted by department ID
        """
        # department ID : department class
        self.departments = {}
        self.depts_sorted = []

    def get_dept(self, dept_ID):
        """
            Based on the department id, return the corresponding Department object.

            Arguments:
                dept_ID: int -- Department ID read from input file

            Returns:
                self.departments[dept_ID]: Department object -- The Department object that is currently being processed
        """
        # create a Department object if current dept_ID is not seen before
        if dept_ID not in self.departments:
            self.departments[dept_ID] = Department(dept_ID)
        return self.departments[dept_ID]

    def update_percentage(self):
        """
            Calculate the "percentage" attribute of each Department object in self.departments.
        """
        for dept in self.departments.values():
            dept.percentage = float(dept.first_orders / dept.orders)

    def sort_depts(self):
        """
            Sort all Department objects by department ID, upadte self.depts_sorted.
        """
        self.depts_sorted = list(self.departments.values())
        self.depts_sorted.sort(key=lambda x: x.ID)

    def write_to_file(self, output_path):
        """
            Write the attribute values of each Department object to the output file.

            Arguments:
                output_path: str -- The path to the output file
        """
        self.sort_depts()
        # write to the output file
        with open(output_path, 'w') as fout:
            fout.write("department_id,number_of_orders,number_of_first_orders,percentage\n")
            for dept in self.depts_sorted:
                # A department_id should be listed only if number_of_orders is greater than 0
                # This is actually already implicitly implemented in func process_order_prod.
                if dept.orders <= 0:
                    raise ValueError('Number of orders must be greater than zero!')
                fout.write(str("%d,%d,%d,%0.2f\n" % (dept.ID, dept.orders, dept.first_orders, dept.percentage)))


def get_prod_dept_map(products_path):
    """
        Read "products.csv" file and return a hash table that maps product id to department id.

        Arguments:
            products_path: str -- Path to the "products.csv" file

        Returns:
            mapping: dict {int : int} -- A hash table with the keys being product id and values being department id.
    """
    mapping = {}
    with open(products_path, 'r') as infile:
        next(infile)
        for line in infile:
            entry = line.strip().split(',')
            prod_ID = int(entry[0])
            dept_ID = int(entry[-1])
            mapping[prod_ID] = dept_ID
    return mapping


def process_order_prod(order_products_path, mapping, report):
    """
        Read "order_products.csv" file and update Department and Report objects.

        Arguments:
            order_products_path: str -- Path to file order_products.csv
            mapping: dict {int : int} -- Hash table returned by function get_prod_dept_map
            report: Report object -- Stores all Department objects that are used to generate output

    """
    with open(order_products_path, 'r') as infile:
        next(infile)
        for line in infile:
            entry = line.strip().split(',')
            # get the department id that the current product belongs to
            dept_ID = mapping[int(entry[1])]
            # based on dept_ID, get the corresponding Department object that needs to be updated
            currDept = report.get_dept(dept_ID)
            currDept.orders += 1
            # increment first_orders attribute if reordered = 0
            currDept.first_orders += -(int(entry[-1]) - 1)

    # "percentage" attibute of "Department" is calculated only after reading entire log
    # Alternatively, it can also be updated upon reading each line of the file
    report.update_percentage()


def main():
    """ Driver function. """
    # read paths of in-/output files
    ORDER_PRODUCTS_PATH = argv[1]
    PRODUCTS_PATH = argv[2]
    OUTPUT_PATH = argv[3]

    # process input and write output
    report = Report()
    prod_dept_map = get_prod_dept_map(PRODUCTS_PATH)
    process_order_prod(ORDER_PRODUCTS_PATH, prod_dept_map, report)
    report.write_to_file(OUTPUT_PATH)


if __name__ == '__main__':
    main()
