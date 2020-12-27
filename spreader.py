# TODO: check for maximums (24h, 31 days, weeks have no maximum)

#!/usr/bin/python3

import json
import csv
import sys
from collections import OrderedDict


# Pull out limiting number
def get_limit(args):
    limiting_number = None
    try:
        if "-l" in args:
            limiting_number = args[args.index("l")+1:]
        else:
            limiting_number = None
    except ValueError:
        pass
    return limiting_number


# Fill in the periods in a dictionary
def fill_period(periods, delimiter, lower_delimiter, limit, limit_indicator, args):
    if limit:
        periods[delimiter] = args[args.index(
            delimiter)+2:args.index(limit_indicator)]
        periods[lower_delimiter] = limit
    else:
        periods[delimiter] = args[2:]
    return periods


# Get all periods
def get_all_periods(list_of_delimiters, total_period, week, day, hour, limit_indicator):
    try:
        for item in list_of_delimiters:
            limit = get_limit(item)
            if item.startswith(week):
                fill_period(total_period, week, day,
                            limit, limit_indicator, item)
            elif item.startswith(day):
                fill_period(total_period, day, hour,
                            limit, limit_indicator, item)
            elif item.startswith(hour):
                total_period[hour] = item[2:]
    except IndexError:
        total_period = None
    return total_period


def check_length_of_dict(dict, target):
    return len(list(dict.keys())) > target


# TODO: refactor this
def spreader(periods, all_courses, week_delim, day_delim, hour_delim, SPREADED_JSON_OUTPUT):
    """ Spread the lessons in study periods.

    As params, this function will take in a dictionary with format:
    {'-w': '5', '-d': '4', '-h': '5'}
    the courses store,
    as well as the week, day, hour delimiters.

    By choice, the spreader rounds up minutes.
    For example, if a course lasts 11:20, the calculation will be made
    as if the course lasted 12 minutes.
    This lack of precision is to give some leeway in the
    daily spread of courses.
    """

    courses_copy = all_courses.copy()
    spread_courses = OrderedDict({})
    weeks = 0
    days = 0
    hours = 0
    minutes = 0
    for period in periods:
        if period == week_delim:
            weeks = int(periods[period])
        elif period == day_delim:
            days = int(periods[period])
        elif period == hour_delim:
            hours = int(periods[period])
    for i in range(weeks):
        if check_length_of_dict(courses_copy, 2):
            this_week = "Week {}".format(i+1)
            spread_courses[this_week] = OrderedDict({})
            for j in range(days):
                if check_length_of_dict(courses_copy, 2):
                    this_day = "Day {}".format(j+1)
                    spread_courses[this_week][this_day] = OrderedDict({
                    })
                    for k in range(hours):
                        if check_length_of_dict(courses_copy, 2):
                            this_hour = "Hour {}".format(k+1)
                            spread_courses[this_week][this_day][this_hour] = []
                            minutes += 60
                            if check_length_of_dict(courses_copy, 2):
                                while(minutes > 0):
                                    this_course = (next(iter(courses_copy)))
                                    this_course_time = int(
                                        courses_copy[this_course])
                                    if this_course_time + 1 <= minutes and check_length_of_dict(courses_copy, 2):
                                        courses_copy.popitem(last=False)
                                        minutes -= this_course_time
                                        spread_courses[this_week][this_day][this_hour].append(
                                            [this_course, this_course_time])
                                    elif check_length_of_dict(courses_copy, 2):
                                        courses_copy[this_course] = this_course_time - minutes
                                        this_course = (
                                            next(iter(courses_copy)))
                                        this_course_time = minutes
                                        minutes = 0
                                        spread_courses[this_week][this_day][this_hour].append(
                                            [this_course, this_course_time])
                                    else:
                                        minutes = 0
    export_to_file(spread_courses, json_format=(True, SPREADED_JSON_OUTPUT))


# Export a dictionary to a JSON, CVS and/or TXT file
def export_to_file(data, json_format=(False, "output.json"), csv_format=(False, "output.csv"), txt_format=(False, "output.txt")):
    if isinstance(data, (dict)):
        try:
            if json_format[0]:
                with open(json_format[1], "w") as json_file:
                    json.dump(data, json_file)
            if csv_format[0]:
                with open(csv_format[1], "w") as csv_file:
                    for key in data.keys():
                        csv_file.write("{},{}\n".format(key, data[key]))
            if txt_format[0]:
                with open(txt_format[1], "w") as text_file:
                    text_file.write(str(data))
        except IOError:
            print("I/O error")


def init_files(args):
    if "-i" in args:
        return args[args.index("-i") + 1]


def main(args):
    if init_files(args):
        SOURCE_FILE = init_files(args)
    else:
        SOURCE_FILE = "data.txt"
    JSON_OUTPUT = "{}_output.json".format(SOURCE_FILE)
    CSV_OUTPUT = "{}_output.csv".format(SOURCE_FILE)
    TXT_OUTPUT = "{}_output.txt".format(SOURCE_FILE)
    SPREADED_JSON_OUTPUT = "{}_spreaded_output.json".format(SOURCE_FILE)

    # Fetch data from file
    try:
        with open(SOURCE_FILE) as f_read:
            data = f_read.readlines()
    except IOError:
        print("I/O error")

    week = "-w"
    day = "-d"
    hour = "-h"
    limit_indicator = "-l"
    total_periods = {}
    total_periods = get_all_periods(
        args, total_periods, week, day, hour, limit_indicator)
    courses_store = OrderedDict({})
    total_time = 0

    # TODO: refactor for cleaner and DRY code
    # Populate dictionary with fetched data
    for line in data:
        line = line.strip()
        if "(" in line:
            start = line.index("(")
            stop = line.index(")")
            time = line[start+1:stop]
            try:
                minutes = int(time[:time.index(":")])
            except ValueError:
                minutes = 0
            try:
                seconds = int(time[time.index(":")+1:])
            except ValueError:
                seconds = 0
            minutes = minutes + seconds / 60
            total_time += minutes
            course = line[:start]
            courses_store[course] = round(minutes, 2)

    # Get total times from fetched data and add to store
    hours = str(int(total_time / 60)).zfill(2)
    minutes = str(int(total_time % 60)).zfill(2)
    seconds = str(int((total_time % 1) * 60)).zfill(2)
    courses_store["total time in minutes"] = int(total_time)
    courses_store["total time (hh:mm:ss)"] = "{}:{}:{}".format(
        hours, minutes, seconds)

    if total_periods:
        spreader(total_periods, courses_store, week,
                 day, hour, SPREADED_JSON_OUTPUT)

    # Export to JSON, CSV and TXT
    export_to_file(courses_store, json_format=(
        True, JSON_OUTPUT), csv_format=(True, CSV_OUTPUT), txt_format=(True, TXT_OUTPUT))


if (__name__ == '__main__'):
    main(sys.argv[1:])
