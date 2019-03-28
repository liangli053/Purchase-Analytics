# Purchase-Analytics

Insight data engineering 2019 coding challenge. Based on Instacart orders, calculate, for each department, the number of times a product was requested, number of times a product was requested for the first time and a ratio of those two numbers.

## Libraries required

os and sys libraies are needed
```
import os
from sys import argv
```

## Implementation

### Explanation of classes and functions

Two classes `Department` and `Report` are defined.

`Department`: Stores the data associated with each department that need to be written to the output file 

    └── Department
        └── __init__
            └── self.ID: int, department ID
            └── self.orders: int, total number of orders
            └── self.first_orders: int, number of first-time orders
            └── self.percentage: float, ratio between self.first_orders and self.orders

`Report`: Stores a dict in which each `Department` object is indexed by department id, as well as a list of sorted `Department` objects. Several methods to sort objects and write output.  

    ├── Report
        └── __init__
        |    └── self.departments: dict {int : Department}, mapping department ID to Department object
        |    └── self.depts_sorted: list [Department], Department objects sorted based on department ID 
        ├── get_dept(self, dept_ID): rtype: Department, return the Department object that needs to be updated
        └── update_percentage(self): rtype: None, calculate the percentage attribute of each Department object
        └── sort_depts(self): rtype: None, sort all Department objects by department ID
        └── write_to_file(self, output_path): rtype: None, write the output to output_path


Three functions are defined:

`get_prod_dept_map(products_path)`: read *products.csv* file and return a dict that maps product id to department id  
- Arguments:  
  - products_path: *str*, path to file *products.csv*  
- Returns:  
  - mapping: *dic{int : int}*, product_id : department_id
	
`process_order_prod(order_products_path, mapping, report)`: read *order_products.csv* and update Department and Report objects  
- Arguments:  
  - order_products_path: *str*, path to file *order_products.csv*  
  - mapping: *dic{int : int}*, hash table returned by `get_prod_dept_map`  
  - report: A *Report* object  
- Returns: None

`main`: main function

### Executation procedure
1. Read in the paths of input and output files.
2. Declare a `Report` object named `report` that stores all `Department` objects.
3. Parse *products.csv* and generate `mapping`, a hash table that maps product id to department id.
3. Parse *order_products.csv*, read in each order entry, update the `orders` and `first_order` attributes of the corresponding `Department` object.
4. After processing entire *order_products.csv* file, calculate the `percentage` atrribute of each `Department` object.
5. Sort all `Department` objects based on department ID, store the sorted list in `reprot.depts_sorted`, and then write the output.
    
## Instruction to run code

1. Clone the git repository
```
git clone
```

2. make run.sh executable
```
cd Purchase-Analytics
chmod u+x run.sh
```

3. run code
```
./run.sh
```
**Output is written in ./output/report.csv**
