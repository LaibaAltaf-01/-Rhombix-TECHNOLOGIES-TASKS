"""
Task 2: Student Grade Tracker
-------------------------------
A program for tracking student grades and calculating averages.
- Allows users to input grades for different subjects.
- Supports multiple students.
- Calculates per-student averages, letter grades, and class statistics.
"""

students = {}


def get_letter_grade(average):
    """Convert a numeric average into a letter grade."""
    if average >= 90:
        return "A"
    elif average >= 80:
        return "B"
    elif average >= 70:
        return "C"
    elif average >= 60:
        return "D"
    else:
        return "F"


def add_student():
    name = input("Enter student name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    if name in students:
        print(f"'{name}' already exists. Use 'Add grade' to add more subjects.")
        return
    students[name] = {}
    print(f"Student '{name}' added.")


def add_grade():
    if not students:
        print("No students found. Please add a student first.")
        return

    print("Students: " + ", ".join(students.keys()))
    name = input("Enter student name: ").strip()
    if name not in students:
        print(f"Student '{name}' not found.")
        return

    subject = input("Enter subject name: ").strip()
    if not subject:
        print("Subject cannot be empty.")
        return

    while True:
        grade_input = input(f"Enter grade for {subject} (0-100): ").strip()
        try:
            grade = float(grade_input)
            if 0 <= grade <= 100:
                students[name][subject] = grade
                print(f"Grade recorded: {name} - {subject}: {grade}")
                break
            else:
                print("Grade must be between 0 and 100.")
        except ValueError:
            print("Please enter a valid number.")


def calculate_average(subject_grades):
    """Calculate the average of a dict of subject:grade pairs."""
    if not subject_grades:
        return 0.0
    return sum(subject_grades.values()) / len(subject_grades)


def view_student_report():
    if not students:
        print("No students found.")
        return

    print("Students: " + ", ".join(students.keys()))
    name = input("Enter student name: ").strip()
    if name not in students:
        print(f"Student '{name}' not found.")
        return

    subject_grades = students[name]
    print(f"\n--- Report for {name} ---")
    if not subject_grades:
        print("No grades recorded yet.")
        return

    for subject, grade in subject_grades.items():
        print(f"  {subject:<20} {grade:>6.2f}")

    average = calculate_average(subject_grades)
    print(f"  {'-' * 28}")
    print(f"  {'Average':<20} {average:>6.2f}")
    print(f"  {'Letter Grade':<20} {get_letter_grade(average):>6}")


def view_all_students():
    if not students:
        print("No students found.")
        return

    print("\n--- All Students Summary ---")
    print(f"{'Name':<20}{'Subjects':<10}{'Average':<10}{'Letter':<8}")
    print("-" * 48)
    for name, subject_grades in students.items():
        average = calculate_average(subject_grades)
        letter = get_letter_grade(average) if subject_grades else "-"
        print(f"{name:<20}{len(subject_grades):<10}{average:<10.2f}{letter:<8}")


def view_class_statistics():
    all_averages = [
        calculate_average(grades) for grades in students.values() if grades
    ]
    if not all_averages:
        print("No grades recorded yet for any student.")
        return

    class_average = sum(all_averages) / len(all_averages)
    highest = max(all_averages)
    lowest = min(all_averages)

    print("\n--- Class Statistics ---")
    print(f"Number of students with grades: {len(all_averages)}")
    print(f"Class average: {class_average:.2f}")
    print(f"Highest average: {highest:.2f}")
    print(f"Lowest average: {lowest:.2f}")


def print_menu():
    print("\n" + "=" * 40)
    print("STUDENT GRADE TRACKER")
    print("=" * 40)
    print("1. Add student")
    print("2. Add grade for a student")
    print("3. View student report")
    print("4. View all students summary")
    print("5. View class statistics")
    print("6. Exit")


def main():
    while True:
        print_menu()
        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            add_grade()
        elif choice == "3":
            view_student_report()
        elif choice == "4":
            view_all_students()
        elif choice == "5":
            view_class_statistics()
        elif choice == "6":
            print("Exiting Student Grade Tracker. Goodbye!")
            break
        else:
            print("Invalid option. Please choose a number between 1 and 6.")


if __name__ == "__main__":
    main()
