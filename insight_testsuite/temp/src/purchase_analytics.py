import os
from sys import argv


class Department:
    def __init__(self, dept_ID):
        self.ID = dept_ID
        self.orders = 0
        self.first_orders = 0
        self.percentage = 0.0


class Report:
    def __init__(self):
        # department ID : department class
        self.departments = {}
        self.depts_sorted = []

    def get_dept(self, dept_ID):
        if dept_ID not in self.departments:
            self.departments[dept_ID] = Department(dept_ID)
        return self.departments[dept_ID]

    def update_percentage(self):
        for dept in self.departments.values():
            dept.percentage = float(dept.first_orders / dept.orders)

    def sort_depts(self):
        # sort the Department objects by dept_ID
        self.depts_sorted = list(self.departments.values())
        self.depts_sorted.sort(key=lambda x: x.ID)

    def write_to_file(self, output_path):
        self.sort_depts()
        if os.path.isfile(output_path):
            os.remove(output_path)
        # write to the output file
        fout = open(output_path, 'a')
        fout.write("department_id,number_of_orders,number_of_first_orders,percentage\n")
        for dept in self.depts_sorted:
            # A department_id should be listed only if number_of_orders is greater than 0
            if dept.orders > 0:
                fout.write(str("%d,%d,%d,%0.2f\n" % (dept.ID, dept.orders, dept.first_orders, dept.percentage)))
        fout.close()


def get_prod_dept_map(products_path):
    mapping = {}
    with open(products_path) as infile:
        next(infile)
        for line in infile:
            entry = line.strip().split(',')
            prod_ID = int(entry[0])
            dept_ID = int(entry[-1])
            mapping[prod_ID] = dept_ID
    return mapping


def process_order_prod(order_products_path, mapping, report):
    with open(order_products_path) as infile:
        next(infile)
        for line in infile:
            entry = line.strip().split(',')
            dept_ID = mapping[int(entry[1])]
            currDept = report.get_dept(dept_ID)
            currDept.orders += 1
            # increment first_orders attribute if reordered = 0
            currDept.first_orders += -(int(entry[3]) - 1)
    # "percentage" attibute of "Department" is calculated only after reading entire log
    report.update_percentage()


def main():
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
