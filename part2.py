import flask
from flask import jsonify, request
import requests

app = flask.Flask(__name__)
app.config["Debug"] = True

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'}


# For some reason, the script loves to randomly give a JSONDecodeError after trying to make more than one request.
# I'm assuming it's an issue with the API that I was supposed to use for this, but I genuinely have no idea.
# If you do run into the error, just re-run the program a few times and it should work. I promise.
# Justin M


def get_employees():
    response = requests.get("http://dummy.restapiexample.com/api/v1/employees", headers=headers)
    employees = response.json()["data"]
    for e in employees:
        print("\nEmployee Id: " + str(e["id"]) + "\nName: " + e["employee_name"] + "\nSalary: " + str(
            e["employee_salary"]) + "\nAge: " + str(e["employee_age"]))
        if e["id"] == 10:
            enter_input = input("\nWould you like to see the remaining employees? If so, please press enter. ")
            if enter_input == "":
                print("Resuming....")
            else:
                print("Exiting....")
                break


def get_emp_by_id(emp_id):
    response = requests.get("http://dummy.restapiexample.com/api/v1/employee/" + str(emp_id), headers=headers)
    return response.json()["data"]


def create_employee(emp_name, emp_salary, emp_age):
    response = requests.post("http://dummy.restapiexample.com/api/v1/create",
                             data={'employee_name': emp_name,
                                   'employee_salary': emp_salary,
                                   'employee_age': emp_age
                                   }, headers=headers)
    return response.json()["data"]


def update_employee(emp_id, emp_name, emp_salary, emp_age):
    response = requests.put("https://dummy.restapiexample.com/api/v1/update/" + str(emp_id),
                            data={'employee_name': emp_name,
                                  'employee_salary': emp_salary,
                                  'employee_age': emp_age,
                                  'profile_image': ''
                                  }, headers=headers)
    return response.json()["data"]


def delete_employee(emp_id):
    employee_info = get_emp_by_id(emp_id)
    delete_confirm = input(
        "Are you sure you want to delete employee {}? Y/y or N/n".format(employee_info['employee_name']))
    if delete_confirm == 'Y' or delete_confirm == 'y':
        response = requests.delete("https://dummy.restapiexample.com/api/v1/delete/" + str(emp_id), headers=headers)
        return response.json()
    else:
        return {}


def get_avg_salary():
    total_salary = 0
    total_employees = 0
    response = requests.get("http://dummy.restapiexample.com/api/v1/employees", headers=headers)
    employees = response.json()["data"]
    for e in employees:
        total_salary += e["employee_salary"]
        total_employees += 1
    avg_sal = total_salary / total_employees
    return "The Average Salary is {:.2f}$".format(avg_sal)


def show_age_info():
    lowest_salary = 10000000
    highest_salary = 0
    total_salary = 0
    total_employees = 0
    age_1 = input("Please enter the lowest number in the employee age range. ")
    age_2 = input("Please enter the highest number in the employee age range. ")
    age_1_int = int(age_1)
    age_2_int = int(age_2)
    response = requests.get("http://dummy.restapiexample.com/api/v1/employees", headers=headers)
    employees = response.json()["data"]
    for e in employees:
        if e["employee_age"] >= age_1_int or e["employee_age"] <= age_2_int:
            total_employees += 1
            total_salary += e["employee_salary"]
            if lowest_salary > e["employee_salary"]:
                lowest_salary = e["employee_salary"]
            if highest_salary < e["employee_salary"]:
                highest_salary = e["employee_salary"]
    avg_age_sal = total_salary / total_employees
    return "\nInfo from Employees aged {} to {}:\nLowest Salary: {}$\nAverage Salary: {}$\nHighest Salary: {}$".format(
        str(age_1), str(age_2), str(lowest_salary), str(avg_age_sal), str(highest_salary))


user_input = input(
    "Please make a selection: \n1. Get All Employees\n2. Get Employee by Id\n3. Create Employee\n4. Update an Employee\n5. Delete an Employee\n6. Get Average Salary\n7. Get Age Range\n8. Quit")

while True:

    if user_input == '1':
        print(get_employees())

    if user_input == '2':
        empNum = input("Please enter a valid employee number: ")
        if int(empNum):
            print(get_emp_by_id(empNum))

    if user_input == '3':
        empl_name = input("Please enter the employee name.")
        empl_salary = input("Please enter the employee's salary.")
        empl_age = input("Please enter the employee's age.")

        empl_salary = int(empl_salary)
        empl_age = int(empl_age)
        print(create_employee(empl_name, empl_salary, empl_age))

    if user_input == '4':
        empl_id = input("Please enter the employee's id number.")
        empl_name = input("Please enter the employee name.")
        empl_salary = input("Please enter the employee's salary.")
        empl_age = input("Please enter the employee's age.")

        empl_id = int(empl_id)
        empl_salary = int(empl_salary)
        empl_age = int(empl_age)
        print(update_employee(empl_id, empl_name, empl_salary, empl_age))

    if user_input == '5':
        empl_id = input("Please enter the employee's id number. ")
        print(delete_employee(empl_id))

    if user_input == '6':
        print(get_avg_salary())

    if user_input == '7':
        print(show_age_info())

    if user_input == '8':
        break

    user_input = input(
        "\nPlease make a selection: \n1. Get All Employees\n2. Get Employee by Id\n3. Create Employee\n4. Update an Employee\n5. Delete an Employee\n6. Get Average Salary\n7. Get Age Range\n8. Quit")
