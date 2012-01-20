# handling date/time data
# Python23 tested   vegaseat   3/6/2005

import time
from time import time

print "List the functions within module time:"
for funk in dir(time):
  print funk

print time.time(), "seconds since 1/1/1970 00:00:00"
print time.time()/(60*60*24), "days since 1/1/1970"

# time.clock() gives wallclock seconds, accuracy better than 1 ms
# time.clock() is for windows, time.time() is more portable
print "Using time.clock() = ", time.clock(), "seconds since first call to clock()"
print "\nTiming a 1 million loop 'for loop' ..."
start = time.clock()
for x in range(1000000):
  y = x  # do something
end = time.clock()
print "Time elapsed = ", end - start, "seconds"

# create a tuple of local time data
timeHere = time.localtime()
print "\nA tuple of local date/time data using time.localtime():"
print "(year,month,day,hour,min,sec,weekday(Monday=0),yearday,dls-flag)"
print timeHere

# extract a more readable date/time from the tuple
# eg.  Sat Mar 05 22:51:55 2005
print "\nUsing time.asctime(time.localtime()):", time.asctime(time.localtime())
# the same results
print "\nUsing time.ctime(time.time()):", time.ctime(time.time())
print "\nOr using time.ctime():", time.ctime()

print "\nUsing strftime():"
print "Day and Date:", time.strftime("%a %m/%d/%y", time.localtime())
print "Day, Date   :", time.strftime("%A, %B %d, %Y", time.localtime())
print "Time (12hr) :", time.strftime("%I:%M:%S %p", time.localtime())
print "Time (24hr) :", time.strftime("%H:%M:%S", time.localtime())
print "DayMonthYear:",time.strftime("%d%b%Y", time.localtime())

print

print "Start a line with this date-time stamp and it will sort:",\
    time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())

print

def getDayOfWeek(dateString):
  # day of week (Monday = 0) of a given month/day/year
  t1 = time.strptime(dateString,"%m/%d/%Y")
  # year in time_struct t1 can not go below 1970 (start of epoch)!
  t2 = time.mktime(t1)
  return(time.localtime(t2)[6])

Weekday = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
  'Friday', 'Saturday', 'Sunday']

# sorry about the limitations, stay above 01/01/1970
# more exactly 01/01/1970 at 0 UT (midnight Greenwich, England)
print "11/12/1970 was a", Weekday[getDayOfWeek("11/12/1970")]

print

print "Calculate difference between two times (12 hour format) of a day:"
time1 = raw_input("Enter first time (format 11:25:00AM or 03:15:30PM): ")
# pick some plausible date
timeString1 = "03/06/05 " + time1
# create a time tuple from this time string format eg. 03/06/05 11:22:00AM
timeTuple1 = time.strptime(timeString1, "%m/%d/%y %I:%M:%S%p")

#print timeTuple1   # test eg. (2005, 3, 6, 11, 22, 0, 5, 91, -1)

time2 = raw_input("Enter second time (format 11:25:00AM or 03:15:30PM): ")
# use same date to stay in same day
timeString2 = "03/06/05 " + time2
timeTuple2 = time.strptime(timeString2, "%m/%d/%y %I:%M:%S%p")

# mktime() gives seconds since epoch 1/1/1970 00:00:00
time_difference = time.mktime(timeTuple2) - time.mktime(timeTuple1)
#print type(time_difference)  # test <type 'float'>
print "Time difference = %d seconds" % int(time_difference)
print "Time difference = %0.1f minutes" % (time_difference/60.0)
print "Time difference = %0.2f hours" % (time_difference/(60.0*60))

print

print "Wait one and a half seconds!"
time.sleep(1.5)
print "The end!"
