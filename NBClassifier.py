import os
import re
import string
import pandas as pd
import numpy as np

def getMaxCounts(directoryPathOfInputFiles):
    total_records=0; local_count_cell=0; local_count_wifi=0; max_cell_count=0; max_wifi_count=0
    for eachfile in os.listdir(directoryPathOfInputFiles):
        labels = eachfile.split("_")[0]
        print labels
        fin = open(directoryPathOfInputFiles + eachfile,"r")
        next(fin);   #Skips first lines
        for line in fin:
            splittedLine = re.split('\n', line)         #Splitted the line, use splttedLine[0] to access the line
            if splittedLine[0].find('_') != -1 and re.match(r'[0-9]+_[0-9]+_[0-9]+', splittedLine[0]):         #This means a new block/record has begun
                next(fin); next(fin); next(fin)         #Skip the next three lines to jump to the first EDGE CELL line
                if local_count_cell > max_cell_count:
                    max_cell_count = local_count_cell
                if local_count_wifi > max_wifi_count:
                    max_wifi_count = local_count_wifi
                local_count_cell=0; local_count_wifi=0  ## SInce we are just counting the no. of cells and wifi, make them zero locally
                print splittedLine
                total_records = total_records+1 # Keeping track of useful rows
                continue                                ## You do not want anything from these lines

            if splittedLine[0].find("EDGE Cell") != -1:
                local_count_cell= local_count_cell+1
            if splittedLine[0].find("WiFi:") != -1:
                local_count_wifi= local_count_wifi+1
        fin.close()
        print 'Max Cell Count --> ', max_cell_count   ##Can remove these print statements
        print 'Max wifi Count --> ', max_wifi_count   ##Can remove these print statements
        print 'Total records -->', total_records      ##Can remove these print statements

    return max_cell_count, max_wifi_count, total_records


#Make the column list first, now u know how many maximum cells and wifi could be there
def makeColumnHeaders(max_cell_count, max_wifi_count):
    newColumns = []
    for i in range(max_cell_count):
        newColumns.append('cell' + str(i))
        newColumns.append('rssi' + str(i))

    for j in range(max_wifi_count):
        newColumns.append('wifiIP' + str(j))
        newColumns.append('wifiStrength' + str(j))
        newColumns.append('wifiID' + str(j))

    newColumns.append('label')
    #print newColumns   #Can remove this print statement
    return newColumns


#Creaate new Data Frame and initialize all values to zero
def createNewDataFrame(total_records, newColumns):
    newDF = pd.DataFrame(0, index = np.arange(total_records), columns=list(newColumns))  #using total_records and newColumns to make a new DF.
    #print df                                                                         #again, you should remove this print statement
    return newDF


#Fill the dataframe with appropriate values and write it to the ouptput file
def fillDataIntoDataframe(outputFileNameWithPath, directoryPathOfInputFiles, max_cell_count, max_wifi_count):
    fout = open(outputFileNameWithPath,"w")

    #Iterate over all the files in that directory
    for eachfile in os.listdir(directoryPathOfInputFiles):
        local_count_cell=0; local_count_wifi=0
        labels = eachfile.split("_")[0]
        #print labels                                       ##Can remove this print

        # Open each file in that directory and read it's line one by one.
        fin = open(directoryPathOfInputFiles + eachfile,"r")
        next(fin)                                           #Skips the first line that is of no use for us.
        local_count_cell=0; local_count_wifi=0;
        for line in fin:
            splittedLine = re.split('\n', line)              #Splitted the line, use splttedLine[0] to access the line
            if splittedLine[0].find("EDGE Cell") != -1:
                flag = True
                arr = splittedLine[0].split(' ')
                fout.write(arr[3] + "," + arr[7] + ",")
                local_count_cell= local_count_cell+1
                continue

            if splittedLine[0].find("WiFi:") != -1 and flag == True:
                if local_count_cell != 0:
                    cell_difference = max_cell_count-local_count_cell  # find the difference between the local count and max count
                    for diff in range(cell_difference):
                        fout.write('0' + "," + '0' + ",")
                flag = False


            if splittedLine[0].find("WiFi:") != -1 and flag == False:
                arr = splittedLine[0].split(' ')
                fout.write(arr[1])
                fout.write("," + arr[-2] + "," + arr[-1] + ",")
                local_count_wifi= local_count_wifi+1
                continue

            if splittedLine[0].find('_') != -1 and re.match(r'[0-9]+_[0-9]+_[0-9]+', splittedLine[0]): #This means a new block/record has begun
                if local_count_wifi != 0:
                    #print labels, "-->",  splittedLine[0]              ## Can remove these Print statements
                    wifi_difference = max_wifi_count-local_count_wifi  # find the difference between this count and max count
                    for diff in range(wifi_difference):
                        fout.write('0' + "," + '0' + "," + '0' + ",")

                    fout.write(labels)
                    fout.write("\n")

                next(fin); next(fin); next(fin)                         #Skip the next three lines to jump to the first EDGE CELL line
                local_count_cell=0; local_count_wifi=0
            #Inner for loop ends here.

        #THis is also part of Outer for loop
        wifi_difference = max_wifi_count-local_count_wifi  # find the difference between this count and max count
        for diff in range(wifi_difference):
            fout.write('0' + "," + '0' + "," + '0' + ",")
        fout.write(labels)
        fout.write("\n")
        fin.close()
        #Outer for loop ends here.

    fout.close()
    return True
#The method definition ends here



if __name__ == "__main__":
    #Define the input file directory path and output file name with path.
    outputFileNameWithPath = "C:/Users/Anshul/Desktop/Courses/Wireless/Final_Project/output1Directly.csv"
    directoryPathOfInputFiles = "C:/Users/Anshul/Desktop/Courses/Wireless/Final_Project/Initial_Data/"

    #Get the max count of cells and wifi
    max_cell_count, max_wifi_count, total_records = getMaxCounts(directoryPathOfInputFiles)

    #Get the list of newColumns
    newColumns = makeColumnHeaders(max_cell_count, max_wifi_count)

    #Get back a new DataFrame of size total_records x length of newColumns. This will initially be filled with all zeros
    df = createNewDataFrame(total_records, newColumns)

    #Fill the dataframe with appropriate values and write it to the ouptput file
    wasFillingASuccess = False
    wasFillingASuccess = fillDataIntoDataframe(outputFileNameWithPath, directoryPathOfInputFiles, max_cell_count, max_wifi_count)
    print 'Was filling data and writing to output file successful? -->', wasFillingASuccess

    #Now load this output file into a new dataframe which is going to be fed to the naive bayes classifier
    dfFinal = pd.read_csv("C:/Users/Anshul/Desktop/Courses/Wireless/Final_Project/output1Directly.csv", header=None)
    print dfFinal
