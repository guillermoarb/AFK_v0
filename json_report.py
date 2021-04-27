import json
import datetime
import math
import os.path
import pprint
import os
from tabulate import tabulate

class Report:
    def __init__(self):
        #Main dictionary for report
        self.report_dic = {}

        self.today = datetime.datetime.now()
        self.report_update_week()
        
        self.json_rep_file_path = "W" + str(self.week) + "_Report.json"
        self.json_rep_file_path = os.path.join("Reports", self.json_rep_file_path)
        self.md_rep_file_path = "W" + str(self.week) + "_Report.md"
        self.md_rep_file_path = os.path.join("Reports", self.md_rep_file_path)

        #Load actual json report
        if os.path.isfile(self.json_rep_file_path):
            with open(self.json_rep_file_path, "r") as json_file:
                self.report_dic = json.loads(json_file.read())
        #Or create a new dictionary for reporting
        else:
            self.report_dic["week_number"] = 0
            self.report_dic["worked_time_hr"] = 0
            self.report_dic["worked_time_min"] = 0
            self.report_dic["activities"] = []
            self.report_dic["days"] = []

    def report_update_day(self, time_counter):        
        day = {}
        day["date"] = self.today.strftime("%m%d%y")
        day["name"] = self.today.strftime("%A")

        seconds = self.report_counter_to_sec(time_counter)
        day["worked_time_hr"], day["worked_time_min"] = self.report_sec_to_hr_min(seconds)

        day_idx = self.day_get_idx(day["name"])
        #If item don't exist add the item
        if day_idx == None:
            self.report_dic["days"].append(day)
        else: #Update the item
            self.report_dic["days"][day_idx] = day

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

    def day_get_idx(self, day_name):

        incidence = False
        day_idx = 0

        for day in self.report_dic["days"]:
            if day["name"] == day_name:
                incidence = True
                break

            day_idx = day_idx + 1

        if incidence == False:
            day_idx = None 

        return day_idx


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

        with open(self.json_rep_file_path, "w") as file_object:
            file_object.write(json.dumps(self.report_dic, indent=4, sort_keys=True))

    def report_update_week(self):
        self.week = self.today.isocalendar()[1]
        self.report_dic["week_number"] = self.week

    def report_update_worked_time(self):

        total_week_time_seconds = 0
        total_activity_time_seconds = 0

        for activity in self.report_dic["activities"]:
            for item in activity["items"]:
                time_seconds = self.report_counter_to_sec(item["time"])
                #Total week time in seconds
                total_week_time_seconds = total_week_time_seconds + time_seconds
                #Total activity time in seconds
                total_activity_time_seconds = total_activity_time_seconds + time_seconds

            #Report activity total time and then reset it
            activity_time_hours, activity_time_minutes = self.report_sec_to_hr_min(total_activity_time_seconds)

            activity["total_time_hr"] = activity_time_hours
            activity["total_time_min"] = activity_time_minutes

            total_activity_time_seconds = 0

        #Report week time
        week_time_hours = math.trunc(total_week_time_seconds / 3600)
        week_time_minutes = math.trunc((total_week_time_seconds % 3600) / 60)

        self.report_dic["worked_time_hr"] = week_time_hours
        self.report_dic["worked_time_min"] = week_time_minutes

    def report_counter_to_sec(self, counter):
        time_parts = counter.split(":")
        time_seconds = (int(time_parts[0]) * 3600) + (int(time_parts[1]) * 60) + int(time_parts[2])

        return time_seconds
    
    def report_sec_to_hr_min(self, seconds):
        hours = math.trunc(seconds / 3600)
        minutes = math.trunc((seconds % 3600) / 60)

        return hours, minutes

    def report_get_task_time(self, activity, task):

        activity_time = datetime.time()
        
        activity_idx = self.activity_get_idx(activity)

        if activity_idx != None:
            item_idx = self.item_get_idx(activity_idx, task)

            if item_idx != None:
                act_time_split =  self.report_dic["activities"][activity_idx]["items"][item_idx]["time"].split(":")
                activity_time = datetime.time(int(act_time_split[0]), int(act_time_split[1]), int(act_time_split[2]))
        
            else:
                activity_time = datetime.time(0, 0, 0)
        else:
            activity_time = datetime.time(0, 0, 0)


        return activity_time
            

    def json_report_open(self):
        os.system(f"code {self.json_rep_file_path}")


    def report_get_today_time(self):
        today_time = datetime.time()
        today_hr = 0
        today_min = 0
        day_name = self.today.strftime("%A")
        day_idx = self.day_get_idx(day_name)

        #If item don't exist add the item
        if day_idx != None:
            today_hr = self.report_dic["days"][day_idx]["worked_time_hr"]
            today_min = self.report_dic["days"][day_idx]["worked_time_min"]

        else:
            today_hr = 0
            today_min = 0
             
        today_time = datetime.time(today_hr, today_min, 0)

        return today_time

    def activity_get_all(self):
        activities_array = []
        for activity in self.report_dic["activities"]:
            activities_array.append(activity["name"])

        return activities_array

    def task_get_all(self, activity):
        tasks_array = []

        activity_idx = self.activity_get_idx(activity)

        for task in self.report_dic["activities"][activity_idx]["items"]:
            tasks_array.append(task["log"])

        return tasks_array

    def report_generate_report(self):
        #Update the information before printing
        self.report_update_worked_time()
        #Get activity logs and time
        rows = []
        txt_dictionary = {}
        #Add firs row as header
        txt_dictionary["project"] = "Project"
        txt_dictionary["name"] = "Activity"
        txt_dictionary["time"] = "Time"
        txt_dictionary["logs"] = "Logs"

        rows.append(txt_dictionary)

        for idx, activity in enumerate(self.report_dic["activities"]):
            logs = ""
            for item in activity["items"]:
                logs = logs + item["log"] + ", " 

            #Rounded time to report just hours
            #if activity["total_time_min"] > 30:
            #    activity["total_time_hr"] = activity["total_time_hr"]  + 1
            #Make time a fraction
            time = float(activity["total_time_hr"]) + float(activity["total_time_min"])  / 60
            
            #Save the activity info in a row for a file
            txt_dictionary = {}
            txt_dictionary["project"] = activity["project"]
            txt_dictionary["name"] = activity["name"]
            txt_dictionary["time"] = f"{time:.2f}"
            txt_dictionary["logs"] = logs
            
            rows.append(txt_dictionary)

        header = ["Activity name", "Time (hr)", "Logs"]
        
        with open(self.md_rep_file_path, "w") as md_file:
            md_file.write(f"# WEEK {self.report_dic['week_number']} REPORT\n")
            md_file.write( tabulate( rows, headers="firstrow", tablefmt = "github" , numalign="left")   )

        os.system(f"code {self.md_rep_file_path}")







