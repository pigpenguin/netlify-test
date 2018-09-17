import os
from num2words import num2words

def format_time(time):
    """ Formats milliseconds to hh:mm:ss.ff"""
    hours = (time//(1000*60*60)) % 60
    minutes = (time//(1000*60)) % 60
    seconds = (time/1000) % 60
    return "{}:{:02d}:{:05.2f}".format(hours, minutes, seconds)

def format_place(place):
    return num2words(place, to="ordinal_num")

class cd:
    """ Context manager to enter directories and do stuff """
    def __init__(self,new_path):
        mkdir(new_path)
        self.new_path = os.path.abspath(new_path)

    def __enter__(self):
        self.saved_path = os.getcwd()
        os.chdir(self.new_path)
        return self

    def __exit__(self, etype, value, traceback):
        os.chdir(self.saved_path)

    def open(self, path, mode):
       return open(os.path.join(self.new_path, path), mode)

def mkdir(directory):
    if not os.path.isdir(directory):
        os.makedirs(directory)
