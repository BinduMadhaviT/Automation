import os
import pypyodbc as db
import zipfile
import datetime
import string
def createcon():
    dbname = input("Enter Database Name: ")
    sname = input("Enter Server you want to connect to: ")
    uname = input("Enter UID: ")
    pwd = input("Enter Password: ")
    try:
        conn = db.connect("Driver={SQL Server};Server="+sname+";Database="+dbname+";uid="+uname+";pw="+pwd+";Trusted_Connection=true;")
    except:
        print("One of the parameters is wrong!!!")
        exit()
    cursor = conn.cursor()
    return [cursor,conn]
def sqlexec(f_name, tup):
    fw.write("File Name: "+f_name+"\n")
    try:
        fhand=open(f_name)
    except:
        print("Wrong File name!!!!")
        exit()
    sqlfile=fhand.read()
    sqlc=sqlfile.split(';')
    for command in sqlc:
        try:
            if command[:6].lower() == "select":
                tup[0].execute(command)
                title = [i[0] for i in tup[0].description]
                print(title)
                for row in tup[0]:
                    print(row)
                fw.write("Command executed: "+str(datetime.datetime.now())+"\n")
            else:
                tup[0].execute(command)
                tup[1].commit()
                fw.write("Command executed: "+str(datetime.datetime.now())+"\n")
        except(db.Error) as msg:
            if str(str(msg).lstrip()).startswith("(\'HY090\'"):
                continue
            else:
                print("Command Skipped: ",msg)
                tup[1].rollback()
                fw.write("Command not executed: "+str(datetime.datetime.now()))
                fw.write(" Error: "+str(msg)+"\n")  
    print(f_name," is executed")
    fw.write("\n")
def recexec(dname):
    if os.path.isfile(dname):
        if dname.endswith('.sql'):
                sqlexec(dname, tup)
                print('exec: ', dname)
    else:            
        for (dirname, dirs, files) in os.walk(dname):
            for filename in files:
                if filename.endswith('.sql') :
                    sqlexec(os.path.join('./'+dname, filename), tup)
                    print('exec: ',filename)
def repexec(dirc):
    for (dirname, dirs, files) in os.walk(dirc):
            for filename in files:
                if filename.endswith('.sql'):
                    sqlexec(os.path.join('./'+dirc, filename), tup)
                    print('exec: ', filename)
fw = open('Report.txt','w+')
file_name =input("Enter name of zip file: ")
print('Extracting ZIP.')
archive = zipfile.ZipFile(file_name+'.zip', 'r')
file_name = file_name+'__dir'
if os.path.exists(file_name) : 
    os.rmdir(file_name)
else :
    os.mkdir(file_name)
archive.extractall('./'+file_name)
print('ZIP Extracted.')
dirList = os.listdir(file_name)
print(dirList)
tup = createcon()
for dirc in dirList:
    dirc = os.path.join(file_name, dirc)
    if os.path.isdir(dirc):
        print(dirc)
        repexec(dirc)
    else:
        print(dirc)
        recexec(dirc)
archive.close()
