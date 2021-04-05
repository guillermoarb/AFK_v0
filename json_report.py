import json
import datetime
import math
import os.path
import pprint

class Report:
    def __init__(self):

        self.report_file_path = datetime.datetime.now().strftime("%m%d%y") + "_AFK_report.json"
        self.report_file_path = os.path.join("Reports", self.report_file_path)

        self.report_dic = {}

        #Load actual json report
        if os.path.isfile(self.report_file_path):
            with open(self.report_file_path, "r") as json_file:
                self.report_dic = json.loads(json_file.read())
        #Or create a new dictionary for reporting
        else:
            self.report_dic["week"] = 0
            self.report_dic["worked_time_hr"] = 0
            self.report_dic["worked_time_min"] = 0
            self.report_dic["activities"] = []

    def report_add_activity(self, name, project):
        activity = {}
        activity["name"] = name
        activity["project"] = project
        activity["items"] = []

        activity_ind = self.activity_get_idx(name)

        if activity_ind == None:
            self.report_dic["activities"].append(activity)

    def report_add_item(self, time, log, date, activity_name):
        item = {}
        item["time"] = time
        item["log"] = log
        item["date"] = date

        activity_ind = self.activity_get_idx(activity_name)

        #If activity exist
        if activity_ind != None:

            item_idx = self.item_get_idx(activity_ind, log)
            #If item don't exist add the item
            if item_idx == None:
                self.report_dic["activities"][activity_ind]["items"].append(item)
            else: #Update the item
                self.report_dic["activities"][activity_ind]["items"][item_idx] = item

    def report_update_item(self, time, log, date, activity_name):
        item = {}
        item["time"] = time
        item["log"] = log
        item["date"] = date

        activity_ind = self.activity_get_idx(activity_name)

        #If activity exist
        if activity_ind != None:

            item_idx = self.item_get_idx(activity_ind, log)
            #If item don't exist add the item
            if item_idx == None:
                self.report_dic["activities"][activity_ind]["items"].append(item)
            else: #Update the item
                self.report_dic["activities"][activity_ind]["items"][item_idx] = item

    def activity_get_idx(self, activity_name):

        incidence = False
        activity_ind = 0

        for activity in self.report_dic["activities"]:
            if activity["name"] == activity_name:
                incidence = True
                break

            activity_ind = activity_ind + 1

        if incidence == False:
            activity_ind = None 

        return activity_ind


    def item_get_idx(self, activity_idx, item_log):

        item_idx = 0
        incidence = False

        for item in self.report_dic["activities"][activity_idx]["items"]:
            if item["log"] == item_log:
                incidence = True
                break

            item_idx = item_idx + 1

        if incidence == False:
            item_idx = None


        return item_idx


    def report_print_json(self):

        with open(self.report_file_path, "w") as file_object:
            file_object.write(json.dumps(self.report_dic, indent=4, sort_keys=True))

    def report_update_week(self):
        self.report_dic["week"] = datetime.datetime.now().isocalendar()[1]

    def report_update_worked_time(self):

        total_week_time_seconds = 0
        total_activity_time_seconds = 0

        for activity in self.report_dic["activities"]:
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

        self.report_dic["worked_time_hr"] = week_time_hours
        self.report_dic["worked_time_min"] = week_time_minutes

    def report_update_day_info(self):
        pass

""" 

report_dict = {}

report_dict["week"] = 0
report_dict["worked_time_hr"] = 0
report_dict["worked_time_min"] = 0
report_dict["activities"] = []

""" 
"""
report = Report()


report.report_add_activity("Activity 01","Project 01")
report.report_add_activity("Activity 03","Project 01")
report.report_add_activity("Activity 03","Project 01")
report.report_add_item('01:01:00', "Log 03", "12/34/56", "Activity 01")
report.report_add_item('01:01:00', "Log 01", "99/99/99", "Activity 01")
report.report_add_item("01:01:20", "Log 02", "78/90/12", "Activity 01")


report.report_add_activity("Activity 02","Project 03")
report.report_add_item("01:01:50", "Log 01", "12/34/56", "Activity 02")
report.report_add_item("01:56:60", "Log 02", "78/90/52", "Activity 03")

report.report_update_worked_time()
report.report_update_week()

#pprint.pprint(report_dict["activities"])
report.report_print_json()



#print( "item index {}".format(item_get_idx(activity_get_idx("Activity 01"), "Log 01")))

"""