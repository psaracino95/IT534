import xml.etree.ElementTree as ET

def parse_employee_data(xml_path):
    """
    Parses the cleaned XML file and extracts employee information.
    Returns a list of dicts with keys: 'name', 'title', 'profile_pic'
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    employees = []
    for employee in root.findall("employee"):
        emp_info = {
            "name": employee.find("name").text,
            "title": employee.find("title").text,
            "profile_pic": employee.find("profile_pic").text
        }
        employees.append(emp_info)
        
    return employees