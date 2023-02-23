import time
import pickle
import os
import datetime
from playsound import playsound


class CountdownError(Exception):
    pass


class Reminder:
    def __init__(self, name, message, alarm_music, alarm_time=None, alarm_on=True):
        self.name = name
        self.message = message
        self.alarm_music = alarm_music
        self.alarm_time = alarm_time
        self.alarm_on = alarm_on
        self.turn_on_off = True

    def create_alarm(self):
        if self.alarm_time:
            time_diff = (self.alarm_time - datetime.datetime.now()).total_seconds()
            if time_diff > 0:
                time.sleep(time_diff)
                if self.alarm_on:
                    playsound(self.alarm_music)
                    print(self.message)
                else:
                    print("Alarm is switched off.")
            else:
                raise ValueError("Alarm time is in the past.")
        else:
            raise ValueError("Alarm time not set.")

    def days_until(self):
        if self.alarm_time:
            time_diff = (self.alarm_time - datetime.datetime.now()).total_seconds()
            return int(time_diff / 86400)
        else:
            raise ValueError("Alarm time not set.")


class ReminderSet:
    def __init__(self):
        self.reminders = {}

    def add_a_reminder(self, name, message, alarm_music, alarm_time=None):
        reminder = Reminder(name, message, alarm_music, alarm_time)
        self.reminders[name] = reminder
        if alarm_time:
            reminder.create_alarm()

    def show_reminders(self):
        if not self.reminders:
            print("No reminders have been set.")
            return
        for alarm, reminder in self.reminders.items():
            print(
                f"Name: {alarm}\nMessage: {reminder.message}\nAlarm Sound:"
                f" {reminder.alarm_music}\nAlarm On: {reminder.alarm_on}\n")

    def edit_reminder(self, alarm):
        reminder = self.reminders.get(alarm)
        if reminder:
            message = input("Enter a new reminder message: ")
            alarm_music = input("Enter new path of the alarm sound/song: ")
            if not os.path.isfile(alarm_music):
                print("Incorrect file path")
                return
            reminder.message = message
            reminder.alarm_music = alarm_music
            print(f"Reminder '{alarm}' has been modified.")
        else:
            print(f"Reminder '{alarm}' could not be found.")

    def trigger_reminder(self, alarm):
        reminder = self.reminders.get(alarm)
        if reminder:
            reminder.create_alarm()
        else:
            print(f"Reminder '{alarm}' could not be found.")

    def delete_reminder(self, alarm):
        reminder = self.reminders.get(alarm)
        if reminder:
            self.reminders.pop(alarm)
            print(f"Reminder '{alarm}' has been deleted.")
        else:
            print(f"Reminder '{alarm}' could not be found.")

    def alarm_switch(self, alarm):
        reminder = self.reminders.get(alarm)
        if reminder:
            reminder.turn_on_off = not reminder.turn_on_off
            if reminder.turn_on_off:
                print(f"Alarm for reminder '{alarm}' turned on.")
            else:
                print(f"Alarm for reminder '{alarm}' turned off.")
        else:
            print(f"Reminder '{alarm}' not found.")

    def save_alarm_list(self):
        with open("alarm_list.pickle", "wb") as f:
            pickle.dump(self.reminders, f)

    @staticmethod
    def load_alarm_list():
        try:
            with open("alarm_list.pickle", "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return ReminderSet()


def main():
    reminder_app = ReminderSet()

    while True:
        print("1. Add a New Reminder")
        print("2. Show Current Reminders in list")
        print("3. Edit a Reminder")
        print("4. Play Alarm for a definite Reminder")
        print("5. Delete a Reminder")
        print("6. Turn On/Off Alarm for a Reminder")
        print("7. Add a New Reminder with a definite Alarm time")
        print("8. Exit the application")

        choice = input("Enter your preferred input (1-8): ")

        if choice == "1":
            alarm = input("Enter reminder name: ")
            message = input("Enter reminder message: ")
            alarm_music = input("Enter path of the alarm sound/song: ")
            if not os.path.isfile(alarm_music):
                print("Invalid file path")
                continue
            reminder_app.add_a_reminder(alarm, message, alarm_music)
        elif choice == "2":
            reminder_app.show_reminders()
        elif choice == "3":
            alarm = input("Enter reminder name: ")
            reminder_app.edit_reminder(alarm)
        elif choice == "4":
            alarm = input("Enter reminder name: ")
            reminder = reminder_app.reminders.get(alarm)
            if reminder:
                if not reminder.alarm_time:
                    alarm_time = input("Enter the alarm time (YYYY-MM-DD HH:MM:SS): ")
                    reminder.alarm_time = datetime.datetime.strptime(alarm_time, "%Y-%m-%d %H:%M:%S")
                reminder_app.trigger_reminder(alarm)
            else:
                print(f"Reminder '{alarm}' could not be found.")
        elif choice == "5":
            alarm = input("Enter reminder name: ")
            reminder_app.delete_reminder(alarm)
        elif choice == "6":
            alarm = input("Enter reminder name: ")
            reminder_app.alarm_switch(alarm)
        elif choice == "7":
            alarm = input("Enter reminder name: ")
            message = input("Enter reminder message: ")
            alarm_music = input("Enter path of the alarm sound/song: ")
            if not os.path.isfile(alarm_music):
                print("Invalid file path")
                continue
            alarm_time = input("Enter the alarm time in the format 'YYYY-MM-DD HH:MM:SS': ")
            alarm_time = datetime.datetime.strptime(alarm_time, "%Y-%m-%d %H:%M:%S")
            reminder_app.add_a_reminder(alarm, message, alarm_music, alarm_time=alarm_time)
        elif choice == "8":
            reminder_app.save_alarm_list()
            print("Exiting the application...")
            break
        else:
            print("Invalid choice, please select a number between 1 and 8.")


if __name__ == "__main__":
    main()
