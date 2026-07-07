#Peter Saracino 
## 7/7/2026
### IT-534
class Person():

    def __init__(self, name, email, id, program, degree, institution):
        self.name = name
        self.email = email
        self.id = id
        self.program = program
        self.degree = degree
        self.institution = institution

    def displayInformation(self):
        print("Name: " + self.name)
        print("Email: " + self.email) # Fixed: changed self.name to self.email
        print("ID: " + self.id)

class Student(Person): # Fixed: Added inheritance

    def __init__(self, name, email, id, program): # Fixed: Added missing parameters and self
        super().__init__(name, email, id, program, None, None)
        self.program = program

    def displayInformation(self): # Fixed: Added self
        super().displayInformation()
        print("Program: " + self.program)

class Instructor(Person): # Fixed: Added inheritance

    def __init__(self, name, email, id, degree, institution): # Fixed: Added missing parameters and self
        super().__init__(name, email, id, None, degree, institution)
        self.degree = degree
        self.institution = institution

    def displayInformation(self): # Fixed: Added self
        super().displayInformation()
        print("Degree: " + self.degree)
        print("Institution: " + self.institution)

class Validator():

    def __init__(self):
        # Fixed: Appended '_list' at end
        self.validate_name_list = ['!','"','@','#','$','%','^','&','*','(',')','_','=','+',',','<','>','/','?',';',':','[',']','{','}','\\']
        self.validate_email_list = ['!','"','\'','#','$','%','^','&','*','(',')','=','+',',','<','>','/','?',';',':','[',']','{','}','\\']


    def validate_name(self, passed_name):
        if passed_name and isinstance(passed_name, str): # Fixed: Changed 'and str' to proper checking
            for character in passed_name:
                if character in self.validate_name_list: # Fixed: Referenced self.validate_name_list
                    return False # Fixed: Return false if a bad character
            return True # Fixed: Return true only if it survives the whole loop
        else:
            print("Your name cannot be blank")
            return False
    
    def validate_email(self, passed_email):
        if passed_email and isinstance(passed_email, str): # Fixed: Changed 'and str' to proper checking
            has_bad_chars = False
            for character in passed_email:
                if character in self.validate_email_list: # Fixed: Referenced self.validate_email_list
                    has_bad_chars = True
                    break # Fixed: Break early if a bad character is hit
            if not has_bad_chars:
                return True 
            else:
                print("Your email has bad characters in it")
                return False
        else:
            print("Your email cannot be blank")
            return False 

    def validate_user_type(self, passed_type):
        if passed_type.lower() == "s" or passed_type.lower() == "i": # Fixed: Added () to .lower()
            return True
        else:
            print("The provided user type is invalid")
            return False

    def validate_student_id(self, passed_id):
        if len(passed_id) <= 5 and passed_id.isdigit(): # Fixed: Changed .len() to len() and changed to 5 digits
            return True
        else:
            print("The provided student ID is invalid")
            return False
    
    def validate_instructor_id(self, passed_id): #Fixed: Indented inside Validator
        if len(passed_id) <= 5 and passed_id.isdigit(): # Fixed: Changed .len() to len() checked for digits
            return True
        else:
            print("The provided instructor ID is invalid") # Fixed: Changed to 'instructor ID'
            return False 

    def validate_value(self, passed_value): # Fixed: Indented inside Validator class
        if passed_value:
            return True 
        else:
            print("You must provide a value")
            return False

college_records = []
my_validator = Validator()

while True:

    ind_type_valid = False 
    while ind_type_valid == False:
        ind_type = input("Are you a Student or Instructor? Type: 'S' or 'I' ")
        ind_type_valid = my_validator.validate_user_type(ind_type)

    ind_name_valid = False
    while ind_name_valid == False: 
        your_name = input("Enter your name: ")
        ind_name_valid = my_validator.validate_name(your_name) # Fixed: assigned to ind_name_valid to stop loop

    ind_email_valid = False
    while ind_email_valid == False: 
        your_email = input("Enter your email: ")
        ind_email_valid = my_validator.validate_email(your_email)

    if ind_type.lower() == "s": # Fixed: Added () to .lower() and fixed indentation

        ind_id_valid = False
        while ind_id_valid == False: 
            your_id = input("Enter your Student ID: ")
            ind_id_valid = my_validator.validate_student_id(your_id) # Fixed: Typo

        ind_program_valid = False
        while ind_program_valid == False: 
            your_program = input("Enter your Program of Study: ")
            ind_program_valid = my_validator.validate_value(your_program)

        tmp_student = Student(your_name, your_email, your_id, your_program) # Fixed: Instantiated class object using () instead of tuple
        college_records.append(tmp_student)

    else: # Fixed: Corrected alignment and indentation of the else block
        ind_id_valid = False
        while ind_id_valid == False: 
            your_id = input("Enter your Instructor ID: ")
            ind_id_valid = my_validator.validate_instructor_id(your_id)

        ind_degree_valid = False
        while ind_degree_valid == False: 
            your_degree = input("Enter your Highest Degree: ")
            ind_degree_valid = my_validator.validate_value(your_degree)

        ind_institution_valid = False
        while ind_institution_valid == False: 
            your_institution = input("Enter the Last Instiution you Graduated from: ")
            ind_institution_valid = my_validator.validate_value(your_institution)

        tmp_instructor = Instructor(your_name, your_email, your_id, your_degree, your_institution) # Fixed: Swapped {} to ()
        college_records.append(tmp_instructor)

    keep_going = input("Would you like to add another record (Y/N)? ") # Fixed: Changed keyword 'continue' to 'keep_going'  Causes issues
    if keep_going.lower() == "n": # Changed: Added () to .lower()
        break

# Fixed: Loops through and prints individual data element
print("\n--- Saved Records ---")
for record in college_records:
    record.displayInformation()
    print("-" * 20)