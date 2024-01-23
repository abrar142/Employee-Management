from django.shortcuts import render,redirect
from .form import EmployeeForm,EmployeeSalaryForm, DepartmentForm
from .models import Employee,Department,EmployeeSalary

# Create your views here.

def Home(request):
    return render(request,'home.html')


def Emp(request):
    return render(request,'emp.html')

def Add_Employee(request):
    if request.method == 'POST':
        f = EmployeeForm(request.POST)
        f.save()
        return redirect('/')
    else:
        f = EmployeeForm
        context = {'form': f}
        return render(request,'addemp.html', context)
    

def Department_Form(request):
    f = DepartmentForm
    context = {'form': f}
    return render(request,'department.html', context)


def Employee_List(request):
    departments = Department.objects.all()

    data = {}
    for department in departments:
        managers = Employee.objects.filter(department=department, designation='Manager')
        team_leads = Employee.objects.filter(department=department, designation='TL')
        
        data[department.name] = {
            'managers': managers,
            'team_leads': {}
        }

        for tl in team_leads:
            associates = Employee.objects.filter(department=department, reporting_manager=tl)
            data[department.name]['team_leads'][tl.name] = {
                'team_lead': tl,
                'associates': associates
            }

    return render(request, 'emplist.html', {'data': data})

def Add_Salary(request):
    if request.method == 'POST':
        f = EmployeeSalaryForm(request.POST)
        f.save()
        return redirect('/')
    else:
        f = EmployeeSalaryForm
        context = {'form': f}
        return render(request,'addsalary.html', context)


def Salary_List(request):
    start_date = request.GET.get('start_date', '2022-01-01')
    end_date = request.GET.get('end_date', '2022-12-31')

    departments = Department.objects.all()
    data = {}

    for department in departments:
        employees = Employee.objects.filter(department=department)
        total_cost = 0

        for employee in employees:
            salaries = EmployeeSalary.objects.filter(employee=employee, start_date__lte=end_date, end_date__gte=start_date)

            for salary in salaries:
                total_cost += salary.salary

        data[department.name] = total_cost

    return render(request, 'salarylist.html', {'data': data})



def Edit(request,id):
    e = Employee.objects.get(id=id)

    if request.method == 'POST':
        f = EmployeeForm(request.POST, instance=e)
        f.save()
        return redirect('/emplist')
    
    else:
        f = EmployeeForm(instance=e)
        d = {'form': f}
        return render(request,'addemp.html',d)
    

def Delete(request):
    eid = request.GET.get('id')
    e = Employee.objects.get(id=eid)
    e.delete()
    return redirect('/emplist')