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
import re #regular expression
#mechanicalsoup = mechanize + beautifulsoup
import mechanicalsoup

import webbrowser
import cgi
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


  printTop()










  header = ['I','E','T','R']
    #f = open('firstsem.html','w')
  credit = []
  points = []
  head = []
  subjects = {}
  nested_list = []
  tot_credits = 24
  failure = [0,0,0,0,0,0,0,0]
  usn1 = "1SG17CS001"
  usn2 = "1SG17CS005"
  fail = 0 # counter for failures
  fcd = 0 # counter for FCDs
  fc = 0 # counter for first class
  sc = 0 #counter for second Class
  pas = 0 # counter for number of pass
  total = 0# counter for total number of students
  res = '0'
  withheld = [0,0,0,0,0,0,0,0,0]
  wt_flag = 0
  wt = 0

  def cal_grade(marks_list):
      if (marks_list>='90' or marks_list =='100'):
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


  def extract(us):
      browser = mechanicalsoup.StatefulBrowser()
      browser.open(url)
      form = browser.select_form(nr=0)
      form.set("lns", us)
      response = browser.submit(form,url)
      html =  response.content
      return html
  #end of extract()

  def header_disp(check):
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

      if(check == '17PHY12'):
        for i in range(0,42,6):
            head.append(marks_list[i])
        #head.sort()
        for i in range(0,7): # displays the subject code as the column header.
            htmlc += """<th colspan="4" scope="colgroup"> %s </th>
            """ %(head[i])
      else:
        for i in range(0,48,6):
            head.append(marks_list[i])
        #for i in range(0,8):


        for i in range(0,8): # displays the subject code as the column header.
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

      if(check == '17PHY12'):
          for i in range(0,7):
              for j in header :

                  htmlc += """
                  <th scope="col"> %s </th>
                  """ % j
      else:
          for i in range(0,8):
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

  #dip_flag = 0



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
  #dip_const = dip_usn1[0:7]
  #dip_count = int(dip_usn1[7:])

  #end_point_dip = int(dip_usn2[7:])
  #dip_flag = 0

  #us = '1SG15CS120'
  url = 'http://results.vtu.ac.in/vitaviresultcbcs/index.php'

  while count< (end_point+1) :
      #if dip_flag==0:

      if(count<10):
              us = const+z+z1+str(count)
      elif(count>= 10 and count<100):
              us = const+z+str(count)
      else:
              us = const+str(count)
          #end of if-elif-else
      #else:
          #us = dip_const+str(count)
      #end of if-else
      html = extract(us)
      if (html.find('17MAT11')< 0) :
              count+=1
              #print us
              # if dip_flag==0 and count == end_point+1:
              #     dip_flag=1
              #     count = dip_count
              #     end_point = end_point_dip
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
  # 0-68: header of the table
  #headers are removed
              marks_list = marks1[70:].splitlines()
              marks_list = filter(None,marks_list)
              check_str = marks_list[6]
              if(check_str == '17PHY12'):
                for i in range(0,42,6):
                  if marks_list[i+4] == 'W':
                    wt_flag = 1
                    sub_list = [marks_list[i+2], '_' , marks_list[i+3],marks_list[i+4]]

                    marks_list.insert(i+3,'-')
                    subjects[marks_list[i]] = sub_list

                  else:
                    sub_list = [marks_list[i+2],marks_list[i+3],marks_list[i+4],marks_list[i+5]]
                    subjects[marks_list[i]] = sub_list
              else :
                for i in range(0,48,6):
                  if marks_list[i+4] == 'W':
                    wt_flag = 1

                    sub_list = [marks_list[i+2], '_' , marks_list[i+3],marks_list[i+4]]

                    marks_list.insert(i+3,'-')
                    subjects[marks_list[i]] = sub_list

                  else:
                    sub_list = [marks_list[i+2],marks_list[i+3],marks_list[i+4],marks_list[i+5]]
                    subjects[marks_list[i]] = sub_list


      #print marks_list
              for i in range(0,42,6):
                if( marks_list[i].find('L') > 0 and marks_list[i].find('17ELN15') < 0 and marks_list[i].find('17ELE15') < 0):
                    credit.append(2)

                else:
                    credit.append(4)


              #subjects.sort(key=lambda sublist: sublist[0])



                  #end of if-elif-else
              #end of for
              count+=1
              total+=1



              name = name_list[3] #name of the student. Eg- : Varsha N Urs
              name1 = name[2:]
              if header_flag == 1 : #to display the header only once
                header1=  header_disp(check_str)
                  #f.write(html_head)
                header_flag = 0
              #end of if
              htmlc1 = """</tr>
              <tr>
              <td scope="row">  %s </td>
              <td scope="row"> %s </td>""" %(us,name1)
              if check_str == '17PHY12':
                for i in range (0,7):
                  for j in range (0,4):

                    htmlc1 += """<td> %s </td>""" %subjects[header1[i]][j]

              else:
                for i in range (0,8):
                  for j in range (0,4):

                    htmlc1 += """<td> %s </td>""" %subjects[header1[i]][j]
              #end of if-else

              for i in range (4,42,6):
                  points = cal_grade(marks_list[i])
                  #end of nested-for
              sum = 0
              total_points = 0
              for i,j in zip(range(0,7),range(0,7)):
                  total_points += points[i] * credit[j]
              if wt_flag == 0:
                gpa  =  round((total_points/ float(tot_credits)),3)

                for i in range(4,42,6):
                  sum += int (marks_list[i])
                  #end of for
                perc =  round((sum / float(7)),3)
              else:
                gpa = 'WITHHELD'
                sum = 'WITHHELD'
                perc = 'WITHHELD'

              htmlc1+= """<td> %s </td>
              <td> %s </td>
              <td> %s </td>""" %(sum,perc,gpa)
              list_perc = [us,name1,sum,perc,gpa]
              nested_list.append(list_perc)


              for i in range(5,42,6):
                if marks_list[i] == "F" or marks_list[i] == "A" :
                  res = "FAIL"
                  fail += 1
                  break
              for i in range(5,42,6):
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
              # for i in range(5,42,6):
              #     if marks_list[i] == "F" or marks_list[i] == "A" :
              #         res = "FAIL"
              #         fail += 1
              #         break
                  #end of if
          #end of for
              htmlc1+= "<td> %s </td> </tr>" %(res)
              # if dip_flag==0 and count == end_point+1:
              #     dip_flag=1
              #     count = dip_count
              #     end_point = end_point_dip



              res = '0'
              wt_flag = 0
              del points[0:]
              del credit[0:]

              if check_str == '17PHY12':
                for i in range (1,42,6):
                  if marks_list[i+4] == 'F' or marks_list[i+4] == 'A':
                    failure[i/6] +=1
                  if marks_list[i] == "W" and marks_list[i] != "F" :
                    withheld[i/6] +=1
              else:
                for i in range (1,48,6):
                  if marks_list[i+4] == 'F' or marks_list[i+4] == 'A':
                    failure[i/6] +=1
                  if marks_list[i] == "W" and marks_list[i] != "F" :
                    withheld[i/6] +=1
              subjects.clear()
              print htmlc1
  #end of else
  #end of while

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
  </table>""" %(total,pas-wt,fail,fcd,fc,sc,wt)

  #print total,pas,fail,fcd,fc,sc
  nested_list.sort(key=lambda sublist: sublist[2],reverse=True)
  #print nested_list
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
  #     for i in range(1,42,6):
  if check_str == '17PHY12':
    for i in range(0,42,6):
      html += """  <th scope="col"> %s </th>""" %marks_list[i]
    html +="""</tr><tr><th scope="row"> Total number of Students </th>"""
    for i in range(0,42,6):
        html+="<td> %s </td>" %total
    html +="""</tr><tr><th scope="row"> Total number of Pass  </th>"""
    for i in range(0,42,6):
        html+="<td> %s </td>" % (total-(failure[i/6]+withheld[i/6]))
    html+=  "</tr> <tr> <th scope='row'> Total number of Failures</th> "

    for i in range(0,42,6):
        html+="<td> %s </td>" % failure[i/6]
    html+=  "</tr> <tr> <th scope='row'> Total number of Withheld results</th> "
    for i in range(0,7):
      print"<td> %s </td>" % withheld[i]
    html+=  "</tr> <tr> <th scope='row'> Pass Percentage</th> "
    for i in range(0,42,6):
        pass_perc = round((((total-(failure[i/6]+withheld[i/6])) / float(total)) * 100),3)
        html+="<td> %s </td>" %pass_perc
    html+="</tr> </table>"

  else:
    header_r = []
    pass_list = []
    for i in range(0,48,6):
      html += """  <th scope="col"> %s </th>""" %marks_list[i]
      header_r.append(marks_list[i])
    html +="""</tr><tr><th scope="row"> Total number of Students </th>"""
    for i in range(0,48,6):
        html+="<td> %s </td>" %total
    html +="""</tr><tr><th scope="row"> Total number of Pass  </th>"""
    for i in range(0,48,6):
        html+="<td> %s </td>" % (total-(failure[i/6]+withheld[i/6]))
    html+=  "</tr> <tr> <th scope='row'> Total number of Failures</th> "
    for i in range(0,48,6):
        html+="<td> %s </td>" % failure[i/6]
    html+=  "</tr> <tr> <th scope='row'> Total number of Withheld results</th> "
    for i in range(0,8):
      html+="<td> %s </td>" % withheld[i]
    html+=  "</tr> <tr> <th scope='row'> Pass Percentage</th> "
    for i in range(0,48,6):
        pass_perc = round((((total-(failure[i/6]+withheld[i/6])) / float(total)) * 100),3)
        html+="<td> %s </td>" %pass_perc
        pass_list.append(pass_perc)
    html+="</tr> </table>"





  print html
  import plotly

  plotly.tools.set_credentials_file(username='rheasanjan', api_key='hl5WmJhx6sHA8JEE7idx')
  import plotly.plotly as py
  import plotly.graph_objs as go


  trace0 = go.Bar(
      x=header_r,
      y=pass_list,

      marker=dict(
          color='rgb(150,250,225)',
          line=dict(
              color='rgb(8,48,107)',
              width=1.1,
          )
      ),
      opacity=0.8
  )

  data = [trace0]
  layout = go.Layout(
      title='Pass Percentage',
  )

  fig = go.Figure(data=data, layout=layout)
  py.plot(fig, filename='text-hover-bar1')

  # import plotly.tools as tls
  # tls.get_embed('https://plot.ly/~rheasanjan/2/pass-percentage/')
  html_graph = """<div>
  <a href='https://plot.ly/~rheasanjan/2/pass-percentage/'> click me
  </a>
    </div>"""
  #
  # <img src=\"https://plot.ly/~rheasanjan/2/pass-percentage/ \" style="width:400px;height:500px;" /> </a>

  print html_graph
  tail()
