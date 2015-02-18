import csv
import sys
import os

class CSVManip:
	headers = []
	records = []
	scriptPath = os.path.abspath(os.path.dirname(sys.argv[0]))

	def __init__(self, filename):
		f = open(filename, 'rt')
		try:
			reader = csv.DictReader(f)
			
			for row in reader:
				self.records.append(row)
		
			for key, value in self.records[0].items():
				if key == "":
					continue
					
				self.headers.append(key)
				
		finally:
			f.close()

	""" @parameters: 	records (list of dictionaries: representing single csv file), 
						filename (string: file to export file to)
		@return:		NULL
	"""
	def exportRecords(self, records, filename):
		print(filename)
		if not os.path.exists(os.path.dirname(os.path.realpath(filename))):
			os.makedirs(os.path.dirname(os.path.realpath(filename)))
	
		with open(os.path.join(self.scriptPath, filename + '.csv'), 'w', newline='') as exportcsv:
			csvwriter = csv.DictWriter(exportcsv, records[0].keys())
			csvwriter.writeheader()
			csvwriter.writerows(records)
		
		exportcsv.close()

		
	""" @parameters:	records (list of dictionaries)
		@return:		sortedlist (list of dictionaries)
		@description:	Determines possible fields based on header contents.
						Gives user option of one or more fields to sort by, quit on a -1.
						After user supplies sort, sorts list and return list.
	"""
	def sortRecords(self, records):
		print("Select fields to sort by -")
		for i, field in enumerate(self.headers):
			print("{}: {}, ".format(i, field), end="")
		print(" -1 to quit")
	
		sortFields = []

		try:
			userChoice = int(input(":: "))
		except:
			userChoice = -1

		while (userChoice >= 0):
			if userChoice <= len(self.headers)-1:
				sortFields.append(self.headers[userChoice])
		
			print("Current sort list: ", end="")
			for field in sortFields:
				print("{}, ".format(field), end="")
				
			print()
			
			try:
				userChoice = int(input(":: "))
			except:
				userChoice = -1
			
		if len(sortFields) > 0:
			for field in reversed(sortFields):
				records = sorted(records, key=lambda k: k[field])
				
		return records
		
	"""	@parameters:	records (list of dictionaries: records to be manipulated)
						numOfLists (int: number of lists to divide array into)
						filename (string: prefix file name)
		@return:		NULL
		@description:	takes an array of records, then sub-divides the array into 
						equal parts, and exports numOfList files with near equal
						records into each. The largest list will always be the final list.
	"""
	def divideRecords(self, records, numOfLists, filename):
		ListSize = int(len(records) / numOfLists) # Records spread across all lists
		CountedRecords = ListSize * numOfLists
		UncountedRecords = len(records) - CountedRecords
		
		for i in range(0, numOfLists):
			if i < numOfLists-1:
				endList = ListSize * (i+1)
			else:
				endList = len(records)
				
			self.exportRecords(records[ListSize*i:endList], (filename + "_" + str(i+1)))


if __name__ == "__main__":
	dataFile = input("Please enter name / path of csv datafile: ")
	myArray = CSVManip(dataFile)
	
	try:
		numberOfFiles = int(input("How many files do you want the record divided into?[1]: "))
	except:
		numberOfFiles = 1
		
	outputFile = input("Enter name of output files (will be in folder exported)[export]: ")
	if outputFile == '':
		outputFile = 'export'
		
	myArray.divideRecords(myArray.sortRecords(myArray.records), numberOfFiles, 'exported\\'+outputFile)