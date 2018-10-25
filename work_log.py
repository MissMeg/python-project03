import csv
import os
import re
from datetime import datetime
from operator import attrgetter


# VARIABLES
# date formatting
date_format = '%Y/%m/%d'

# result strings
single_result_string = '''
Result {} of {}
[E]dit, [D]elete, [R]eturn to main menu
'''

multiple_result_string_next = '''
Result {} of {}
[N]ext, [E]dit, [D]elete, [R]eturn to main menu
'''

multiple_result_string_prev = '''
Result {} of {}
[P]revious, [E]dit, [D]elete, [R]eturn to main menu
'''

multiple_result_string_both = '''
Result {} of {}
[P]revious, [N]ext, [E]dit, [D]elete, [R]eturn to main menu
'''


class Task:
    def __init__(self, task_date, task_title, task_time_spent, task_notes=''):
        self.task_date = task_date
        self.task_title = task_title
        self.task_time_spent = task_time_spent
        self.task_notes = task_notes
        self.task = {
            'date': self.task_date,
            'title': self.task_title,
            'timeSpent': self.task_time_spent,
            'notes': self.task_notes
        }

    def __str__(self):
        return '''\
        \nDate: {}\
        \nTitle: {}\
        \nTime Spent: {}\
        \nNotes: {}
        '''.format(self.task_date,
                   self.task_title,
                   self.task_time_spent,
                   self.task_notes)


class WorkLog:
    def __init__(self):
        self.log = []

    def add_task(self, task):
        self.log.append(task)
        self.sort_list()
        with open('output/tasks.csv', 'a') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=['Date', 'Title', 'Time Spent', 'Notes'])
            writer.writerow({'Date': task.task_date, 'Title': task.task_title, 'Time Spent': task.task_time_spent,
                             'Notes': task.task_notes})

    def remove_task(self, task):
        self.log.remove(task)
        self.sort_list()
        with open('output/tasks.csv', 'w') as output:
            writer = csv.DictWriter(output, fieldnames=['Date', 'Title', 'Time Spent', 'Notes'])
            writer.writeheader()
            for task in self.log:
                writer.writerow({'Date': task.task_date, 'Title': task.task_title, 'Time Spent': task.task_time_spent,
                                 'Notes': task.task_notes})

    def sort_list(self):
        self.log.sort(key=attrgetter('task_date'), reverse=True)

    def show_list(self):
        count = 1
        for task in self.log:
            print(count, task)
            count += 1


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def create_task():
    while True:
        clear()
        new_task_date = input('(Please use YYYY/MM/DD) Date of the task > ')
        # make sure the user enters a valid date
        try:
            new_task_date = datetime.strptime(new_task_date, date_format)
        except ValueError:
            input('That\'s not a valid date. Please press enter to try again.')
        else:
            while True:
                clear()
                new_title = input('Title of the task > ')
                # make sure the user enters a title
                try:
                    if not new_title:
                        raise ValueError('Please input a title')
                except ValueError as error:
                    print(error)
                else:
                    clear()
                    # Start another while loop so if a mistake is made
                    # so the user doesn't get sent back to the main menu
                    while True:
                        new_time_spent = input('Time Spent (rounded minutes) > ')
                        # make sure the user enters time_spent with numbers
                        try:
                            int(new_time_spent)
                        except ValueError:
                            input('Please enter the time in minutes using numbers. Press enter to '
                                  'try again')
                        else:
                            clear()
                            new_notes = input('Notes (Optional) > ')
                            if not new_notes:
                                log.add_task(Task(new_task_date, new_title, new_time_spent))
                            else:
                                log.add_task(Task(new_task_date, new_title, new_time_spent, new_notes))
                            input('The task has been added! Press Enter to return to the main menu')
                            # break out of all loops to go back to the main menu
                            break
                    break
            break


def edit_task(task):
    while True:
        clear()
        print('Current Date:', task.task_date)
        new_task_date = input('(Please use YYYY/MM/DD) Change date of the task or press Enter to keep the same > ')
        if new_task_date == '':
            new_task_date = task.task_date
        else:
            # make sure the user enters a valid date
            try:
                new_task_date = datetime.strptime(new_task_date, date_format)
            except ValueError:
                input('That\'s not a valid date. Please press enter to try again.')
        while True:
            clear()
            print('Current Title:', task.task_title)
            new_title = input('Change the title of the task or press Enter to keep the same > ')
            if new_title == '':
                new_title = task.task_title
            # make sure the user enters a title
            try:
                if not new_title:
                    raise ValueError('Please input a title')
            except ValueError as error:
                print(error)
            else:
                clear()
                # Start another while loop so if a mistake is made
                # so the user doesn't get sent back to the main menu
                while True:
                    print('Current Time Spent:', task.task_time_spent)
                    new_time_spent = input('Change time Spent (rounded minutes) or press Enter to keep the same > ')
                    if new_time_spent == '':
                        new_time_spent = task.task_time_spent
                    # make sure the user enters time_spent with numbers
                    try:
                        int(new_time_spent)
                    except ValueError:
                        input('Please enter the time in minutes using numbers. Press enter to '
                              'try again')
                    else:
                        clear()
                        print('Current Notes:', task.task_notes)
                        new_notes = input('Change notes or press Enter to keep the same > ')
                        if not new_notes:
                            log.add_task(Task(new_task_date, new_title, new_time_spent))
                        else:
                            log.add_task(Task(new_task_date, new_title, new_time_spent, new_notes))
                        input('The task has been added! Press Enter to return to the main menu')
                        # break out of all loops to go back to the main menu
                        break
                break
        break


def matches(task_matches):
    # print first item in list
    match_to_print = 0
    print(task_matches[match_to_print])

    # setup for pagination
    current_page = 1
    end_page = len(task_matches)
    request = ''

    # print correct result string based off of result length
    if len(task_matches) == 1:
        request = input(single_result_string.format(current_page, end_page)).upper()
    elif len(task_matches) != 1:
        request = input(multiple_result_string_next.format(current_page,
                                                           end_page)).upper()

    # loop through to change pages, as well as, to edit or delete tasks + return to menu
    while True:
        # next page
        if request == 'N':
            current_page += 1
            match_to_print += 1
            next_match_to_print = task_matches[match_to_print]
            print(next_match_to_print)
            if current_page == end_page:
                request = input(multiple_result_string_prev.format(
                    current_page,
                    end_page)).upper()
            else:
                request = input(multiple_result_string_both.format(
                    current_page,
                    end_page)).upper()

        # previous page
        elif request == 'P':
            current_page -= 1
            match_to_print -= 1
            next_match_to_print = task_matches[match_to_print]
            print(next_match_to_print)
            if current_page == 1:
                request = input(
                    multiple_result_string_next.format(current_page,
                                                       end_page)).upper()
            else:
                request = input(
                    multiple_result_string_both.format(current_page,
                                                       end_page)).upper()

        # call edit page
        elif request == 'E':
            log.remove_task(task_matches[match_to_print])
            print('Loading the editor')
            edit_task(task_matches[match_to_print])
            break

        # call delete page
        elif request == 'D':
            log.remove_task(task_matches[match_to_print])
            input('Task has been deleted. Press enter to return to the menu.')
            break

        # return to main menu
        elif request == 'R':
            break


if __name__ == "__main__":
    os.makedirs(os.path.dirname('output/tasks.csv'), exist_ok=True)
    with open('output/tasks.csv', 'a') as tasksfile:
        writer = csv.DictWriter(tasksfile, fieldnames=['Date', 'Title', 'Time Spent', 'Notes'])
        writer.writeheader()

    # Start the log
    log = WorkLog()

    while True:
        clear()
        # Print Initial Menu
        first_response = input('''\
            \nWork Log Menu\
            \n1) Add New Task\
            \n2) Search for a Task\
            \n3) View All Entries\
            \n4) Exit\
            \n*Type the number and then push Enter* > \
        ''')

        # Make sure the response is a number - any other numbers will just put them back into the main menu
        try:
            int(first_response)
        except ValueError:
            input('Please choose one of the menu options by typing the matching number and hitting enter. Press enter '
                  'to continue.')
        else:
            # Add item to the work log
            if first_response == '1':
                create_task()

            # Search through existing entries
            elif first_response == '2':
                while True:
                    if len(log.log) < 1:
                        input('There aren\'t any tasks in your work log yet. Try adding a few!')
                        break
                    else:
                        clear()
                        search_by = input('''\
                            \nSearch Entries\
                            \n1) Find by Date\
                            \n2) Find by Time Spent\
                            \n3) Find by Exact Search\
                            \n4) Find by Pattern\
                            \n5) Find by Date Range\
                            \n6) Return to Main Menu\
                            \n*Type the number and then push Enter* >\
                        ''')
                        try:
                            int(search_by)
                        except ValueError:
                            input('Please choose one of the menu options by typing the matching number and hitting '
                                  'enter. Press enter to continue.')
                        else:
                            # search by date
                            if search_by == '1':
                                clear()
                                find_date = input('Enter the date using YYYY/MM/DD > ')
                                try:
                                    find_date = datetime.strptime(find_date, date_format)
                                except ValueError:
                                    input("That's not a valid date. Please press enter to try again.")
                                else:
                                    date_matches = [task for task in log.log if task.task_date == find_date]
                                    if len(date_matches) < 1:
                                        input('No matches. Please try again.')
                                    else:
                                        matches(date_matches)

                            # search by time spent
                            elif search_by == '2':
                                clear()
                                search_time = input('Enter the time spent in minutes: ')
                                try:
                                    search_time = int(search_time)
                                except ValueError:
                                    input("Please enter using numbers only. Press enter to try again.")
                                else:
                                    search_time = str(search_time)
                                    time_matches = [task for task in log.log if task.task_time_spent == search_time]
                                    if len(time_matches) < 1:
                                        input('No matches. Please try again.')
                                    else:
                                        matches(time_matches)

                            # search by exact phrase
                            elif search_by == '3':
                                while True:
                                    clear()
                                    search_exact = input('Enter the phrase to search for: ')
                                    try:
                                        if not search_exact:
                                            raise ValueError('Please input a phrase. Press enter to try again.')
                                    except ValueError as err:
                                        input(err)
                                    else:
                                        exact_matches = []
                                        for task in log.log:
                                            if search_exact in task.task_title or search_exact in task.task_notes:
                                                exact_matches.append(task)
                                        if len(exact_matches) < 1:
                                            input('No matches. Please try again.')
                                        else:
                                            matches(exact_matches)
                                            break

                            # search by regex pattern
                            elif search_by == '4':
                                clear()
                                search_pattern = input('Enter the regex pattern to search for: ')
                                try:
                                    re.compile(search_pattern)
                                except re.error:
                                    input('Please enter a valid Regex pattern. Press enter to try again.')
                                else:
                                    pattern_matches = []
                                    for task in log.log:
                                        if re.search(search_pattern, task.task_title) \
                                                or re.search(search_pattern, task.task_time_spent) \
                                                or re.search(search_pattern, task.task_date) \
                                                or re.search(search_pattern, task.task_notes):
                                            pattern_matches.append(task)
                                    if len(pattern_matches) < 1:
                                        input('No matches. Please try again.')
                                    else:
                                        matches(pattern_matches)

                            # search by date range
                            elif search_by == '5':
                                clear()
                                print('Searching by Date Range')
                                first_date = input('(Enter the date using YYYY/MM/DD) Start Date > ')
                                try:
                                    first_date = datetime.strptime(first_date, date_format)
                                except ValueError:
                                    input("That's not a valid date. Please press enter to try again.")
                                else:
                                    second_date = input('(Enter the date using YYYY/MM/DD) End Date > ')
                                    try:
                                        second_date = datetime.strptime(second_date, date_format)
                                    except ValueError:
                                        input("That's not a valid date. Please press enter to try again.")
                                    else:
                                        date_matches = []
                                        for task in log.log:
                                            if first_date <= task.task_date <= second_date:
                                                date_matches.append(task)
                                        if len(date_matches) < 1:
                                            input('No matches. Please try again.')
                                        else:
                                            matches(date_matches)

                            # return to main menu
                            elif search_by == '6':
                                break

            # Extra: Show all current entries
            elif first_response == '3':
                if len(log.log) < 1:
                    input('There aren\'t any tasks in your work log yet. Try adding a few!')
                else:
                    clear()
                    log.show_list()
                    input('Press enter to return to the main menu.')

            # Quit program
            elif first_response == '4':
                clear()
                print('Goodbye!')
                break
