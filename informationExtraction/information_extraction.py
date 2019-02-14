#####################################################################
'''
 # Regular Expression to extract contact information of faculties at CS Department UTD
 # @author Bhargav Lenka
'''
#####################################################################

#importing libraries
import sys
import re

# giving input and output paths
input_path = sys.argv[1]
output_path = sys.argv[2]
data = []
professorSet = set()

# writing output text file
f = open(output_path, "w")

# dictionary of regular expressions to extract information
rx_dict = {
    'faculty': re.compile(r'<a href=.*>(.*?)</a>'),
    'position': re.compile(r'((\w+.*)?Professor)'),
    'email': re.compile(r'(mailto:)?([a-z0-9 .]+@\w+.edu)'),
    'phone': re.compile(r'\d{3}.(\d{4})'),
}

# parsing line function to extract information
def parse_line(line):
    for key, rx in rx_dict.items():
        match = rx.search(line)
        if match:
            return key, match
    return None, None


# appending information to data list
with open(input_path, 'r') as file_object:
    line = file_object.readline()
    while line:
        key, match = parse_line(line)

        # extract faculty
        if key == 'faculty':
            faculty = match.group(1)
            if faculty != "Website" and faculty != "Webite":
                data.append(faculty)

        # extract position
        if key == 'position':
            position = match.group(1)
            data.append(position)
            professorSet.add(position)

        # extract email
        if key == 'email':
            email = match.group(2)
            data.append(phone)

        # extract phone number
        if key == 'phone':
            phone = match.group(1)
            data.append(phone)

        # writing to text file
        if (line.startswith('</tr></p>')):
            if data[1] in professorSet and len(data) >= 3:
                #print(data)
                for i in data:
                    f.write(i + "   ")
                f.write("\n")
            data = []
        line = file_object.readline()
f.close()

