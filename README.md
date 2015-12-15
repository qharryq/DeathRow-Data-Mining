Project as part of a Data warehousing & data mining module.
We are aiming to predict the sentiment of the final statement of an inmate on deathrow, e.g. whether or not they show remorse, are they positive, negative, religious or in denial - based on attributes such as their age at the time of the crime, prior convictions, type of crime committed, etc.

Our findings are explained in report.docx

There are two different datasets:

inmate.csv contains all of the data scraped from https://www.tdcj.state.tx.us/death_row/dr_executed_offenders.html - missing the 12 earliest executions. A lot of the information was available only in .JPG format, which we manually added to the dataset.

finaldb.csv contains this data but it has been modified after sentiment analysis was carried out. The attribute final statement states whether or not a final statement was given. The crime has been summarised for each inmate. The prior record attribute now has a yes/no value. There is a new attribute - number of victims. There is an attribute for remorse, religion, denial, anger & acceptance - These have a binary value (1 = yes 0 = no)
