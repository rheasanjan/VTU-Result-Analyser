#!/usr/bin/env python

#------------FINAL VERSION 1 ----------#
# The range of usn is given manually.
# The first usn is taken as usn1 and the last usn is taken as usn2.
# The result of the usn's between usn1(included) and usn2(included) is displayed.
# usn1 and usn2 are split into three parts: constant, zeros and count(in case of usn1)/end_point(in case of usn2)

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

  formData = cgi.FieldStorage() #FieldStorage() can used like a python dictionary
  usn1 = formData.getvalue('usn1')
  usn2 = formData.getvalue('usn2')
  dip_usn1 = formData.getvalue('dip_usn1')
  dip_usn2 = formData.getvalue('dip_usn2')



  printTop()

  html_body = " "
  subject_tot = OrderedDict() #stores the total number students for each subject
  subject_fail = OrderedDict() #total number of students failed in each subject
  subject_wt = OrderedDict() #total number of withheld results in each subject
  header = ['I','E','T','R']
  nested_list = [] #a list that is used to contain student usn,name, total marks and percentage
  stu_data = OrderedDict() # A 2D dictinary that contains 'USN,NAME' -{subjectcode - marks pair}pair . I,E,T,R are stored in a list and this list is the value for the key.
  header1 = [] #contains the subjectcodes that act as the header of the table.
  failure = [0,0,0,0,0,0,0,0] # failures in each subject
  # usn1 = "1RN14CS001"
  # usn2 = "1RN14CS003"
  # dip_usn1 = "1RN15CS401"
  # dip_usn2 = "1RN15CS405"
  fail = 0 # counter for failures
  fcd = 0 # counter for FCDs
  fc = 0 # counter for first class
  sc = 0 #counter for second Class
  pas = 0 # counter for number of pass
  total = 0 # counter for total number of students
  wt = 0 #counter for Withheld results
  withheld = [0,0,0,0,0,0,0,0] #list for counting withheld results for each subject
  res = '0' #flag
  wt_flag = 0 #flag for withheld result
  header_flag = 1

  const = usn1[0:7] #constatnt part of usn1
  #initially
  dip_flag = 0



  #splitting usn1
  if usn1[7] == '0': # Example:- 1SG14CS087
    z = '0'
    if usn1[8] == '0': # Example:- 1SG14CS006
      z1 = '0'
      count = int(usn1[9]) #For the above example, count = 6
    else:
      count = int(usn1[8:]) #For the first example, count = 87
      #end of if-else
  else: #Example:- 1SG14CS125
    count = int(usn1[7:]) #For the example, count = 120
  #end of if-else

  #splitting usn2
  if usn2[7] == '0':
    if usn2[8] == '0':
      end_point = int(usn2[9])
    else:
      end_point = int(usn2[8:])
      #end of if-else
  else:
    end_point = int(usn2[7:])
  #end of if-else

  dip_const = dip_usn1[0:7] #Example of diploma USN:- 1SG15CS407
  dip_count = int(dip_usn1[7:])

  end_point_dip = int(dip_usn2[7:]) #number of dip_usn2 is taken as the end point
  dip_flag = 0

  # Fucntion to get the result page.
  def extract(us):
    browser = mechanicalsoup.StatefulBrowser()
    browser.open('http://results.vtu.ac.in/vitaviresultnoncbcs/index.php')
    form = browser.select_form(nr=0)
    form.set("lns", us)
    response = browser.submit(form,'http://results.vtu.ac.in/vitaviresultnoncbcs/index.php')
    html =  response.content #variable html contains the result page
    return html
  #end of extract()

  #Function to display the header
  def header_disp(head):
    html_header= """<table class='table table-bordered table-striped table-hover'>
      <col>
      <colgroup span='9'></colgroup>
      <colgroup span='9'></colgroup>
      <tr>

      <th colspan="2" scope='colgroup'> Student Info </th>"""
    for i in range(0,len(head)):
      # displays the subject code as the column header.
      html_header+= """<th colspan="4" scope="colgroup"> %s </th> """ %(head[i])
    #end of for

    html_header+= """ <th> Total </th>
          <th> Perc </th>

          <th> Class </th>
          </tr> <tr>
          <th scope='col'> USN </th>
          <th scope='col'> STUDENT NAME </th>
          """


    for i in range(0,len(head)):
      for j in header :

          html_header+= """
                  <th scope=\"col\"> %s </th>""" % j
    #end of nested-for
    html_header+= """<th colspan=\"1\" scope=\"colgroup\">  </th>
      <th colspan=\"1\" scope=\"colgroup\">  </th>
      <th colspan=\"1\" scope=\"colgroup\">  </th> """


    print html_header
  #end of header_disp()


  while count< (end_point+1) :
    if dip_flag==0:
      #Constructing the USN using the counter
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
    html = extract(us) #to get the result page
    # if the USN is invalid, skip that USN and move to the next USN.
    if (html.find('10CS71') < 0 and html.find('10EE71') < 0 and html.find('10EC71') < 0  and html.find('10ME71') < 0 and html.find('10BT71') < 0 and html.find('10CV71') < 0 ) :
      count+=1
      #If it is the last USN , then switch to diploma USN
      if dip_flag==0 and count == end_point+1:
        dip_flag=1
        count = dip_count
        end_point = end_point_dip
        #end of if
    else :
      soup = bs(html, "lxml") #parser

      #findall returns a list.
      info = soup.findAll('div',{'class' : 'col-md-12 table-responsive'})
      name_usn =  info[0].text #name_usn is a string
      name_usn1 = name_usn.strip() #starting and ending whitespace removed
      name_list = name_usn1.splitlines()
      name_list = filter(None,name_list)
      tds = soup.findAll('div', {'class': 'divTable'})
      marks = tds[0].text
      marks1 = marks.strip()
      #print marks1
      name = name_list[3]
      name1 = name[2:]
      name_usn_list = [us,name1] #List which holds the USN and the name of the student
      name_and_usn = tuple(name_usn_list) #List converted to tuple to use it as a key in the dictionary. Keys in a dictionary should be immutable.
      # 0-68: header of the table
      #headers are removed
      marks_list = marks1[70:].splitlines()
      marks_list = filter(None,marks_list)
      subjects = {} # A dictionary that uses subject codes as keys and a list of I,E,T,R as values.
      #print marks_list
      for i in range(0,48,6):
          #If the result is withheld, then in marks_list add an hyphen in place of External marks.
          if marks_list[i+4] == 'W':
            wt_flag = 1
            sub_list = [marks_list[i+2], '_' , marks_list[i+3],marks_list[i+4]]
            marks_list.insert(i+3,'-')
            subjects[marks_list[i]] = sub_list

          else:

            sub_list = [marks_list[i+2],marks_list[i+3],marks_list[i+4],marks_list[i+5]]
            #print sub_list
            subjects[marks_list[i]] = sub_list
            #print subjects
      #stu_data uses name_and_usn list as keys and the dictionary subjects as values. It is a 2D dictionary.
      stu_data[name_and_usn] = subjects


      count+=1
      total+=1


      if header_flag == 1 :
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

      # To switch to diploma results
      if dip_flag==0 and count == end_point+1:
       dip_flag=1
       count = dip_count
       end_point = end_point_dip
      #end of if

      # Delete the following variables
      del name_and_usn
      del name_usn_list
      del sub_list
      del subjects





#end of else
#end of while
  #Display the header
  header_disp(header1)
  #Initialize the dictionaries
  for i in range (0,len(header1)):
    subject_tot[header1[i]] = 0
    subject_fail[header1[i]] = 0
    subject_wt[header1[i]] = 0

  #Print details of each student
  for k in stu_data.keys():
    sum = 0

    html_body+= """</tr>
            <tr>
            <td scope=\"row\">  %s </td>
            <td scope=\"row\"> %s </td>""" %(k[0],k[1]) #USN and Name
    #Print marks
    for i in range (0,len(header1)):
      #If the student has not taken this elective,then print '-' under the subject code column
      if header1[i] not in stu_data[k].keys():
        for j in range(0,4):
          html_body+= "<td> - </td> "
      else:
        for j in range(0,4):
          html_body+="""<td> %s </td>""" %stu_data[k][header1[i]][j]
      #Increment the counter
        subject_tot[header1[i]]+=1





    if wt_flag == 0:
      #Calculate the total and percentage if the withheld flag is not set
      for m in stu_data[k]:
        sum += int (stu_data[k][m][2])
        #end of for
      perc =  round(((sum / float(900))*100),3)
    else:
      sum = 'WITHHELD'
      perc = 'WITHHELD'
    #end of if-else


    html_body+="""<td> %s </td>
            <td> %s </td>
            """ %(sum,perc)
    list_perc = [k[0],k[1],sum,perc]
    nested_list.append(list_perc)

    #Find out the result and the class
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

    html_body+= "<td> %s </td> </tr>" %(res)




    for m in stu_data[k]:
      if stu_data[k][m][3] == 'F' or stu_data[k][m][3] == 'A':
        subject_fail[m]+=1
      #end of if
      if stu_data[k][m][3] == "W" and stu_data[k][m][3] != "F" :
        subject_wt[m][2]+=1
      #end of if
    #end of for



    res = '0' #Reset res

  #end of for {for k in stu_data.keys()}
  html_body+= "</tr>"
  print html_body


  pas = total - fail

  print """</table>
  <table class='table table-bordered table-striped table-hover'>
  <caption> Results </caption>
  <tr>
  <th scope=\"col\"> Total number of Students </th>
  <th scope=\"col\"> Total number of Pass  </th>
  <th scope=\"col\"> Total number of Failures</th>
  <th scope=\"col\"> Total number of FCDs</th>
  <th scope=\"col\"> Total number of FCs </th>
  <th scope=\"col\"> Total number of SCs </th>
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

  print""" <table class=' table table-bordered table-striped table-hover'> <caption> Top 3 Students </caption><tr> <th> Rank </th><th> USN </th>
  <th> Name </th>
  <th> Total Marks </th>
  <th> Percentage </th>
  </tr>"""
  for i in range(0,3):
      print " <tr> <td> %s </td> " %(i+1)
      print"""<td> %s </td> <td> %s </td>  <td> %s </td><td> %s </td></tr>""" %(nested_list[i][0],nested_list[i][1],nested_list[i][2],nested_list[i][3])
  print"</table>"
  print"""<table> <table class='table table-bordered table-striped table-hover'> <caption> ANALYSIS FOR EACH SUBJECT </caption> <tr> <td> </td>"""
  for j in header1:
      print""" <th scope=\"col\"> %s </th>""" %j


  print"""</tr><tr><th scope=\"row\"> Total number of Students </th>"""
  for j in subject_tot.keys():
    print"<td> %s </td>" %subject_tot[j]
  print"""</tr><tr><th scope=\"row\"> Total number of Pass  </th>"""
  for j in header1:
    print"<td> %s </td>" % (subject_tot[j]-(subject_fail[j]+subject_wt[j]))
  print"</tr> <tr> <th scope='row'> Total number of Failures</th> "
  for j in subject_fail.keys():
    print"<td> %s </td>" % subject_fail[j]
  print"</tr> <tr> <th scope='row'> Total number of Withheld results</th> "
  for j in subject_wt.keys():
    print"<td> %s </td>" %subject_wt[j]
  print"</tr> <tr> <th scope='row'> Pass Percentage</th> "
  for j in header1:
    pass_perc = round(((( subject_tot[j]-(subject_fail[j]+subject_wt[j]))/ float(subject_tot[j])) * 100),3)
    print"<td> %s </td>" %pass_perc
  print"</tr> </table>"



  tail()
