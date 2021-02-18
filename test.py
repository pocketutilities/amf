student_tuples = [
    {'name': 'john', 'group': 'A', 'age': '15.5'},
    {'name': 'jane', 'group': 'B', 'age': '10.8'},
    {'name': 'dave', 'group': 'B', 'age': '12.2'},
]
student_tuples = sorted(student_tuples, key=lambda student: float(student['age']))  # sort by age
for entry in student_tuples:
    print("-----------------")
    print(entry['name'])
    print(entry['group'])
    print(entry['age'])