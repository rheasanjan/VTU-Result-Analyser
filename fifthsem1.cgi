#!/usr/bin/env python

# The range of usn is given manually.
# The first usn is taken as usn1 and the last usn is taken as usn2.
# The result of the usn's between usn1(included) and usn2(included) is displayed.
# usn1 and usn2 are split into three parts: constant, zeros and count(in case of usn1)/end_point(in case of usn2)
# ---------- version 8-----------------#
# Total marks and percentage of each student is calculated and displayed.
# The result is displayed. If the student has failed in one subject, then the result is FAIL. If their percentage is >= 70, then its FCD, if its >=60 and <60, then its FC
# If its >=50 and <60, then its second Class
# Total number of students, number of pass, number of fcds,number of FCs,number of SCs and number of failures is displayed in a separate table at the end.
# GPA of each student is calculated.


from bs4 import BeautifulSoup as bs
import mechanicalsoup
import webbrowser
import cgi
from collections import OrderedDict
from collections import defaultdict

def printTop():
  print """Content-type:text/html\n\n
    <!doctype html>
    <html>
     <head>
     <link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css\">
    <script src=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js\"> </script>
     <script src=\"https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js\"></script>

     <meta charset="utf-8"/>

     <title> server-side </title>
     </head>
     <body>"""

def tail():
    print """</body> </html>"""


if __name__ == "__main__":

  formData = cgi.FieldStorage()
  usn1 = formData.getvalue('usn1')
  usn2 = formData.getvalue('usn2')
  dip_usn1 = formData.getvalue('dip_usn1')
  dip_usn2 = formData.getvalue('dip_usn2')

  printTop()

  header1 = []
  htmlc1 = " "
  stu_data = OrderedDict()
  subject_tot = OrderedDict() #stores the total number students for each subject
  subject_fail = OrderedDict() #total number of students failed in each subject
  subject_wt = OrderedDict() #total number of withheld results in each subject
  header = ['I','E','T','R'] # stands for Internals,Externals,Total,Result
  #f = open('result.html','w')
  credit = [] # a list that stores the number of credits for each subject
  points = [] # a list that stores the points earned for each subject
  nested_list = [] # a list used to store name,usn, percentage and gpa of students so that it can be sorted and the top 3 students info can be displayed.
  tot_credits = 26 # total credits
  failure = [0,0,0,0,0,0,0,0]
  wt = 0 #counter for Withheld results
  withheld = [0,0,0,0,0,0,0,0]
  wt_flag = 0

  # usn1 = "1RN15CS001"
  # usn2 = "1RN15CS010"
  # dip_usn1 = "1RN16CS401" #diploma usn
  # dip_usn2 = "1RN16CS410"
  fail = 0 # counter for failures
  fcd = 0 # counter for FCDs
  fc = 0 # counter for first class
  sc = 0 #counter for second Class
  pas = 0 # counter for number of pass
  total = 0 # counter for total number of students

  res = '0'


  def cal_grade(marks_list): #function to calculate points and grade
    if (marks_list>='90' or marks_list== '100'):
        p = 10

        grade = 'S+'
    elif(marks_list<'90' and marks_list>='80'):
        p=9

        grade = 'S'
    elif(marks_list<'80' and marks_list>='70'):
        p=8

        grade = 'A'
    elif(marks_list<'70' and marks_list>='60'):
        p=7

        grade = 'B'
    elif(marks_list<'60' and marks_list>='50'):
        p=6

        grade = 'C'
    elif(marks_list<'50' and marks_list>='40'):
        p=5

        grade = 'D'
    elif(marks_list<'40' and marks_list>='30'):
        p=4

        grade = 'E'
    else:
        p=0
        grade = 'F'
        #end of if-elif-else
    return p
    #end of cla_grade() function


  def extract(us): #to extract the data from the html page
    browser = mechanicalsoup.StatefulBrowser()
    browser.open(url)
    form = browser.select_form(nr=0)
    form.set("lns", us)
    response = browser.submit(form,url)
    html =  response.content
    return html
  #end of extract()

  def header_disp(head): #to display header just once
    htmlc = """
    <table class='table table-bordered table-striped table-hover'>
    <col>
    <colgroup span="9"></colgroup>
    <colgroup span="9"></colgroup>
    <tr>

    <th colspan="2" scope="colgroup"> Student Info </th>"""



    #head.sort()
    for i in range(0,len(head)): # displays the subject code as the column header.
        htmlc += """<th colspan="4" scope="colgroup"> %s </th>
        """ %(head[i])
    #end of for
    # other column headers:-
    htmlc += """ <th> Total </th>
        <th> Perc </th>
        <th> SGPA </th>
        <th> Class </th>
        </tr> <tr>
        <th scope="col"> USN </th>
        <th scope="col"> STUDENT NAME </th>
        """


    for i in range(0,len(head)): # for displaying the internal,external and total marks, and results for each subject
        for j in header :

            htmlc += """
                <th scope="col"> %s </th>
                """ % j
    #end of nested-for
    # these headers have only no sub headers
    htmlc += """<th colspan="1" scope="colgroup">  </th>
                <th colspan="1" scope="colgroup">  </th>
                <th colspan="1" scope="colgroup">  </th>"""




    print htmlc

  #end of header_disp()

  const = usn1[0:7] # the constant part of the usn

  dip_flag = 0

  #splitting usn1
  if usn1[7] == '0':
    z = '0'
    if usn1[8] == '0':
        z1 = '0'
        count = int(usn1[9])
    else:
        count = int(usn1[8:])
  else:
    count = int(usn1[7:])
  #end of if-else

  header_flag = 1

  #splitting usn2
  if usn2[7] == '0':
    if usn2[8] == '0':
        end_point = int(usn2[9])
    else:
        end_point = int(usn2[8:])
  else:
    end_point = int(usn2[7:])
  #end of if-else
  dip_const = dip_usn1[0:7]
  dip_count = int(dip_usn1[7:])

  end_point_dip = int(dip_usn2[7:])
  dip_flag = 0

  #us = '1SG15CS120'
  url = 'http://results.vtu.ac.in/vitaviresultcbcs/index.php'

  while count< (end_point+1) :
    if dip_flag==0:

        if(count<10):
            us = const+z+z1+str(count)
        elif(count>= 10 and count<100):
            us = const+z+str(count)
        else:
            us = const+str(count)
        #end of if-elif-else
    else:
        us = dip_const+str(count)
    #end of if-else
    html = extract(us)
    if (html.find('15CS51')< 0 and html.find('15EE51') < 0 and html.find('15EC51') < 0  and html.find('15ME51') < 0 and html.find('15BT51') < 0 and html.find('15CV51') < 0) :
          count+=1
          if dip_flag==0 and count == end_point+1:
              dip_flag=1
              count = dip_count
              end_point = end_point_dip
    else :
            soup = bs(html, "lxml") #parser
  #end of if-else
  #findall returns a list.
            info = soup.findAll('div',{'class' : 'col-md-12 table-responsive'})
            name_usn =  info[0].text #name_usn is a string
            name_usn1 = name_usn.strip() #starting and ending whitespace removed            name_list = name_usn1.splitlines()
            name_list = name_usn1.splitlines()
            name_list = filter(None,name_list)
            tds = soup.findAll('div', {'class': 'divTable'})
            marks = tds[0].text
            marks1 = marks.strip()
            name = name_list[3] #name of the student. Eg- : Varsha N Urs
            name1 = name[2:]
            name_usn_list = [us,name1] #List which holds the USN and the name of the student
            name_and_usn = tuple(name_usn_list) #List converted to tuple to use it as a key in the dictionary. Keys in a dictionary should be immutable.
  # 0-68: header of the table
  #headers are removed
            marks_list = marks1[70:].splitlines()
            marks_list = filter(None,marks_list)
            subjects = {} # A dictionary that uses subject codes as keys and a list of I,E,T,R as values.
            #If the result is withheld, then in marks_list add an hyphen in place of External marks.
            for i in range(0,48,6):
              if marks_list[i+4] == 'W':
                wt_flag = 1
                sub_list = [marks_list[i+2], '_' , marks_list[i+3],marks_list[i+4]]
                marks_list.insert(i+3,'-')
                subjects[marks_list[i]] = sub_list
              else:
                sub_list = [marks_list[i+2],marks_list[i+3],marks_list[i+4],marks_list[i+5]]
                subjects[marks_list[i]] = sub_list
            stu_data[name_and_usn] = subjects


            #subjects.sort(key=lambda sublist: sublist[0])

                #end of if-elif-else
            #end of for
            count+=1
            total+=1


            if header_flag == 1 : #to display the header only once
              for i in range(0,48,6):
                  header1.append(marks_list[i]) #Initially, let header1 contain subject codes of the first student
              #end of for
              header_flag = 0
            #end of if

            for key in subjects.keys():
              # If a student has taken an elective that is not present in header1, then add that subject to header1
              if key not in header1:
                 header1.append(key)
              #end of if
            #end of for


            if dip_flag==0 and count == end_point+1:
                dip_flag=1
                count = dip_count
                end_point = end_point_dip

            del name_and_usn
            del name_usn_list
            del sub_list
            del subjects




  #end of else
  #end of while
  #Display the header
  header_disp(header1)
  sub_credit = dict()

  for i in range(0,len(header1)):
      if( header1[i].find('CSL') > 0):
          sub_credit[header1[i]] = 2
      elif(len(header1[i]) == 7 and header1[i].find('MAT') <0 ):
          sub_credit[header1[i]] = 3
      else:
          sub_credit[header1[i]] = 4


  #Initialize the dictionaries
  for i in range (0,len(header1)):
    subject_tot[header1[i]] = 0
    subject_fail[header1[i]] = 0
    subject_wt[header1[i]] = 0

  #Print details of each student
  for k in stu_data.keys():


    sum = 0
    total_points = 0
    sub_points = dict()

    htmlc1+= """</tr>
    <tr>
    <td scope=\"row\">  %s </td>
    <td scope=\"row\"> %s </td>""" %(k[0],k[1])
    for i in range(0,len(header1)):
      #If the student has not taken this elective,then print '-' under the subject code column
      if header1[i] not in stu_data[k].keys():
        for j in range(0,4):
          htmlc1+= "<td> - </td> "
      else:
        for j in range(0,4):
        #  print stu_data[k][header1[i]][j]
          htmlc1+="""<td> %s </td>""" %stu_data[k][header1[i]][j]
      #Increment the counter
        subject_tot[header1[i]]+=1
        #perc =  round(((sum / float(900))*100),3)
    if wt_flag == 0:
      for m in stu_data[k]:
        points = cal_grade(stu_data[k][m][2])
        sub_points[m] = points
        sum += int (stu_data[k][m][2])
      perc =  (sum / float(8))
        #end of nested-form

      for m in sub_points.keys():
        total_points += sub_points[m] * sub_credit[m]
      gpa  =  round((total_points/ float(tot_credits)),2)
    else:
      gpa = 'WITHHELD'
      sum = 'WITHHELD'
      perc = 'WITHHELD'

    htmlc1+= """<td> %s </td>
    <td> %s </td>
    <td> %s </td>""" %(sum,perc,gpa)
    list_perc = [k[0],k[1],sum,perc,gpa]
    nested_list.append(list_perc)


    for m in stu_data[k]:
      # If the student has failed in a subject or is absent, the result is FAIL
      if stu_data[k][m][3] == "F" or stu_data[k][m][3] == "A" :
        res = "FAIL"
        fail += 1
        break
      #end of if

      if stu_data[k][m][3] == "W" and stu_data[k][m][3] != "F" :
        res = "WITHHELD"
        wt +=1
        break
      #end of if
    #end of for

    if res is '0':

      if perc >= 70:
        fcd += 1
        res = 'FCD'

      elif perc >= 60 and perc < 70 :
        res = 'FC'
        fc += 1
      elif perc >= 50 and perc < 60:
          res = "SC"
          sc += 1
      elif perc>=40:
          res = "PASS"
        #end of if-elif

        #end of if

    htmlc1+= "<td> %s </td> </tr>" %(res)

    for m in stu_data[k]:
      if stu_data[k][m][3] == 'F' or stu_data[k][m][3] == 'A':
        subject_fail[m]+=1
      #end of if
      if stu_data[k][m][3] == "W" and stu_data[k][m][3] != "F" :
        subject_wt[m][2]+=1
      #end of if
    #end of for




    del sub_points #delete this
    res = '0'
    #end of for {for k in stu_data.keys()}
  htmlc1+= "</tr>"
  print htmlc1

  pas = total - fail
  html = """</table>
  <table class='table table-bordered table-striped table-hover'>
  <caption> Results </caption>
  <tr>
  <th scope="col"> Total number of Students </th>
  <th scope="col"> Total number of Pass  </th>
  <th scope="col"> Total number of Failures</th>
  <th scope="col"> Total number of FCDs</th>
  <th scope="col"> Total number of FCs </th>
  <th scope="col"> Total number of SCs </th>
  <th scope=\"col\"> Total number of Withheld results </th>
  </tr>
  <tr>
  <td> %d </td>
  <td> %d </td>
  <td> %d </td>
  <td> %d </td>
  <td> %d </td>
  <td> %d </td>
  <td> %d </td>
  </tr>
  </table>""" %(total,(pas-wt),fail,fcd,fc,sc,wt)


  nested_list.sort(key=lambda sublist: sublist[2],reverse=True)

  html+=""" <table class=' table table-bordered table-striped table-hover'> <caption> Top 3 Students </caption><tr> <th> Rank </th><th> USN </th>
  <th> Name </th>
  <th> Total Marks </th>
  <th> Percentage </th>
  <th> GPA </th></tr>"""
  for i in range(0,3):
    html+= " <tr> <td> %s </td> " %(i+1)
    html+= """<td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td><td> %s </td></tr>""" %(nested_list[i][0],nested_list[i][1],nested_list[i][2],nested_list[i][3],nested_list[i][4])
  html+="</table>"

  html+="""<table> <table class='table table-bordered table-striped table-hover'> <caption> ANALYSIS FOR EACH SUBJECT </caption> <tr> <td> </td>"""
  for j in header1:
      html+=""" <th scope=\"col\"> %s </th>""" %j
  html+="""</tr><tr><th scope=\"row\"> Total number of Students </th>"""
  for j in subject_tot.keys():
    html+="<td> %s </td>" %subject_tot[j]
  html+="""</tr><tr><th scope=\"row\"> Total number of Pass  </th>"""
  for j in header1:
    html+="<td> %s </td>" % (subject_tot[j]-(subject_fail[j]+subject_wt[j]))
  html+="</tr> <tr> <th scope='row'> Total number of Failures</th> "
  for j in subject_fail.keys():
    html+="<td> %s </td>" % subject_fail[j]
  html+="</tr> <tr> <th scope='row'> Total number of Withheld results</th> "
  for j in subject_wt.keys():
    html+="<td> %s </td>" %subject_wt[j]
  html+="</tr> <tr> <th scope='row'> Pass Percentage</th> "
  for j in header1:
    pass_perc = round(((( subject_tot[j]-(subject_fail[j]+subject_wt[j]))/ float(subject_tot[j])) * 100),3)
    html+="<td> %s </td>" %pass_perc
  html+="</tr> </table>"
  print html
  tail()
