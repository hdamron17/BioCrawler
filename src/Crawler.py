#! /usr/bin/env python

'''
Crawls various files and detects birth/death dates

NOTE: The data produced by this is not always exactly accurate due to the vagueness of some cemetery entries. Do a quick manual verification.
'''

import dateutil.parser as dateutil
from datetime import datetime
import csv


INPUT_DIR = "inputs"
OUTPUT_DIR = "outputs"

JAN1 = datetime.strptime("1/1/0001", '%m/%d/%Y')
MIN = 0 * 365.25 #min years to accept
MAX = 120 * 365.25 #max years to accept

def people(file, n=100):
    '''
    Parses text and detects people and birth/death dates
    Note: discards all unusable people
    :param file: File object to iterate
    :param n: max number to count, -1 if all should be counted
    :return: returns generator of people with (name, birth date, death date)
    '''
    count = 0
    for line in file:
        parts = [part.strip() for part in line.split(",")]
        
        name = "%s, %s" % (parts[0], parts[1])
        birth = None
        death = None
        
        for i in range(2, len(parts)):
            part = parts[i]
            if part.startswith("b. "):
                birthstr = part.replace("b. ", "")
                try: 
                    birth_datetime = dateutil.parse(birthstr, default=JAN1)
                    if birth_datetime.year == 1:
                        try:
                            birth_datetime = birth_datetime.replace(year=int(parts[i+1]))
                        except:
                            birth = None
                            raise Exception()
                    birth = datetime.strftime(birth_datetime, '%m/%d/%Y')
                except: pass
            
            elif part.startswith("d. "):
                deathstr = part.replace("d. ", "")
                try: 
                    death_datetime = dateutil.parse(deathstr, default=JAN1)
                    if death_datetime.year == 1:
                        try:
                            death_datetime = death_datetime.replace(year=int(parts[i+1]))
                        except:
                            death = None
                            raise Exception()
                    death = datetime.strftime(death_datetime, '%m/%d/%Y')
                except: pass
        
        if name and birth and death:
            try:
                if MIN > (datetime.strptime(death, '%m/%d/%Y') - datetime.strptime(birth, '%m/%d/%Y')).days > MAX:
                    continue
            except: continue
            
            yield (name, birth, death)
            count += 1
            if count >= n and n != -1:
                break

def main():
    num = -1
    names = ("greenwood", "enoree")
    for name in names:
        with open("inputs/%s.txt" % name, "r") as fp, open("outputs/%s.csv" % name, "w+", newline='') as outfile:
            writer = csv.writer(outfile)
            for item in people(fp, n=num):
                writer.writerow((item[1], item[2]))

if __name__ == "__main__":
    main()