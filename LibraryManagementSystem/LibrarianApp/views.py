from django.shortcuts import render
import pymysql
# Create your views here.
def index(request):
    return render(request,"LibrarianApp/index.html")

def librarianlogin(request):
    return render(request, "LibrarianApp/librarianlogin.html")

def libaction(request):
    uname=request.POST['username']
    pwd=request.POST['password']
    if uname=='admin' and pwd=='root':
        return render(request,'LibrarianApp/librarianhome.html')
    else:
        context={'msg':'Librarian Login Failed..!'}
        return render(request,'LibrarianApp/librarianlogin.html', context)
    
def adddept(request):
    return render(request,"LibrarianApp/adddept.html")

def deptAction(request):
    d=request.POST["dept_name"]
    con=pymysql.connect(host='localhost',user='root', password='root', database="vg_lib")
    cur=con.cursor()
    cur.execute("select * from department where dept='"+d+"'")
    data=cur.fetchone()
    if data is not None:
        context={'data': 'Departement Already Exist..!!!'}
        return render(request, 'LibrarianAPP/adddept.html',context)
    else:
        i=cur.execute("insert into department values (null, '"+d+"')")
        con.commit()
        if i > 0:
            context={'data': 'Departement Added Successfully..!!'}
            return render(request,'LibrarianApp/adddept.html',context)
        else:
            context={'data': 'Departement Adding Failed..!!'}
            return render(request, 'LibrarianAPP/adddept.html',context)
    
def addRacks(request):
    con=pymysql.connect(host='localhost', user='root', password='root', database='vg_lib')
    cur=con.cursor()
    cur.execute("select * from department")
    data=cur.fetchall()
    tdata="<tr><td><select name='dept' required style='width:300px; height:50px;border-radius: 20px;'>"
    tdata+="<option>Choose Department</option>"
    for d in data:
        tdata+="<option>"+str(d[1])+"</option>"
    tdata+="</select></td></tr>"
    context={'msg': tdata}
    return render(request, 'LibrarianAPP/addrack.html',context)

def rackAction(request):
    d=request.POST['dept']
    rno=request.POST['rno']
    con=pymysql.connect(host='localhost',user='root',password='root',database='vg_lib')
    cur=con.cursor()
    i=cur.execute("insert into racks values(null,'"+d+"','"+rno+"','waiting','waiting')")
    con.commit()
    if i > 0:
        cur.execute("select * from department")
        data=cur.fetchall()
        tdata="<tr><td><select name='dept' required style='width: 300px; height:50px;border-radius: 20px;'>"
        tdata+="<option></option>"
        for d in data:
            tdata+="<option>"+str(d[1])+"</option>"
        tdata+="</select></td></tr>"
        context={'msg':tdata, 'data':'Rack Added Successfully..!!!!'}
        return render(request, 'LibrarianApp/addrack.html',context)
    else:
        context={'mag':tdata, 'data': 'Rack Adding Failed..!!!'} 
        return render(request, 'LibrarianApp/addrack.html',context)

def home(request):
    return render(request,"LibrarianApp/librarianhome.html")

def addbooks(request):
    con=pymysql.connect(host='localhost', user='root', password='root', database='vg_lib')
    cur=con.cursor()
    cur.execute("select * from department")
    data=cur.fetchall()
    tdata="<tr><td><select name='dept' required style='width:300px; height:50px;border-radius: 20px;'>"
    tdata+="<option>Choose Department</option>"
    for d in data:
        tdata+="<option>"+str(d[1])+"</option>"
    tdata+="</select></td></tr>"
    context={'msg': tdata}
    return render(request, 'LibrarianAPP/addbooks.html',context)

def choosedept(request): 
    d=request.POST['dept']
    con=pymysql.connect(host='localhost', user='root', password='root', database='vg_lib')
    cur=con.cursor()
    cur.execute("select Rack_NO from racks where Dept_Name='"+d+"'")
    data=cur.fetchall()
    tdata="<tr><td><select name='rno' required style='width:300px; height:50px;border-radius: 20px;'>"
    tdata+="<option>Available Racks</option>"
    for a in data:
        tdata+="<option>"+str(a[0])+"</option>"
    tdata+="</select></td></tr>"
    n=request.POST["rno"]
    o=request.POST['bookname']
    p=request.POST['authorname']
    cur.execute("update racks SET Book_name='"+o+"', Author='"+p+"' WHERE Dept_Name='"+d+"' AND Rack_No='"+n+"'")
    con.commit()
    context={'msg': tdata, "dept_data": d,"rack_data":n }
    return render(request, 'LibrarianApp/rackdetails.html',context)