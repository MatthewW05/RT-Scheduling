from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import DateSelectionForm
from .models import SelectedDate
from datetime import timedelta, date

@login_required
def select_dates(request):
    user = request.user
    selected_dates = SelectedDate.objects.filter(user=user).values_list('selected_date', flat=True)
    selected_dates = [date.strftime('%Y-%m-%d') for date in selected_dates]
    rows_str = request.POST.get('row', '')
    rows = [int(row) for row in rows_str.split(',') if row]
    days = [date(2023, 10, 29) + timedelta(days=i) for i in range(42)]
    people = range(13)

    selected_rows = SelectedDate.objects.filter(user=user).values_list('row', flat=True)
    all_rows = [int(row) for row in selected_rows]

    date_row_dict = {}
    
    if request.method == 'POST':
        form = DateSelectionForm(request.POST)
        if form.is_valid():
            selected_dates_str = form.cleaned_data['selected_dates']
            selected_dates = selected_dates_str.split(',')

            # Clear the user's previous selections
            SelectedDate.objects.filter(user=user).delete() #IMPORTANT IF I WANT TO SAVE PAST SCHEDULES

            # Save the user's new selections
            for day, row in zip(selected_dates, rows):  # Iterate through selected_dates and rows together
                selected_date = SelectedDate(user=user, selected_date=day, row=row)
                selected_date.save()

            return redirect('schedule_view')
    else:
        form = DateSelectionForm(initial={
        'selected_dates': ','.join(selected_dates),
        'row': ','.join(map(str, rows))  # Convert rows to strings and join with commas
        })

    for i in range(len(selected_dates)):
        date_row_dict[selected_dates[i]] = all_rows[i]
    
    selected_dates_all = SelectedDate.objects.values_list('selected_date', flat=True)
    selected_dates_all = [date.strftime('%Y-%m-%d') for date in selected_dates_all]

    selected_rows_all = SelectedDate.objects.values_list('row', flat=True)
    all_rows_all = [int(row) for row in selected_rows_all]

    all_objects = SelectedDate.objects.all()
    date_row_dict_all = {}
    count = 0

    for o in all_objects:
        username = o.user.username

        date_row_dict_all[f"{selected_dates_all[count]},{all_rows_all[count]}"] = username

        count += 1

    return render(request, 'main/select_dates.html', {'form': form, 'days': days, 'people': people, 'selected_dates': selected_dates, 'date_row_dict': date_row_dict, 'user': user, 'date_row_dict_all': date_row_dict_all})

@login_required
def schedule_view(request):
    logged_in = request.user.get_full_name()
    selected_dates = SelectedDate.objects.values_list('selected_date', flat=True)
    selected_dates = [date.strftime('%Y-%m-%d') for date in selected_dates]

    selected_rows = SelectedDate.objects.values_list('row', flat=True)
    all_rows = [int(row) for row in selected_rows]

    days = [date(2023, 10, 29) + timedelta(days=i) for i in range(42)]
    people = range(13)
    date_row_dict = {}
    count = 0

    all_objects = SelectedDate.objects.all()

    for o in all_objects:
        user = o.user
        name = user.get_full_name()

        date_row_dict[f"{selected_dates[count]},{all_rows[count]}"] = name

        count += 1

    return render(request, 'main/schedule_view.html', {'days': days, 'people': people, 'selected_dates': selected_dates, 'all_rows': all_rows, 'date_row_dict': date_row_dict, 'name': name, 'logged_in': logged_in})

@login_required
def users(response):
    all_users = User.objects.all()
    all_usernames = []
    all_names = []
    length = []
    count = 0

    for user in all_users:
        name = user.get_full_name()
        username = user.username

        all_usernames.append(username)
        all_names.append(name)

        length.append(str(count))
        count += 1

    return render(response, 'main/users.html', {"usernames": all_usernames, "names": all_names, "length": length})

def home(response):
    return render(response, "main/home.html", {})

def events_list(request):
    # Retrieve events from the database and pass them to the template
    events = SelectedDate.objects.all()
    return render(request, 'main/events_list.html', {'events': events})