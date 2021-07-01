from django.http import JsonResponse
import re, csv


def convert_employee_to_1d_array(data):
    """ to convert employee data to 1d array """
    transformed_data = []
    transformed_data.append(data['FirstName']+' '+ data['LastName'])
    transformed_data.append(data['Department']+' '+data['Designation'])
    transformed_data.append("$ {0:,.0f}".format(int(data['Salary'])))
    transformed_data.append(data['Address']+', '+data['City']+', '+data['Email']+' and '+data['Mobile'])

    return transformed_data


def report(request):
    """ Reports based on empoyee details  """

    # department data
    departments_data = {}

    # reading department data from csv file
    with open('employee_data/Departments.csv') as departments:
        # iterating over the department data
        for row in csv.DictReader(departments, skipinitialspace=True):
            # assigning department data to department id to access department with department id
            departments_data[row['Id']] = row

    # employees salary data
    employees_salary_data = {}

    # salary details 
    employee_wise_salary = {}

    # reading employees salary data from csv file
    with open('employee_data/Employees Salary.csv') as employees_salary:
        # iterating over the employees salary data
        for row in csv.DictReader(employees_salary, skipinitialspace=True):
            # assigning salary data to employee id to access salary with employee id
            employees_salary_data[row['EmployeeId']] = row
            # employee salary
            employee_wise_salary[row['EmployeeId']] = int(row['Salary'].replace(',',''))

    # employees salary data
    employees_data = {}

    # department wise employee data
    department_wise_employee_data = {}

    # active employee with active department
    active_employee_with_active_department = {}

    # employee email domains list
    employee_email_domains_list = []

    # transformed data
    Employee_data_oned_array = []

    # department wise salary grouping
    department_wise_salary_grouping = {}

    total_salary_by_gender = {'Male':0,'Female':0}


    # reading employees data from csv file
    with open('employee_data/Employees.csv') as employees:
        # iterating over the employees data
        for row in csv.DictReader(employees, skipinitialspace=True):
            
            # getting department status
            department_status = departments_data[row['Department']].get('Status') if departments_data.get(row['Department'],None) else ''

            # updating employee salary with employee id
            row['Salary'] = employees_salary_data[row['Id']].get('Salary').replace(',','') if employees_salary_data.get(row['Id'],None) else ''

            # updating employee salary with employee id
            row['Department'] = departments_data[row['Department']].get('Name') if departments_data.get(row['Department'],None) else ''

            # assigning employee data to employee id to access employee with employee id
            employees_data[row['Id']] = row

            # grouping employee based on department
            if row['Department'] not in department_wise_employee_data:
                department_wise_employee_data[row['Department']] = [row]
                department_wise_salary_grouping[row['Department']] = int(row['Salary'])
            else:
                department_wise_employee_data[row['Department']].append(row)
                department_wise_salary_grouping[row['Department']] = department_wise_salary_grouping[row['Department']] + int(row['Salary'])

            # grouping active employee with active department
            if department_status == 'Active' and row['Status'] == 'Active':
                active_employee_with_active_department[row['Id']] = row

            # getting domain from email
            domain = re.search("@[\w.]+", row['Email'])
            
            if domain:
                # generating domain list
                employee_email_domains_list.append(domain.group().lstrip("@"))

            # transforming dict to array with extra format
            Employee_data_oned_array.append(convert_employee_to_1d_array(row))

            # grouping salary based on gender
            total_salary_by_gender[row['Gender']] += int(row['Salary'])
            

    # over all report
    report = {}

    # employee data
    report["EmployeeData"] = employees_data 
    
    # department wise employee data
    report["DepartmentWiseEmployeeData"] = department_wise_employee_data
    
    # active employee with active department
    report["ActiveEmployeeWithActiveDepartment"] = active_employee_with_active_department

    # most popular email domain
    report["MostPopularEmailDomain"] = max(employee_email_domains_list, key=employee_email_domains_list.count)

    # Employee Data OneD Array
    report["EmployeeDataOneDArray"] = Employee_data_oned_array

    # Highly Ranked Department Salary Based
    report["HighlyRankedDepartmentSalaryBased"] = max(department_wise_salary_grouping, key=department_wise_salary_grouping.get)

    # highly ranked employee salary based
    highly_ranked_employee_salary_based = employees_data[max(employees_data, key=employee_wise_salary.get)]

    # Highly Ranked Department Salary Based
    report["HighlyRankedEmployeeSalaryBased"] = highly_ranked_employee_salary_based['FirstName']+' '+ highly_ranked_employee_salary_based['LastName']

    # Highly Ranked Department Salary Based
    report["TotalSalaryByGender"] = total_salary_by_gender

    return JsonResponse(report, safe=False)