import csv
import sys
import os

class CSVManip:
	headers = []
	records = []
	csvfile = sys.argv[1]
	scriptPath = os.path.abspath(os.path.dirname(sys.argv[0]))

	def __init__(self):
		f = open(self.csvfile, 'rt')
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

	def exportRecords(self, sublist, filename):
		print(os.path.join(self.scriptPath, filename))
		with open(os.path.join(self.scriptPath, filename + '.csv'), 'w', newline='') as exportcsv:
			csvwriter = csv.DictWriter(exportcsv, sublist[0].keys())
			csvwriter.writeheader()
			csvwriter.writerows(sublist)
		
		exportcsv.close()
	
	def sortRecords(self, sublist):
		print("Select fields to sort by -")
		for i, field in enumerate(self.headers):
			print("{}: {}, ".format(i, field), end="")
		print(" -1 to quit")
	
		sortFields = []
	
		userChoice = int(input(":: "))
		while (userChoice >= 0):
			if userChoice >= 0 and userChoice <= len(self.headers)-1:
				sortFields.append(self.headers[userChoice])
		
			print("Current sort list: ", end="")
			for field in sortFields:
				print("{}, ".format(field), end="")
				
			print()
		
			userChoice = int(input(":: "))
		
		if len(sortFields) > 0:
			for field in reversed(sortFields):
				self.records = sorted(self.records, key=lambda k: k[field])
				
		for row in self.records:
			print(str(row['date_issued']).encode(sys.stdout.encoding, errors='replace'), end="")
			print(str(row['authors']).encode(sys.stdout.encoding, errors='replace'))
	
	def divideRecords(self, NumOfLists, filename):
		ListSize = int(len(self.records) / NumOfLists) # Records spread across all lists
		CountedRecords = ListSize * NumOfLists
		UncountedRecords = len(self.records) - CountedRecords
		
		for i in range(0, NumOfLists):
			if i < NumOfLists-1:
				endList = ListSize * (i+1)
			else:
				endList = len(self.records)
				
			self.exportRecords(self.records[ListSize*i:endList], (filename + "_" + str(i+1)))

		
def main():
	myArray = CSVManip()
	
	myArray.sortRecords(myArray.records)
	myArray.exportRecords(myArray.records, 'export')
	myArray.divideRecords(5, 'export')
	
if __name__ == "__main__":
    main()