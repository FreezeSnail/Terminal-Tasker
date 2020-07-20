from datetime import date
import json

class JobModule:

        jobList = []

        def addJob(self, company, posistion, link):
            self.jobList.append({'Company': company, 
            'Posistion': posistion, 
            'Date': str(date.today()),
            'Status': "applied", 
            'Link': link })

        def print(self):
            print(self.jobList)

        def getJobList(self):
            return self.jobList

        def save(self):
            output_file = open("jobs.json", 'w', encoding='utf-8')
            for dic in self.getJobList():
                json.dump(dic, output_file) 
                output_file.write("\n")
    
        def load(self):
            with open("jobs.json") as f:
                for line in f:
                    self.jobList.append(json.loads(line)) 
