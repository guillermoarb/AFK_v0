import json
import datetime
import math
import pprint

def js_rep_add_activity(name, project):
    activity = {}
    activity["name"] = name
    activity["project"] = project
    activity["items"] = []

    activity_ind = activity_get_idx(name)

    if activity_ind == None:
        report_dict["activities"].append(activity)

def json_rep_add_item(time, log, date, activity_name):
    item = {}
    item["time"] = time
    item["log"] = log
    item["date"] = date

    activity_ind = activity_get_idx(activity_name)
    
    #If activity exist
    if activity_ind != None:

        item_idx = item_get_idx(activity_ind, log)
        #If item don't exist add the item
        if item_idx == None:
            report_dict["activities"][activity_ind]["items"].append(item)
        else: #Update the item
            report_dict["activities"][activity_ind]["items"][item_idx] = item


def activity_get_idx(activity_name):

    incidence = False
    activity_ind = 0

    for activity in report_dict["activities"]:
        if activity["name"] == activity_name:
            incidence = True
            break

        activity_ind = activity_ind + 1

    if incidence == False:
        activity_ind = None 

    return activity_ind


def item_get_idx(activity_idx, item_log):

    item_idx = 0
    incidence = False

    for item in report_dict["activities"][activity_idx]["items"]:
        if item["log"] == item_log:
            incidence = True
            break

        item_idx = item_idx + 1

    if incidence == False:
        item_idx = None


    return item_idx


def report_print_json(report):
    report_file_name = datetime.datetime.now().strftime("%m%d%y") + "_AFK_report.json"

    with open(report_file_name, "w") as file_object:
        file_object.write(json.dumps(report, indent=4, sort_keys=True))

def report_update_week():
    report_dict["week"] = datetime.datetime.now().isocalendar()[1]

def report_update_worked_time():

    total_week_time_seconds = 0
    total_activity_time_seconds = 0

    for activity in report_dict["activities"]:
        for item in activity["items"]:
            time_parts = item["time"].split(":")
            time_seconds = (int(time_parts[0]) * 3600) + (int(time_parts[1]) * 60) + int(time_parts[2])
            #Total week time in seconds
            total_week_time_seconds = total_week_time_seconds + time_seconds
            #Total activity time in seconds
            total_activity_time_seconds = total_activity_time_seconds + time_seconds

        #Report activity total time and then reset it
        activity_time_hours = math.trunc(total_activity_time_seconds / 3600)
        activity_time_minutes = math.trunc((total_activity_time_seconds % 3600) / 60)

        activity["total_time_hr"] = activity_time_hours
        activity["total_time_min"] = activity_time_minutes

        total_activity_time_seconds = 0

    #Report week time
    week_time_hours = math.trunc(total_week_time_seconds / 3600)
    week_time_minutes = math.trunc((total_week_time_seconds % 3600) / 60)

    report_dict["worked_time_hr"] = week_time_hours
    report_dict["worked_time_min"] = week_time_minutes

report_dict = {}

report_dict["week"] = 0
report_dict["worked_time_hr"] = 0
report_dict["worked_time_min"] = 0
report_dict["activities"] = []


js_rep_add_activity("Activity 01","Project 01")
js_rep_add_activity("Activity 03","Project 01")
js_rep_add_activity("Activity 03","Project 01")
json_rep_add_item('01:01:00', "Log 03", "12/34/56", "Activity 01")
json_rep_add_item('01:01:00', "Log 01", "99/99/99", "Activity 01")
json_rep_add_item("01:01:20", "Log 02", "78/90/12", "Activity 01")


js_rep_add_activity("Activity 02","Project 03")
json_rep_add_item("01:01:50", "Log 01", "12/34/56", "Activity 02")
json_rep_add_item("01:56:60", "Log 02", "78/90/52", "Activity 03")

report_update_worked_time()
report_update_week()

#pprint.pprint(report_dict["activities"])
report_print_json(report_dict)



#print( "item index {}".format(item_get_idx(activity_get_idx("Activity 01"), "Log 01")))