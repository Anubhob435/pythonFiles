
marks = 75
attendance = 75
backlogs = False
teacher_not_like_student = False
student_not_like_teacher = False
male = False
colour = "White"
female = False

"""college eelegible placement strategy"""

def eligible_students(students):
    if marks < 75:
        return "Not Eligible"
    if attendance < 75:
        return "Not Eligible"
    if backlogs == True:
        return "Not Eligible"
    if teacher_not_like_student:
        return "Not Eligible" 
    if student_not_like_teacher:
        return "Not Eligible"
    if male:
        return "Not Eligible"
    if female:
        return "Not Eligible"
    if colour == "Black":
        return "Not Eligible"
    else:
        return "Not Eligible"
    
