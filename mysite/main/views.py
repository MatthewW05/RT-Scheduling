from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import DateSelectionForm, ScheduleInitiationForm, CreateGroups, EditProfileForm
from .models import SelectedDate, InitiateSchedule, SelectionGroups
from datetime import timedelta, datetime
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from functions import *
import calendar
from okta_oauth2.decorators import okta_login_required
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

@login_required
@okta_login_required
def home(request):
    try:
        rewrite_super(request.user)
    except:
        pass

    name = request.user.get_full_name()
    name1 = request.user.first_name
    name2 = request.user.last_name

    if empty_name(name1, name2):
        return redirect("/profile/edit/")

    return render(request, "main/home.html", {'first': get_first_schedule(), 'name': name,})

@login_required
@okta_login_required
def select_dates(request, check_error=-1):
    try:
        rewrite_super(request.user)
    except:
        pass

    name1 = request.user.first_name
    name2 = request.user.last_name

    if empty_name(name1, name2):
        return redirect("/profile/edit/")

    # Check if there are any schedules initialized
    if len(InitiateSchedule.objects.values_list('user_start_date', flat=True)) != 0:
        error_message = ""


        if check_error == "taken": # Check if the 'taken' parameter is set, indicating that the user attempted to select already taken dates
            error_message = "One or more of the dates you selected have been taken"
        elif check_error == "over": # Check if the 'over' parameter is set, indicating that the user attempted to select too many dates
            error_message = "You may only select 20 dates per schedule"

        user = request.user

        # Retrieve the last user start date, adjust it, and calculate the target date range for selection
        selection_start = InitiateSchedule.objects.values_list('user_start_date', flat=True)
        selection_start = selection_start[len(selection_start)-1]
        selection_start = datetime.combine(selection_start, datetime.min.time()) + timedelta(hours=7.5)

        now = datetime.now()

        try:
            group = SelectionGroups.objects.filter(user=user)[0].group
        except:
            return render(request, 'main/message.html', {'message': "You have not been added to a group!"})

        target = (selection_start + timedelta(days=(3*group)), selection_start + timedelta(days=(3*group+3)))
        can_select = False

        # Check if the current time is within the allowed selection period
        if target[0] <= now <= target[1]:
            can_select = True

        # Retrieve selected dates and rows for the current user
        selected_dates = SelectedDate.objects.filter(user=user).values_list('selected_date', flat=True)
        selected_dates = [date.strftime('%Y-%m-%d') for date in selected_dates]
        rows_str = request.POST.get('row', '')
        rows = [int(row) for row in rows_str.split(',') if row]

        # Retrieve the last schedule start date
        start = InitiateSchedule.objects.values_list('schedule_start_date', flat=True)
        start = start[len(start)-1]

        # Generate a list of days for the calendar view
        days = [start + timedelta(days=i) for i in range(42)]
        people = range(34)
        bottom_border_rows = [1, 5, 12, 13, 14, 15, 21, 25]
        top_border_rows = [2, 6, 13, 14, 15, 16, 22, 26]

        # Retrieve selected rows for the current user
        selected_rows = SelectedDate.objects.filter(user=user).values_list('row', flat=True)
        all_rows = [int(row) for row in selected_rows]

        date_row_dict = {}

        if request.method == 'POST':
            form = DateSelectionForm(request.POST)
            if form.is_valid():
                selected_dates_str = form.cleaned_data['selected_dates']
                selected_dates = selected_dates_str.split(',')

                # Clear the user's previous selections
                check_to_delete_days = SelectedDate.objects.filter(user=user)

                for o in check_to_delete_days:
                    if start <= o.selected_date <= start + timedelta(days=42):
                        o.delete()

                already_selected = False
                too_many = False

                if len(selected_dates) > 20:
                        too_many = True

                # Save the user's new selections
                logger.info(f'[{datetime.now()}] --> [{user.get_full_name()}] submitted the dates: {selected_dates} in the rows: {rows}')
                for day, row in zip(selected_dates[:20], rows[:20]):  # Iterate through selected_dates and rows together
                    if SelectedDate.objects.filter(selected_date=day).filter(row=row):
                        already_selected = True
                    else:
                        selected_date = SelectedDate(user=user, selected_date=day, row=row)
                        selected_date.save()

                if not already_selected and not too_many:
                    return redirect('schedule_view')
                elif already_selected:
                    return redirect('/select_dates/taken')
                else:
                    return redirect('/select_dates/over')
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

        sidebar_info = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}

        unsorted_users = []

        for o in User.objects.all():
            unsorted_users.append(o)

        # Populate sidebar information with user groups
        for o in SelectionGroups.objects.filter():
            sidebar_info[o.group+1].append(o.user.get_username())
            unsorted_users.remove(o.user)

        sidebar_info["unsorted"] = unsorted_users

        context = {
            'form': form,
            'days': days,
            'people': people,
            'selected_dates': selected_dates,
            'date_row_dict': date_row_dict,
            'user': user,
            'date_row_dict_all': date_row_dict_all,
            'sidebar_info': sidebar_info,
            'can_select': can_select,
            'start': target[0],
            'end': target[1],
            'first': get_first_schedule(),
            'error_message': error_message,
            'bottom_border_rows': bottom_border_rows,
            'top_border_rows': top_border_rows,
        }

        return render(request, 'main/select_dates.html', context)
    else:
        # Render a message page if no schedules have been initialized
        return render(request, 'main/message.html', {'message': "No Schedules have been initialized"})

@login_required
@okta_login_required
def schedule_view(request, start=-1):
    try:
        rewrite_super(request.user)
    except:
        pass

    name1 = request.user.first_name
    name2 = request.user.last_name

    if empty_name(name1, name2):
        return redirect("/profile/edit/")

    # Check if there are any schedules initialized
    if len(InitiateSchedule.objects.values_list('user_start_date', flat=True)) != 0:
        sidebar_for_old = False

        # Check if the 'start' parameter is set, indicating an older schedule is being viewed
        if start != -1:
            start = datetime.strptime(start, "%Y-%m-%d").date()

            sidebar_for_old = True
        else:
            start = get_first_schedule_date()

        try:
            logged_in = request.user.get_full_name().split(" ")
            logged_in = logged_in[0][0]+logged_in[1][:4]
        except:
            logged_in = request.user.get_username()[:5]

        selected_dates = SelectedDate.objects.values_list('selected_date', flat=True)
        selected_dates = [date.strftime('%Y-%m-%d') for date in selected_dates]

        selected_rows = SelectedDate.objects.values_list('row', flat=True)
        all_rows = [int(row) for row in selected_rows]

        # Generate a list of days for the calendar view
        days = [start + timedelta(days=i) for i in range(42)]
        people = range(34)
        bottom_border_rows = [1, 5, 12, 13, 14, 15, 21, 25]
        top_border_rows = [2, 6, 13, 14, 15, 16, 22, 26]
        date_row_dict = {}
        count = 0

        all_objects = SelectedDate.objects.all()
        name = ''

        # Populate a dictionary with selected dates and corresponding rows for display
        for o in all_objects:
            user = o.user
            try:
                name = user.get_full_name().split(" ")
                name = name[0][0]+name[1][:4]
            except:
                name = user.get_username()[:5]

            date_row_dict[f"{selected_dates[count]},{all_rows[count]}"] = name

            count += 1

        user = request.user

        sidebar_info = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}

        unsorted_users = []

        for o in User.objects.all():
            unsorted_users.append(o)

        # Populate sidebar information with user groups
        for o in SelectionGroups.objects.filter():
            sidebar_info[o.group+1].append(o.user.get_username())
            unsorted_users.remove(o.user)

        sidebar_info["unsorted"] = unsorted_users

        schedule = {}
        gaps = []

        for day in days:
            if f"{day.year}-{day.month}-1" not in schedule:
                full = calendar.monthrange(day.year, day.month)[1]+((calendar.monthrange(day.year, day.month)[0]+1)%7)
                gap = 6-(full//7+bool(full%7))

                gaps.append(200*gap)

                for sub_day in range(calendar.monthrange(day.year, day.month)[1]):
                    schedule[f"{day.year}-{day.month}-{sub_day+1}"] = ""

        for check in date_row_dict:
            total = check.split(",")
            date = total[0].replace("-0", "-")

            if date_row_dict[check] == name and date in schedule:
                if 0 <= int(total[1]) <= 1 or 20 <= int(total[1]) <= 21:
                    schedule[date] = "ICU CORE,"
                elif 2 <= int(total[1]) <= 5 or 22 <= int(total[1]) <= 25:
                    schedule[date] = "CASEROOM,"
                elif 6 <= int(total[1]) <= 12 or 26 <= int(total[1]):
                    schedule[date] = "ROTATING,"
                elif int(total[1]) == 13:
                    schedule[date] = "MEDICINE,"
                elif int(total[1]) == 14:
                    schedule[date] = "OR C/Section,"
                elif int(total[1]) == 15:
                    schedule[date] = "OR RT,"
                elif int(total[1]) == 16:
                    schedule[date] = "BRIDGEPOINT,"

                if int(total[1]) < 17:
                    schedule[date] += "DAYS"
                else:
                    schedule[date] += "NIGHTS"

        context = {
            'days': days,
            'people': people,
            'selected_dates': selected_dates,
            'all_rows': all_rows,
            'date_row_dict': date_row_dict,
            'name': name,
            'logged_in': logged_in,
            'user': user,
            'sidebar_info': sidebar_info,
            'sidebar_for_old': sidebar_for_old,
            'schedules': get_schedules(),
            'first': get_first_schedule(),
            'bottom_border_rows': bottom_border_rows,
            'top_border_rows': top_border_rows,
            'schedule': schedule,
            'gaps': gaps,
        }

        return render(request, 'main/schedule_view.html', context)
    else:
        return render(request, 'main/message.html', {'message': "No Schedules have been initialized"})

@login_required
@okta_login_required
def admin_select_dates(request, user_n):
    try:
        rewrite_super(request.user)
    except:
        pass

    name1 = request.user.first_name
    name2 = request.user.last_name

    if empty_name(name1, name2):
        return redirect("/profile/edit/")

    logged_in = request.user

    if logged_in.is_superuser:

        user_exists = False
        can_select = True

        # Check if the specified user exists
        for o in User.objects.all():
            if o.get_username() == user_n:
                user = o
                user_exists = True

        # Raise an error if the specified user does not exist
        if not user_exists:
            raise LookupError('User does not exist')

        # Retrieve selected dates for the specified user
        selected_dates = SelectedDate.objects.filter(user=user).values_list('selected_date', flat=True)
        selected_dates = [date.strftime('%Y-%m-%d') for date in selected_dates]

        # Retrieve rows for the specified user
        rows_str = request.POST.get('row', '')
        rows = [int(row) for row in rows_str.split(',') if row]

        # Retrieve the last schedule start date
        start = InitiateSchedule.objects.values_list('schedule_start_date', flat=True)
        start = start[len(start)-1]

        # Generate a list of days for the calendar view
        days = [start + timedelta(days=i) for i in range(42)]
        people = range(35)

        # Used to format the schedule
        bottom_border_rows = [1, 5, 12, 13, 14, 15, 21, 25]
        top_border_rows = [2, 6, 13, 14, 15, 16, 22, 26]

        # Retrieve selected rows for the specified user
        selected_rows = SelectedDate.objects.filter(user=user).values_list('row', flat=True)
        all_rows = [int(row) for row in selected_rows]

        date_row_dict = {}

        if request.method == 'POST':
            form = DateSelectionForm(request.POST)
            if form.is_valid():
                selected_dates_str = form.cleaned_data['selected_dates']
                selected_dates = selected_dates_str.split(',')

                # Clear the user's previous selections
                check_to_delete_days = SelectedDate.objects.filter(user=user)

                for o in check_to_delete_days:
                    if start <= o.selected_date <= start + timedelta(days=42):
                        o.delete()

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

        # Populate a dictionary with all selected dates and corresponding rows for display
        for o in all_objects:
            username = o.user.username

            date_row_dict_all[f"{selected_dates_all[count]},{all_rows_all[count]}"] = username

            count += 1

        sidebar_info = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}

        unsorted_users = []

        for o in User.objects.all():
            unsorted_users.append(o)

        # Populate sidebar information with user groups
        for o in SelectionGroups.objects.filter():
            sidebar_info[o.group+1].append(o.user.get_username())
            unsorted_users.remove(o.user)

        sidebar_info["unsorted"] = unsorted_users

        context = {
            'form': form,
            'days': days,
            'people': people,
            'selected_dates': selected_dates,
            'date_row_dict': date_row_dict,
            'user': user,
            'date_row_dict_all': date_row_dict_all,
            'sidebar_info': sidebar_info,
            'can_select': can_select,
            'logged_in': logged_in,
            'first': get_first_schedule(),
            'bottom_border_rows': bottom_border_rows,
            'top_border_rows': top_border_rows,
        }

        return render(request, 'main/select_dates.html', context)

@login_required
@okta_login_required
def initialize_schedule(request):
    try:
        rewrite_super(request.user)
    except:
        pass

    name1 = request.user.first_name
    name2 = request.user.last_name

    if empty_name(name1, name2):
        return redirect("/profile/edit/")

    user = request.user

    if user.is_superuser:

        if request.method == "POST":
            form = ScheduleInitiationForm(request.POST)

            if form.is_valid():
                # Retrieve user_start_date and schedule_start_date from the form's cleaned data
                user_start_date = form.cleaned_data['user_start_date']
                schedule_start_date = form.cleaned_data['schedule_start_date']

                # Create an instance of InitiateSchedule and save it to the database
                initialize = InitiateSchedule(user_start_date=user_start_date, schedule_start_date=schedule_start_date)
                initialize.save()

            return redirect('schedule_view')
        else:
            form = ScheduleInitiationForm()
            return render(request, "main/initialize_schedule.html", {"form": form, 'first': get_first_schedule(),})

@login_required
@okta_login_required
def create_groups(request):
    try:
        rewrite_super(request.user)
    except:
        pass

    name1 = request.user.first_name
    name2 = request.user.last_name

    if empty_name(name1, name2):
        return redirect("/profile/edit/")

    user = request.user

    if user.is_superuser:

        # Initialize lists and dictionaries to store information about users and previous selections
        all_users = []
        all_users_names = []
        user_with_names = {}
        user_with_usernames = {}

        # Retrieve all users from the User model
        for o in User.objects.filter():
            if o.get_username() != "X":
                all_users.append(o)
                all_users_names.append(o.get_full_name())
                user_with_names[o.get_full_name()] = o
                user_with_usernames[o.get_username()] = o

        # Initialize lists to store information about previously selected users and groups
        prev_selected_dict = {}
        prev_selected_users = []
        prev_selected_users_names = []
        prev_selected_groups = []

        # Retrieve information about previously selected users and groups from SelectionGroups model
        for o in SelectionGroups.objects.filter():
            prev_selected_users.append(o.user)
            prev_selected_users_names.append(o.user.get_full_name())
            prev_selected_groups.append(o.group)
            prev_selected_dict[o.user] = o.group

        # Calculate the number of users and create a range for the number of users
        num_of_users = len(all_users)
        num_of_users_list = range(num_of_users)

        context = {
            'all_users': all_users,
            'all_users_names': all_users_names,
            'prev_selected_users': prev_selected_users,
            'prev_selected_users_names': prev_selected_users_names,
            'prev_selected_groups': prev_selected_groups,
            'columns': num_of_users+1,
            'num_of_users': num_of_users_list,
            'user_with_names': user_with_names,
            'prev_selected_dict': prev_selected_dict,
            'first': get_first_schedule(),
        }

        if request.method == 'POST':
            form = CreateGroups(request.POST)
            if form.is_valid():
                # Retrieve selected groups and users from the form's cleaned data
                selected_groups_str = form.cleaned_data['selected_column']
                selected_groups = selected_groups_str.split(',')

                selected_users_str = form.cleaned_data['selected_row']
                selected_users = selected_users_str.split(',')

                # Clear the user's previous selections
                SelectionGroups.objects.filter().delete() #IMPORTANT IF I WANT TO SAVE PAST SCHEDULES

                # Save the user's new selections
                for col, row in zip(selected_groups, selected_users):  # Iterate through selected_dates and rows together
                    selected_group = SelectionGroups(user=user_with_usernames[row], group=int(col))
                    selected_group.save()

                return redirect('initialize_schedule')
        else:
            form = CreateGroups(initial={
            'selected_row': ','.join(map(str, prev_selected_users)),
            'selected_column': ','.join(map(str, prev_selected_groups))
            })

        return render(request, "main/create_groups.html", context)

@login_required
@okta_login_required
def master(request, start=-1):
    try:
        rewrite_super(request.user)
    except:
        pass

    name1 = request.user.first_name
    name2 = request.user.last_name

    if empty_name(name1, name2):
        return redirect("/profile/edit/")

    user = request.user

    if user.is_superuser:
        if len(InitiateSchedule.objects.values_list('user_start_date', flat=True)) != 0:
            if start != -1:
                start = datetime.strptime(start, "%Y-%m-%d").date()
            else:
                start = get_first_schedule_date()

            user_date_dict = {}
            user_row_dict = {}
            all_schedule_info = SelectedDate.objects.filter()
            days = [start + timedelta(days=i) for i in range(42)]

            for item in all_schedule_info:
                if days[0] <= item.selected_date <= days[-1]:
                    if item.user.get_username() != "X":
                        try:
                            name = item.user.get_full_name().split(" ")[0]
                            display = item.user.get_full_name().split(" ")
                            display = f"{display[0][0]}{display[1][:4]}"
                        except:
                            name = item.user.get_username()
                            display = name[:5]

                        if (name, display) in user_date_dict:
                            user_date_dict[(name, display)].append(item.selected_date)
                            user_row_dict[(name, display)].append(item.row)
                        else:
                            user_date_dict[(name, display)] = [item.selected_date]
                            user_row_dict[(name, display)] = [item.row]

            sidebar_info = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}

            unsorted_users = []

            for o in User.objects.all():
                unsorted_users.append(o)

            # Populate sidebar information with user groups
            for o in SelectionGroups.objects.filter():
                sidebar_info[o.group+1].append(o.user.get_username())
                unsorted_users.remove(o.user)

            sidebar_info["unsorted"] = unsorted_users

            context = {
                "user_date_dict": user_date_dict,
                "user_row_dict": user_row_dict,
                "sidebar_info": sidebar_info,
                "days": days,
                'schedules': get_schedules(),
                'first': get_first_schedule(),
            }

            return render(request, "main/master.html", context)



@login_required
@okta_login_required
def view_profile(request):
    try:
        rewrite_super(request.user)
    except:
        pass

    name1 = request.user.first_name
    name2 = request.user.last_name

    if empty_name(name1, name2):
        return redirect("/profile/edit/")

    return render(request, "main/view_profile.html", {'user': request.user, 'first': get_first_schedule(),})

@login_required
@okta_login_required
def edit_profile(request):
    try:
        rewrite_super(request.user)
    except:
        pass

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/profile')
    else:
        form = EditProfileForm(instance=request.user)
        return render(request, 'main/edit_profile.html', {'form': form, 'first': get_first_schedule(),})

@login_required
@okta_login_required
def change_password(request):
    try:
        rewrite_super(request.user)
    except:
        pass

    name1 = request.user.first_name
    name2 = request.user.last_name

    if empty_name(name1, name2):
        return redirect("/profile/edit/")

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password_change_success')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'main/change_password.html', {'form': form, 'first': get_first_schedule(),})

@login_required
@okta_login_required
def password_change_success(request):
    try:
        rewrite_super(request.user)
    except:
        pass

    return render(request, 'main/password_change_success.html', {'first': get_first_schedule(),})

@login_required
@okta_login_required
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

@login_required
@okta_login_required
def events_list(request):
    try:
        rewrite_super(request.user)
    except:
        pass

    # Retrieve events from the database and pass them to the template
    events = SelectedDate.objects.all()
    return render(request, 'main/events_list.html', {'events': events})