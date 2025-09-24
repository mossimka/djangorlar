from django.shortcuts import render

# Create your views here.
def users_view(request):
    users: list[dict[str, str | int]] = [
        {'id': 1, 'name': 'Alice', 'age': 30},
        {'id': 2, 'name': 'Bob', 'age': 25},
        {'id': 3, 'name': 'Charlie', 'age': 35},
        {'id': 4, 'name': 'Diana', 'age': 28},
        {'id': 5, 'name': 'Ethan', 'age': 32},
        {'id': 6, 'name': 'Fiona', 'age': 27},
        {'id': 7, 'name': 'George', 'age': 29},
        {'id': 8, 'name': 'Hannah', 'age': 31},
        {'id': 9, 'name': 'Ian', 'age': 26},
        {'id': 10, 'name': 'Jane', 'age': 33},
    ]
    return render(request, 'users.html', {'users': users})