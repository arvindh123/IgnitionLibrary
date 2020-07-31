def GetDaysRange(Start,End,Interval="Week",WeekStart="Sunday",Debug=False):
	"""
	Start - Datatype : java.util.date , Star date of the date range 
	End  - Datatype : java.util.date , End Date of the date range 
	Interval - Datatype : string, Support Options : 1.) Week 2.) Month 3.)Year, Defualt Option :  Week
	Weekstart - Datatype : String Supported Options : 1.)Monday , 2.)Tuesday 3.) Sunday   Default Option: Sunday  
	Debug - Datatype : Boolean  , Default - False , To print the internal vairables for debug  Default Value  : False
	"""
	RangeDate = [] 
	DaysIn = {0:31,1:28,2:31,3:30,4:31,5:30,6:31,7:31,8:30,9:31,10:30,11:31,99:29}
	if Interval == 'Day':
			Daysbetween = system.date.daysBetween(Start,End)
			DaysRange = [system.date.addDays(Start,n+1) for n in range(0,Daysbetween,1)]
            return DaysRange
			
	if Interval == 'Year':
		StartYear = system.date.getYear(Start)
		
		RangeDate.append([Start, system.date.setTime(system.date.getDate(StartYear+1, 0, 1),0,0,0)])
		Previous = system.date.setTime(system.date.getDate(StartYear+1, 0, 1),0,0,0)
		i=0
		while system.date.getYear(Previous) < system.date.getYear(End):
			CurrEnd = system.date.setTime(system.date.getDate(system.date.getYear(Previous)+1, 0, 1),0,0,0)
			RangeDate.append([Previous,CurrEnd])
			Previous = CurrEnd
			if i > 100 :
				break
		if Previous == End :
			if system.date.millisBetween(Previous,End) > 0 : 
				RangeDate.append([ Previous, End])
		else :
			RangeDate.append([ Previous , End])

		
	if Interval  == 'Month':
		StartMonth = system.date.getMonth(Start)
		StartMonthDays = DaysIn[StartMonth]
		StartMonthRemainingDays = StartMonthDays - system.date.getDayOfMonth(Start)
		
		EndMonth = system.date.getMonth(End)
		EndMonthDays = DaysIn[EndMonth]
		EndMonthRemainingDays =  EndMonthDays- system.date.getDayOfMonth(End)
		
		RangeDate.append([Start,system.date.midnight(system.date.addDays(Start,StartMonthRemainingDays+1))])
		PreviousDay=system.date.midnight(system.date.addDays(Start,StartMonthRemainingDays+1))
		i=0
		while __CheckMonthAndYearIsLesser__(PreviousDay,End):
			CurrentMonth = system.date.getMonth(PreviousDay)
			if CurrentMonth == 1:
				if system.date.getYear(PreviousDay) % 4 ==0:
					CurrentMonth = 99
			NumOfDaysInMonth = DaysIn[CurrentMonth]
			RangeDate.append([PreviousDay,system.date.addDays(PreviousDay,NumOfDaysInMonth)])
			PreviousDay = system.date.addDays(PreviousDay,NumOfDaysInMonth)

		if PreviousDay == End :
			if system.date.millisBetween(PreviousDay,End) > 0 : 
				RangeDate.append([ PreviousDay, End])
		else :
			RangeDate.append([ PreviousDay , End])
		
		
	if Interval == 'Week':
		NumOfDaysInWeek = 7 
		if WeekStart == 'Monday':
			StartWeekDay = system.date.getDayOfWeek(Start) -1 
			EndWeekDay = system.date.getDayOfWeek(End) - 1
		elif WeekStart == 'Tuesday':
			StartWeekDay = system.date.getDayOfWeek(Start) - 2
			EndWeekDay = system.date.getDayOfWeek(End) - 2
		else : 
			StartWeekDay = system.date.getDayOfWeek(Start) 
			EndWeekDay = system.date.getDayOfWeek(End) 
		if Debug : 
			print 'StartWeekDay',StartWeekDay
			print 'EndWeekDay',EndWeekDay
		if StartWeekDay < 1 :
			StartWeekDay = 7- StartWeekDay
		if EndWeekDay < 1 :
			EndWeekDay = 7 - EndWeekDay
		
		FirstWeekDays = NumOfDaysInWeek -  StartWeekDay
		LastWeekDays = EndWeekDay
		FirstAndLastWeek = FirstWeekDays + LastWeekDays 
		Daysbetween = system.date.daysBetween(Start, End)
		BetweenDays = Daysbetween-FirstAndLastWeek
		if Debug :
			print 'StartWeekDay',StartWeekDay
			print 'EndWeekDay',EndWeekDay
			print 'FirstWeekDays',FirstWeekDays
			print 'LastWeekDays',LastWeekDays
			print 'FirstAndLastWeek', FirstAndLastWeek
			print 'Daysbetween', Daysbetween
			print 'BetweenDays', BetweenDays
	
	
		RangeDate.append([Start, system.date.midnight(system.date.addDays(Start,FirstWeekDays+1))])
		
		PreviousStartDay =  system.date.midnight(system.date.addDays(Start,FirstWeekDays+1))
		
		for day in range(0,BetweenDays,7):
			RangeDate.append([PreviousStartDay , system.date.addDays(PreviousStartDay,7)])
			PreviousStartDay = system.date.addDays(PreviousStartDay,7)
			
		if PreviousStartDay == End :
			if system.date.millisBetween(PreviousStartDay,End) > 0 : 
				RangeDate.append([ PreviousStartDay, End])
		else :
			RangeDate.append([ PreviousStartDay , End])
	else :
		pass
	return RangeDate
	
	
def __CheckMonthAndYearIsLesser__(start,end):
	if system.date.getYear(start) >= system.date.getYear(end):
		if system.date.getMonth(start)>=system.date.getMonth(end):
			return False
