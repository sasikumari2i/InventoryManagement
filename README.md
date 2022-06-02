# Inventory Management
An Inventory Management and Asset Maintainance Application for an Organisation

Django Inventory Management is aiming to provide a SaaS application for Inventory Management 
using Django rest framework, which is still in development phase. Major purpose of the application
is order products from a vendor and track the inventory of those products. Assign a product to a User 
and track the records of that product. Record the invoice and payments of the orders.

## Django Inventory supports 

- Categories, Products, Inventories 
- Users, Vendors and the Orders
- Assigned Assets, Assets in Repair Status
- Invoices and Payments
- Multi tenancy

### Note :
Django Inventory Management is still in development phase and only has the fundamental positive 
flows required and it has to be developed according to the requirements

### Installed Apps : 
Different apps created for the development are as follows. These are added to the Installed Apps
list field in **settings.py** file

- products 
- orders
- organisations
- assets
- payments


### Prerequisites:
- Git clone the main branch from the remote repository into the local repository
- install virtual environment using 
```{pip install virtualenv}```
- Create a Virtual environment for the project in a separate directory using  
```{virtualenv <my_env_name>}```
- Keep the virtual environment directory parallel to the project directory
- Activate the virtual environment using command in cmd
 ```{virtual_environment_name}\scripts\activate``` 
- To install the required packages for the application use the requirement.txt file in the git 
- Command to install the required packages are 
```pip install -r requirement.txt ```
- Mention the database details in the ```settings.py``` file in the project
- Add the created the apps in the "Installed apps" list in settings.py file
- Run the following command from the base directory to execute the migration scripts in the apps ```python manage.py migrate {app-name}```  
- Run the project using the command ```python manage.py runserver```
