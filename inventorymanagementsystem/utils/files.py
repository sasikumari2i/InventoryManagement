import csv

from pathlib import Path

from inventorymanagementsystem import settings


def create_products(product_uid):
    """Read employees.txt file as csv and convert
    into the list of employee dictionary
    """
    # print(request.data['inventories'])
    products = list()
    heading = list()
    csv_file = request.data['inventories']
    # ifile = open(csv_file, "rb")
    # csv_reader = csv.reader(csv_file)
    line_count = 0
    for row in csv_file:
        index = row.decode().replace('\r\n', '').split(',')
        if line_count == 0:
            heading = index
            line_count = 1
        else:
            inventory = Inventory(serial_no=index[0])
            products.append(inventory)

    inventories = Inventory.objects.bulk_create(products)
    print(inventories)

    # line_count = 0
    #
    # for row in csv_reader:
    #     if line_count == 0:
    #         line_count += 1
    #     else:
    #         employee = dict(name=row[0], email=row[1])
    #
    #         employees.append(employee)
    #         line_count += 1
    #
    # print(employees)
    # csv = b64.b64decode(request.data['inventories']).decode('utf-8').split(',')
    # for v in csv:
    #     print(v)