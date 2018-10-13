#!/usr/bin/env python
# ----------Third sem version 2-----------#
# Diploma students have one extra subject.
# Therefore, one extra subject column has been added and only diploma students' marks is displayed.
# Other students' marks are not displayed in that subject.
# dip_flag variable plays a very important role here. If it is set, then it means the list contains 9 subjects.
# credits and  points lists must contain 9 values for these students.
# total credits for dip students is 32.
# displays the pass perc, no. of failures for each subject
# USN is taken from the client




from bs4 import BeautifulSoup as bs
import re #regular expression
#mechanicalsoup = mechanize + beautifulsoup
import mechanicalsoup

import webbrowser
import cgi #common gateway interface

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

    res = '0'
    head = []
    subjects = {}
    header = ['I','E','T','R']
    #f = open('thirdsem.html','w')
    credit = []
    points = []
    nested_list = []
    tot_credits = 28
    tot_credits_dip = 32 #diploma credits
    failure = [0,0,0,0,0,0,0,0,0]
    # usn1 = "1SG16CS001"
    # usn2 = "1SG16CS002"
    # dip_usn1 ="1SG17CS401"
    # dip_usn2 = "1SG17CS402"
    fail = 0 # counter for failures
    fcd = 0 # counter for FCDs
    fc = 0 # counter for first class
    sc = 0 #counter for second Class
    pas = 0 # counter for number of pass
    total = 0 # counter for total number of students
    wt = 0 #counter for Withheld results
    withheld = [0,0,0,0,0,0,0,0,0]
    dip_tot = 0
    dip_wt = 0
    wt_flag = 0

    def cal_grade(marks_list):
        if (marks_list>='90'):
            p = 10
            points.append(p)
            grade = 'S+'
        elif(marks_list<'90' and marks_list>='80'):
            p=9
            points.append(p)
            grade = 'S'
        elif(marks_list<'80' and marks_list>='70'):
            p=8
            points.append(p)
            grade = 'A'
        elif(marks_list<'70' and marks_list>='60'):
            p=7
            points.append(p)
            grade = 'B'
        elif(marks_list<'60' and marks_list>='50'):
            p=6
            points.append(p)
            grade = 'C'
        elif(marks_list<'50' and marks_list>='40'):
            p=5
            points.append(p)
            grade = 'D'
        elif(marks_list<'40' and marks_list>='30'):
            p=4
            points.append(p)
            grade = 'E'
        else:
            points.append(0)
            grade = 'F'
            #end of if-elif-else
        return points
#end of cal_grade() function

    def extract(us):
        url = 'http://results.vtu.ac.in/vitaviresultcbcs2018/index.php'

        browser = mechanicalsoup.StatefulBrowser()
        browser.open(url)
        browser.select_form(nr=0)
        #get the unique token for each session from the hidden input fields
        token = browser.get_current_page().find('input',type="hidden",id="tokenid")['value']
        # usn = '1SG15CS085'
        browser['lns'] = us
        browser['token'] = token
        browser['current_url'] = url  #set the value of the second hidden input field to current url
        response = browser.submit_selected() #form,url
        html =  response.content #and voila! you get the result! there's nothing you can do to stop us,VTU!!
        return html
    #end of extract()

    def header_disp():
        htmlc = """<!doctype html>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"> </script>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
        <table class='table table-bordered table-striped table-hover'>
        <col>
        <colgroup span="9"></colgroup>
        <colgroup span="9"></colgroup>
        <tr>

        <th colspan="2" scope="colgroup"> Student Info </th>"""


        head.append('15MATDIP41')

        for i in range(0,48,6):
            head.append(marks_list[i])

        #head.sort()
        for i in range(0,9): # displays the subject code as the column header.
            htmlc += """<th colspan="4" scope="colgroup"> %s </th>
            """ %(head[i])

        #end of for
        htmlc += """ <th> Total </th>
            <th> Perc </th>
            <th> SGPA </th>
            <th> Class </th>
            </tr> <tr>
            <th scope="col"> USN </th>
            <th scope="col"> STUDENT NAME </th>
            """


        for i in range(0,9):
            for j in header :

                htmlc += """
                    <th scope="col"> %s </th>
                    """ % j
        #end of nested-for
        htmlc += """<th colspan="1" scope="colgroup">  </th>
                    <th colspan="1" scope="colgroup">  </th>
                    <th colspan="1" scope="colgroup">  </th>"""


        print htmlc
        return head
    #end of header_disp()

    const = usn1[0:7]

    dip_flag = 0 #very important variable. used to calculate gpa,percentage,credits and points of dip students



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

    while count < (end_point+1) :
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
        # print(html)
        if (html.find('15MAT41')< 0) :
                print(count)
                count+=1

                if dip_flag==0 and count == end_point+1:
                    dip_flag=1
                    count = dip_count
                    end_point = end_point_dip
                    # print(count)
        else :
                soup = bs(html, "lxml") #parser
    #end of if-else
    #findall returns a list.
                # print(count)
                info = soup.findAll('div',{'class' : 'col-md-12 table-responsive'})
                name_usn =  info[0].text #name_usn is a string
                name_usn1 = name_usn.strip() #starting and ending whitespace removed            name_list = name_usn1.splitlines()
                name_list = name_usn1.splitlines()
                name_list = filter(None,name_list)
                # print(name_list)
                tds = soup.findAll('div', {'class': 'divTable'})
                marks = tds[0].text
                marks1 = marks.strip()
    # 0-68: header of the table
    #headers are removed
                marks_list = marks1[70:].splitlines()
                marks_list = filter(None,marks_list)
                #print marks_list
                #print marks_list
                if dip_flag==1:
                  for i in range(0,54,6):
                    if marks_list[i+4] == 'W':
                      dip_wt = 1
                      sub_list = [marks_list[i+2], '_' , marks_list[i+3],marks_list[i+4]]

                      marks_list.insert(i+3,'-')
                      subjects[marks_list[i]] = sub_list

                    else:
                      sub_list = [marks_list[i+2],marks_list[i+3],marks_list[i+4],marks_list[i+5]]
                      subjects[marks_list[i]] = sub_list
                else:
                  for i in range(0,48,6):
                    if marks_list[i+4] == 'W':
                      wt_flag = 1
                      sub_list = [marks_list[i+2], '_' , marks_list[i+3],marks_list[i+4]]

                      marks_list.insert(i+3,'-')
                      subjects[marks_list[i]] = sub_list

                    else:
                      sub_list = [marks_list[i+2],marks_list[i+3],marks_list[i+4],marks_list[i+5]]
                      subjects[marks_list[i]] = sub_list

                if dip_flag==1:
                    for i in range(0,54,6):
                        if( marks_list[i].find('CSL') > 0):
                            credit.append(2)
                        elif(len(marks_list[i]) == 7 and marks_list[i].find('MAT') <0 ):
                            credit.append(3)
                        else:
                            credit.append(4)
                            #end of if-elif-else
                        #end of for
                else:
                    for i in range(0,48,6):
                        if( marks_list[i].find('CSL') > 0):
                            credit.append(2)
                        elif(len(marks_list[i]) == 7 and marks_list[i].find('MAT') <0 ):
                            credit.append(3)
                        else:
                            credit.append(4)
                #end of if-else

                count+=1
                total+=1

                name = name_list[3] #name of the student. Eg- : Varsha N Urs
                name1 = name[2:]
                if header_flag == 1 : #to display the header only once
                    header1 = header_disp()
                    #f.write(html_head)
                    header_flag = 0
                #end of if
                htmlc1 = """</tr>
                <tr>
                <td scope="row">  %s </td>
                <td scope="row"> %s </td>""" %(us,name1)
                if dip_flag == 0:

                  if header1[0] == '15MATDIP41':   #if its not a dip student
                    for j in range (0,4):
                      htmlc1 += """<td> - </td>"""

                  for i in range (1,9):
                    for j in range (0,4):
                        htmlc1 += """<td> %s </td>""" %subjects[header1[i]][j]
                            #end of nested-for
                  for i in range (4,48,6):

                      points = cal_grade(marks_list[i])
                    #end of for

                else:               #for dip students

                    for i in range (0,9):
                      for j in range (0,4):

                        htmlc1 += """<td> %s </td>""" %subjects[header1[i]][j]
                    for i in range (4,54,6):
                        points = cal_grade(marks_list[i])
                #end of if-else

                sum = 0
                total_points = 0
                if dip_flag==1:
                    for i,j in zip(range(0,9),range(0,9)):
                        total_points += points[i] * credit[j]
                    #end of for
                    if dip_wt == 0:
                      gpa  =  round((total_points/ float(tot_credits_dip)),3)
                      for i in range(4,54,6):
                        sum += int (marks_list[i])
                      perc =  round((sum / float(9)),3)



                    else:
                        gpa = 'WITHHELD'
                        sum = 'WITHHELD'
                        perc = 'WITHHELD'

                    #end of if-else

                else:
                    for i,j in zip(range(0,8),range(0,8)):
                        total_points += points[i] * credit[j]
                    if wt_flag == 0:
                        gpa  =  round((total_points/ float(tot_credits_dip)),3)
                        for i in range(4,48,6):
                            sum += int (marks_list[i])
                        perc =  round((sum / float(8)),3)
                        # print(sum,perc,gpa)

                    else:
                        gpa = 'WITHHELD'
                        sum = 'WITHHELD'
                        perc = 'WITHHELD'
                    #end of if-else
                #end of if-else

                #end of if-else

                htmlc1+= """<td> %s </td>
                <td> %s </td>
                <td> %s </td>"""  %(sum,perc,gpa)
                if dip_wt == 0 or wt_flag == 0:
                  list_perc = [us,name1,sum,perc,gpa]
                  nested_list.append(list_perc)




                for i in range(5,48,6):
                    if marks_list[i] == "F" or marks_list[i] == "A" :
                        res = "FAIL"
                        fail += 1
                        break
                for i in range(5,48,6):
                  if marks_list[i] == "W" and marks_list[i] != "F" :
                    res = "WITHHELD"
                    wt +=1
                    break
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
            #end of for
                htmlc1+= "<td> %s </td> </tr>" %(res)
                # print(perc,sum,res,gpa)
                # if dip_flag==0 and count == end_point+1:
                #     dip_flag=1
                #     count = dip_count
                #     end_point = end_point_dip




                del points[0:]
                del credit[0:]
                dip_wt = 0
                wt_flag = 0
                res = '0'

                if dip_flag == 1:
                    dip_tot+=1


                if dip_flag == 1:
                    for i in range(1,54,6):
                        if marks_list[i+4] == 'F' or marks_list[i+4] == 'A':
                            failure[i/6] +=1
                        if marks_list[i+4] == "W" and marks_list[i+4] != "F" :
                          withheld[i/6] +=1
                else:
                    for i in range(1,48,6):
                        if marks_list[i+4] == 'F' or marks_list[i+4] == 'A':
                          failure[(i/6)+1] +=1
                        if marks_list[i+4] == "W" and marks_list[i+4] != "F" :
                          withheld[i/6] +=1
                if dip_flag==0 and count == end_point+1:
                    dip_flag=1
                    count = dip_count
                    end_point = end_point_dip

                subjects.clear()
                print htmlc1
    #end of else
    #end of while

    pas = total - fail
    #results analysis
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
    </table>""" %(total,pas-wt,fail,fcd,fc,sc,wt)

    #print total,pas,fail,fcd,fc,sc
    nested_list.sort(key=lambda sublist: sublist[2],reverse=True) #finding top scorers
    #print nested_list

    #Top 3 students
    html+=""" <table class=' table table-bordered table-striped table-hover'> <caption> Top 3 Students </caption><tr> <th> Rank </th><th> USN </th>
    <th> Name </th>
    <th> Total Marks </th>
    <th> Percentage </th>
    <th> GPA </th></tr>"""
    for i in range(0,3): #change the range if you want to display more students' results
        html+= " <tr> <td> %s </td> " %(i+1)
        html+= """<td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td><td> %s </td></tr>""" %(nested_list[i][0],nested_list[i][1],nested_list[i][2],nested_list[i][3],nested_list[i][4])
    html+="</table>"

#subject-wise analysis
    html+= """<table class='table table-bordered table-striped table-hover'> <caption> ANALYSIS FOR EACH SUBJECT </caption> <tr> <td></td> """
    html += """ <th scope="col"> %s </th>""" %header1[0]
    for i in range(1,9):
         # if i == 1:
         #   continue
         html += """  <th scope="col"> %s </th>""" %header1[i]
    html +="""</tr><tr><th scope="row"> Total number of Students </th>
    <td> %s </td>""" % dip_tot
    for i in range(0,8):
        html+="<td> %s </td>" %total
    html +="""</tr><tr><th scope="row"> Total number of Pass  </th>
    <td> %s </td>""" % (dip_tot-(failure[1]+withheld[1]))
    for i in range(0,9):
        if i == 1:
          continue
        html+="<td> %s </td>" % (total-(failure[i]+withheld[i]))
    html+=  "</tr> <tr> <th scope='row'> Total number of Failures</th> "
    html+="<td> %s </td>" % failure[1]
    for i in range(0,9):
        if i == 1:
          continue
        html+="<td> %s </td>" % failure[i]
    html+=  "</tr> <tr> <th scope='row'> Total number of Withheld results</th> "
    html+="<td> %s </td>" %withheld[1]
    for i in range(0,9):
      if i == 1:
        continue
      html+="<td> %s </td>" % withheld[i]


    html+=  "</tr> <tr> <th scope='row'> Pass Percentage</th> "
    pass_perc = round((((dip_tot-(failure[1]+withheld[1])) / float(dip_tot)) * 100),3)
    html+="<td> %s </td>" % pass_perc
    for i in range(0,9):
        if i == 1: #ignore dipmath
          continue
        pass_perc = round((((total-(failure[i]+withheld[i])) / float(total)) * 100),3)
        html+="<td> %s </td>" %pass_perc
    html+="</tr> </table>"



    print html
    tail()
