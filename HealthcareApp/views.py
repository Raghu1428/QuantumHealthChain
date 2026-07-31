from django.shortcuts import render
from datetime import datetime
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os
from datetime import datetime
import json
from web3 import Web3, HTTPProvider
import pickle
import time
import base64
import QuantumEncryption
from QuantumEncryption import *
import Kyber
from Kyber import *

global username, doctor, prescriptionList, usersList
global contract, web3

#function to call contract
def getContract():
    global contract, web3
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Healthcare.json' #Healthcare contract file
    deployed_contract_address = '0xdE940b526440D1f0f9D6baBb3Ce8BEbfE698E0D3' #contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
getContract()

def getUsersList():
    global usersList, contract
    usersList = []
    count = contract.functions.getUserCount().call()
    for i in range(0, count):
        user = contract.functions.getUsername(i).call()
        password = contract.functions.getPassword(i).call()
        phone = contract.functions.getPhone(i).call()
        email = contract.functions.getEmail(i).call()
        address = contract.functions.getAddress(i).call()
        desc = contract.functions.getDescription(i).call()
        utype = contract.functions.getUserType(i).call()
        usersList.append([user, password, phone, email, address, desc, utype])

def getPrescriptionList():
    global prescriptionList, contract
    prescriptionList = []
    count = contract.functions.getEhrCount().call()
    for i in range(0, count):
        uname = contract.functions.getPatient(i).call()
        docname = contract.functions.getDoctor(i).call()
        disease = contract.functions.getDisease(i).call()
        report = contract.functions.getReport(i).call()
        prescription = contract.functions.getPrescription(i).call()
        ehr_date = contract.functions.getEhrDate(i).call()
        prescriptionList.append([uname, docname, disease, report, prescription, ehr_date])
getUsersList()
getPrescriptionList()

def ViewReport(request):
    if request.method == 'GET':
        global dec_time
        filename = request.GET.get('file', False)
        data = quantumDecryptMessage("HealthcareApp/static/files/"+filename)
        response = HttpResponse(data,content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename='+filename
        return response

def GeneratePrescriptionAction(request):
    if request.method == 'POST':
        global prescriptionList
        pid = request.POST.get('t1', False)
        prescription = request.POST.get('t2', False)
        filename = request.FILES['t3'].name
        myfile = request.FILES['t3'].read()
        if os.path.exists("HealthcareApp/static/files/"+filename):
            os.remove("HealthcareApp/static/files/"+filename)
        key = computeQuantumKeys(myfile)
        iv, ciphertext = quantumEncryptMessage(myfile, key, "HealthcareApp/static/files/"+filename)
        contract.functions.updatePrescription(int(pid), prescription+"#"+filename).transact()
        pl = prescriptionList[int(pid)]
        pl[4] = prescription+"#"+filename
        data = "Prescription Updated Successfully"
        context= {'data':data}
        return render(request,'DoctorScreen.html', context)

def GeneratePrescription(request):
    if request.method == 'GET':
        global username
        pid = request.GET['pid']
        output = '<tr><td><font size="3" color="black">Appointment&nbsp;ID</td><td><input type="text" name="t1" size="25" value="'+pid+'" readonly/></td></tr>'
        context= {'data':output}
        return render(request,'GeneratePrescription.html', context)    
    
def ViewAppointments(request):
    if request.method == 'GET':
        global username, prescriptionList
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Appointment ID</font></th>'
        output+='<th><font size=3 color=black>Patient Name</font></th>'
        output+='<th><font size=3 color=black>Doctor Name</font></th>'
        output+='<th><font size=3 color=black>Disease Details</font></th>'
        output+='<th><font size=3 color=black>Report Name</font></th>'
        output+='<th><font size=3 color=black>Prescription</font></th>'
        output+='<th><font size=3 color=black>Booking Date</font></th>'
        output+='<th><font size=3 color=black>View Report</font></th>'
        output+='<th><font size=3 color=black>Generate Pescription</font></th></tr>'
        for i in range(len(prescriptionList)):
            pl = prescriptionList[i]
            if pl[1] == username and exchangeKeys(pl[0], pl[1]):
                output+='<tr><td><font size=3 color=black>'+str(i+1)+'</font></td>'
                output+='<td><font size=3 color=black>'+str(pl[0])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(pl[1])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(pl[2])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(pl[3])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(pl[4])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(pl[5])+'</font></td>'
                output+='<td><a href=\'ViewReport?file='+pl[3]+'\'><font size=3 color=blue>Click Here</font></a></td>'                
                if pl[4] == 'None':
                    output+='<td><a href=\'GeneratePrescription?pid='+str(i)+'\'><font size=3 color=blue>Click Here for Prescription</font></a></td></tr>'
                else:
                    output+='<td><font size=3 color=black>'+pl[4]+'</font></td></tr>'
        context= {'data':output}            
        return render(request,'DoctorScreen.html', context)                
        
def ViewPrescription(request):
    if request.method == 'GET':
        global prescriptionList, username
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Patient Name</font></th>'
        output+='<th><font size=3 color=black>Doctor Name</font></th>'
        output+='<th><font size=3 color=black>Disease Details</font></th>'
        output+='<th><font size=3 color=black>Report Name</font></th>'
        output+='<th><font size=3 color=black>Prescription</font></th>'
        output+='<th><font size=3 color=black>Prescription File Name</font></th>'
        output+='<th><font size=3 color=black>Download Prescription</font></th>'
        output+='<th><font size=3 color=black>Date</font></th></tr>'
        for i in range(len(prescriptionList)):
            pl = prescriptionList[i]
            if pl[0] == username:
                prescription = pl[4]
                print(prescription)
                pres = "None"
                fname = "-"
                file_hash = "-"
                if prescription != 'None':
                    arr = prescription.split("#")
                    pres = arr[0]
                    fname = arr[1]                    
                output+='<tr><td><font size=3 color=black>'+pl[0]+'</font></td>'
                output+='<td><font size=3 color=black>'+pl[1]+'</font></td>'
                output+='<td><font size=3 color=black>'+pl[2]+'</font></td>'
                output+='<td><font size=3 color=black>'+pl[3]+'</font></td>'
                output+='<td><font size=3 color=black>'+pres+'</font></td>'
                output+='<td><font size=3 color=black>'+fname+'</font></td>'
                if prescription == 'None':
                    output+='<td><font size=3 color=black>Pending</font></td>'
                else:
                    output+='<td><a href=\'ViewReport?file='+fname+'\'><font size=3 color=blue>Click Here</font></a></td>'
                output+='<td><font size=3 color=black>'+pl[5]+'</font></td></tr>'
        output += "</table><br/><br/><br/><br/>"
        context= {'data':output}        
        return render(request,'PatientScreen.html', context)      

def AppointmentAction(request):
    if request.method == 'POST':
        global username
        doctor = request.POST.get('t1', False)
        patient = request.POST.get('t2', False)
        disease = request.POST.get('t3', False)
        today = str(datetime.now())
        filename = request.FILES['t4'].name
        myfile = request.FILES['t4'].read()
        if os.path.exists("HealthcareApp/static/files/"+filename):
            os.remove("HealthcareApp/static/files/"+filename)
        key = computeQuantumKeys(myfile)
        iv, ciphertext = quantumEncryptMessage(myfile, key, "HealthcareApp/static/files/"+filename)
        msg = contract.functions.saveEhr(patient, doctor, disease, filename, 'None', today).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
        prescriptionList.append([patient, doctor, disease, filename, 'None', today])
        context= {'data':'Your Appointment Confirmed with Doctor : '+doctor+'<br/>Appointment ID : '+str(len(prescriptionList))+'<br/>'+str(tx_receipt)}
        return render(request, 'PatientScreen.html', context)        

def Appointment(request):
    if request.method == 'GET':
        global username
        doctor = request.GET['doctor']
        today = datetime.now()
        month = today.month
        year = today.year
        day = today.day
        output = '<tr><td><font size="3" color="black">Doctor&nbsp;Name</td><td><input type="text" name="t1" size="25" value="'+doctor+'" readonly/></td></tr>'
        output += '<tr><td><font size="3" color="black">Patient&nbsp;Name</td><td><input type="text" name="t2" size="25" value="'+username+'" readonly/></td></tr>'
        output += '<tr><td><font size="3" color="black">Disease&nbsp;Details</td><td><input type="text" name="t3" size="40" /></td></tr>'
        output += '<tr><td><font size="3" color="black">Upload&nbsp;Medical&nbsp;Report</td><td><input type="file" name="t4" size="40" /></td></tr>'
        context= {'data':output}
        return render(request,'BookAppointment.html', context)      

def BookAppointment(request):
    if request.method == 'GET':
        global usersList
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Doctor Name</font></th>'
        output+='<th><font size=3 color=black>Phone No</font></th>'
        output+='<th><font size=3 color=black>Email ID</font></th>'
        output+='<th><font size=3 color=black>Address</font></th>'
        output+='<th><font size=3 color=black>Description</font></th>'
        output+='<th><font size=3 color=black>Book Appointment</font></th></tr>'
        for i in range(len(usersList)):
            ul = usersList[i]
            if ul[6] == 'Doctor':
                output+='<tr><td><font size=3 color=black>'+ul[0]+'</font></td>'
                output+='<td><font size=3 color=black>'+ul[2]+'</font></td>'
                output+='<td><font size=3 color=black>'+ul[3]+'</font></td>'
                output+='<td><font size=3 color=black>'+ul[4]+'</font></td>'
                output+='<td><font size=3 color=black>'+ul[5]+'</font></td>'
                output+='<td><a href=\'Appointment?doctor='+ul[0]+'\'><font size=3 color=blue>Click Here to Book Appointment</font></a></td></tr>'
        output += "</table><br/><br/><br/><br/>"
        context= {'data':output}        
        return render(request,'PatientScreen.html', context)      

def index(request):
    if request.method == 'GET':
        return render(request,'index.html', {})

def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})
    
def DoctorLogin(request):
    if request.method == 'GET':
       return render(request, 'DoctorLogin.html', {})

def PatientLogin(request):
    if request.method == 'GET':
       return render(request, 'PatientLogin.html', {})

def isUserExists(username):
    is_user_exists = False
    global details
    mysqlConnect = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'doctorpatientapp',charset='utf8')
    with mysqlConnect:
        result = mysqlConnect.cursor()
        result.execute("select * from user_signup where username='"+username+"'")
        lists = result.fetchall()
        for ls in lists:
            is_user_exists = True
    return is_user_exists    

def RegisterAction(request):
    if request.method == 'POST':
        global usersList
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        contact = request.POST.get('t3', False)
        email = request.POST.get('t4', False)
        address = request.POST.get('t5', False)
        desc = request.POST.get('t6', False)
        usertype = request.POST.get('t7', False)
        count = contract.functions.getUserCount().call()
        status = "none"
        for i in range(0, count):
            user1 = contract.functions.getUsername(i).call()
            if username == user1:
                status = "exists"
                break
        if status == "none":
            msg = contract.functions.saveUser(username, password, contact, email, address, desc, usertype).transact()
            tx_receipt = web3.eth.waitForTransactionReceipt(msg)
            usersList.append([username, password, contact, email, address, desc, usertype])
            context= {'data':'Signup Process Completed<br/>'+str(tx_receipt)}
            return render(request, 'Register.html', context)
        else:
            context= {'data':'Given username already exists'}
            return render(request, 'Register.html', context)

def PatientLoginAction(request):
    if request.method == 'POST':
        global username, contract, usersList
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        status = 'none'
        for i in range(len(usersList)):
            ulist = usersList[i]
            user1 = ulist[0]
            pass1 = ulist[1]
            utype = ulist[6]
            if user1 == username and pass1 == password and utype == "Patient":
                status = "success"
                break
        if status == 'success':
            output = 'Welcome '+username
            context= {'data':output}
            return render(request, "PatientScreen.html", context)
        if status == 'none':
            context= {'data':'Invalid login details'}
            return render(request, 'PatientLogin.html', context)
        
def DoctorLoginAction(request):
    if request.method == 'POST':
        global username, contract, usersList
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        status = 'none'
        for i in range(len(usersList)):
            ulist = usersList[i]
            user1 = ulist[0]
            pass1 = ulist[1]
            utype = ulist[6]
            if user1 == username and pass1 == password and utype == "Doctor":
                status = "success"
                break
        if status == 'success':
            output = 'Welcome '+username
            context= {'data':output}
            return render(request, "DoctorScreen.html", context)
        if status == 'none':
            context= {'data':'Invalid login details'}
            return render(request, 'DoctorLogin.html', context)










        


        
