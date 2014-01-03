from BeautifulSoup import BeautifulSoup
import glob, csv, xlwt, os, time, urllib2

#Look at example urls.txt file in repo
INPUTS = 'urls.txt'
with open(INPUTS) as f:
    lines = f.readlines()

for line in lines:
    filename, url = line.split()
    print "Getting %s" % url
    page = urllib2.urlopen(url)
    content = page.read()
    dom = BeautifulSoup(content)
    table = dom.findAll('table', attrs={'class': 'financialStatement'})[0]
    rows = table.findAll('tr')
    table2d = []
    for rowdata in rows:
        columns = []
        for cell in rowdata:
            key = cell.getText()
            columns.append(key)
        table2d.append(columns)
    titlerow = table2d[0]
    table2d.pop(0)
    titlerow.pop(1)
    print "Writing %s" % filename
    f = open(filename, 'w')
    heading = ','.join(titlerow)
    quotetitlerow = []
    for item in titlerow:
        quotetitlerow.append('"' + item + '"')
    heading = ','.join(quotetitlerow)
    heading = heading + '\n'
    f.write(heading)
    for row in table2d:
        line = []
        for item in row:
            line.append('"' + item + '"')
    linestring = ','.join(line) + '\n'
    f.write(linestring)
    f.close()

#Merge all the CSVs into one file with individual tabs

#Pull the name of tab from the list
f = open(INPUTS, "r")
line = f.readline()
company = line.split("_")[0]
cur_time = time.ctime()

wb = xlwt.Workbook()

#Combine files
for filename in glob.glob("*.csv"):
    (f_path, f_name) = os.path.split(filename)
    (f_short_name, f_extension) = os.path.splitext(f_name)
    ws = wb.add_sheet(f_short_name)
    miss_piggy = csv.reader(open(filename, 'rb'))
    for rowx, row in enumerate(miss_piggy):
        for colx, value in enumerate(row):
            ws.write(rowx, colx, value)
    wb.save("%s_compiled_%s.xls" % (company, cur_time))

#Erase original CSV that were downloaded
file_list = glob.glob("*.csv")

for f in file_list:
    os.remove(f)    