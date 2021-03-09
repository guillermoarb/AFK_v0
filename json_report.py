import json
import pprint

def js_rep_add_activity(name, project):
    activity = {}
    activity["name"] = name
    activity["project"] = project
    activity["items"] = []

    activity_ind = activity_exist(name)

    if activity_ind == None:
        report_dict["activities"].append(activity)

def json_rep_add_item(time, log, date, activity_name):
    item = {}
    item["time"] = time
    item["log"] = log
    item["date"] = date



    activity_ind = activity_exist(activity_name)
    
    if activity_ind != None:
        report_dict["activities"][activity_ind]["items"].append(item)


def activity_exist(activity_name):

    incidence = 0
    activity_ind = 0

    for activity in report_dict["activities"]:
        if activity["name"] == activity_name:
            incidence = incidence + 1
            break

        activity_ind = activity_ind + 1

    if incidence == 0:
        activity_ind = None 

    return activity_ind

# with open("Report_Example.json") as json_file:
#     json_data = json.load(json_file)

# #print(json.dumps(json_data, indent = 4))

# print(json_data["activities"][0])

report_dict = {}

report_dict["week"] = 0
report_dict["worked_time"] = 0
report_dict["activities"] = []

act_ind = 0;

js_rep_add_activity("Activity 01","Project 01")
js_rep_add_activity("Activity 03","Project 01")
js_rep_add_activity("Activity 03","Project 01")
json_rep_add_item("12:34:56", "Log 01", "12/34/56", "Activity 01")
json_rep_add_item("78:90:12", "Log 02", "78/90/512", "Activity 01")

act_ind = 1;

js_rep_add_activity("Activity 02","Project 03")
json_rep_add_item("12:34:56", "Log 01", "12/34/56", "Activity 02")
json_rep_add_item("78:90:12", "Log 02", "78/90/512", "Activity 02")

pprint.pprint(report_dict["activities"])

