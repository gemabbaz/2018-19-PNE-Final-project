#GEMA BENITO BAZ
import http.client
import json
import socketserver    #Here I imported all the packages I will use
import http.server
from seq import Seq


PORT = 8000   #Defining PORT
socketserver.TCPServer.allow_reuse_address = True


HOSTNAME = "rest.ensembl.org"
ENDPOINT1 = "/info/species?content-type=application/json"
ENDPOINT2 = "/info/assembly/"
ENDPOINT4 = "/sequence/id/"                                  #I defined here every endpoint I will used
ENDPOINT5 = "/lookup/symbol/homo_sapiens/"                   #Each of them will be used for one of the functions, except
ENDPOINT6 = "/lookup/id/"                                    #EDNPOINT2 that it will be used for /karyotype and /chromosomeLength
ENDPOINT7 = "/overlap/region/human/"
METHOD = "GET"
headers = {'User-Agent': 'http-client'}

def list_species(basic):     #Function to be used in /listSpecies, creating and empty list and appending each specie to its display name
    names = []
    for i in basic["species"]:
        names.append(i)
    list1 = []
    for i in range(len(names)):
        list1.append(names[i]["display_name"])

    return list1


def karyotype_function(specie):  #This function will be used for /karyotype and /chromosomeLength function. ALl these indications are the same for the rest.
    conn = http.client.HTTPSConnection(HOSTNAME)
    conn.request(METHOD, ENDPOINT2 + specie + "?content-type=application/json", None, headers) #Request the main page (GET method)
    print(ENDPOINT2 + specie + "?content-type=application/json")
    r1 = conn.getresponse() #reading message
    print()
    print("Response received: ", end='')
    print(r1.status, r1.reason)
    text_json = r1.read().decode("utf-8")
    karyotype = json.loads(text_json) #variable with the data received

    return karyotype


def human_sequence(specie):  #This function will be used in function /geneSeq and /geneCalc
    conn = http.client.HTTPSConnection(HOSTNAME)
    conn.request(METHOD, ENDPOINT4 + specie + "?content-type=application/json", None, headers)
    r1 = conn.getresponse()
    print()
    print("Response received: ", end='')
    print(r1.status, r1.reason)
    text_json = r1.read().decode("utf-8")
    human = json.loads(text_json)
    sequence = human['seq']

    return sequence


def gene_function(gene):   #This function will be used in function /geneSeq, /geneInfo and /geneCalc
    conn = http.client.HTTPSConnection(HOSTNAME)
    conn.request(METHOD, ENDPOINT5 + gene + "?expand=1;content-type=application/json", None, headers)
    r1 = conn.getresponse()
    print()
    print("Response received: ", end='')
    print(r1.status, r1.reason)
    text_json = r1.read().decode("utf-8")
    gen = json.loads(text_json)
    if 'id' in gen:    #In this way it was much easier to avoid errors, assigning a zero value to the id in case the specie did not exist
        id = gen['id']
    else:
        id = '0'

    return id

def info_function(specie): #This function will be used in function /geneInfo
    conn = http.client.HTTPSConnection(HOSTNAME)
    conn.request(METHOD, ENDPOINT6 + specie + "?content-type=application/json;expand=1", None, headers)
    r1 = conn.getresponse()
    print()
    print("Response received: ", end='')
    print(r1.status, r1.reason)
    text_json = r1.read().decode("utf-8")
    human = json.loads(text_json)

    return human

def list_function(chromo, start, end):  #This function will be used in function /geneList
    conn = http.client.HTTPSConnection(HOSTNAME)
    conn.request(METHOD, ENDPOINT7 + chromo + ":" + start + "-" + end + "?content-type=application/json;feature=gene;", None, headers)
    r1 = conn.getresponse()
    print()
    print("Response received: ", end='')
    print(r1.status, r1.reason)
    text_json = r1.read().decode("utf-8")
    list = json.loads(text_json)

    return list



class TestHandler(http.server.BaseHTTPRequestHandler): #Now, my class will have all the methods and properties
    def do_GET(self):
        print("GET received")
        print("Request line" + self.requestline) #With all these printings it was easier to idenfity our values
        print("       Cmd:  " + self.command)
        print("Path:  " + self.path)
        if self.path == "/": #If user types in /, he will be directed to the main html
            file = open("main.html")
            content = file.read()
            file.close()
        elif "/listSpecies" in self.path: #If user introduces /listSpecies, the following tasks will be performed
            conn = http.client.HTTPSConnection(HOSTNAME)
            conn.request(METHOD, ENDPOINT1, None, headers)
            r1 = conn.getresponse()
            print()
            print("Response received: ", end='')
            print(r1.status, r1.reason)
            text_json = r1.read().decode("utf-8")
            basic = json.loads(text_json)
            list1 = list_species(basic) #Calling function
            listspecies = "LIST OF AVAILABLE SPECIES: " + "\n"
            listspecies2 = " " #Along this practices I created some empty strings to make it easier to add different information
            if "limit" in self.path:  #If user types in a limit, the task will have to be modified
                limit = self.path[self.path.find("=") + 1:] #finding limit
                if limit == '':
                    for i in list1:
                        listspecies2 += "Specie: " + i + "<br>"
                elif limit.isalpha(): #In case the limit is a letter
                    listspecies2 += "Your limit must be an integer!"
                else:
                    limit = int(limit)  #In case the limit is out of boundaries
                    if limit > len(list1) or limit <= 0:
                        listspecies2 += "Your limit must be an integer between 0 and " + str(len(list1)) + " Try again"
                    else:
                        listspecies = " WE'LL SHOW " + str(limit) + " OUT OF " + str(len(list1)) + " SPECIES"
                        listspecies2 = " "
                        for i in range(limit):
                            listspecies2 += "Specie nº " + str(i + 1) + ": " + list1[i] + "<br>"
            else:
                listspecies = "Available species: " + "\n"
                listspecies2 = " "
                for i in list1:
                    listspecies2 += "Specie: " + i + "<br>"
            content = """  
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <title>Information of species: </title>
                    </head>
                    <body style="background-color: lightyellow;">
                        <fieldset>
                            <legend style="color:lightgreen;font-family:arial;font-size:250%;text-align:center">{}</legend>
                            <p style="color:black;font-family:arial;font-size:100%">{}</p>
                        </fieldset>
                    <a href="/">Main page</a>
                    </body>
                    </html>
                    """.format(listspecies, listspecies2)  #Instead of creating a new HTML file per function, I directly created them here in the server.
                                                        #sending the information

        elif "/karyotype" in self.path:
            specie = self.path[self.path.find("=") + 1:] #finding the specie introduced
            specie = specie.replace("+", "")
            specie = specie.upper() #capital letters also valid
            info2 = karyotype_function(specie) #calling function
            chromosomes = ""
            message = specie.upper()
            if "karyotype" in info2:  #if the specie introduced has its karyotype we will keep going
                list2 = info2["karyotype"] #finding the karyotype
                for i in range(len(list2)):
                    chromosomes += list2[i] + "\n"
            else: #in case the specie is not valid
                chromosomes += "Either we do not have the information for that specie or that specie does not exist! "
            print(message, chromosomes)

            content = """
                    <!DOCTYPE html>
                    <html lang = "en">
                    <head>
                        <meta charset = "UTF-8">
                        <title>Information of karyotypes:</title>
                    </head>
                    <body style="background-color: lightyellow;">
                        <h1 style="color:lightgreen;font-family:arial;font-size:250%;text-align:center"> KARYOTYPE</h1>
                        <fieldset>
                            <legend style="color:black;font-family:arial;font-size:150%;text-align:center">{}</legend>
                            <p style="color:black;font-family:arial;font-size:100%">{}</p>
                        </fieldset>
                    <a href="/">Main page</a>
                    </body>
                    </html>
                    """.format(message, chromosomes)



        elif "/chromosomeLength" in self.path:
            try:
                specie = self.path[self.path.find("=") + 1:self.path.find("&")] #finding the specie introduced
                specie1 = self.path[self.path.find("?")+1:self.path.find("=")] #"specie="
                msg = ""
                karyotype_json = karyotype_function(specie) #calling function
                karyotype = karyotype_json["top_level_region"]
                length = dict()                #Here, as I had many problems fixing all the possible mistakes, I created dictionaries and used except statement
                for element in range(len(karyotype)):
                    if specie1 != "specie": #in case the user in the URL doesn't write correctly specie=...
                        msg += "Error"
                        pass
                    elif karyotype[element]["coord_system"] == "chromosome":
                        length[karyotype[element]["name"]] = karyotype[element]["length"]
                    else:
                        length[karyotype[element]["name"]] = karyotype[element]["length"] #some species such as cow do not have as coord_system = chromosome
                num = self.path[self.path.find("o=") + 2:] #number of chromosome introduced
                msg += "The length of the chromosome is: " + str(length[num.upper()])
            except KeyError:
                msg = "You introduced an incorrect value"
            content = """                                                                                                                            
                        <!DOCTYPE html>                                                                                                          
                        <html lang="en">                                                                                                         
                        <head>                                                                                                                   
                            <meta charset="UTF-8">                                                                                               
                            <title>Information of chromosome's length: </title>                                                                  
                        </head>                                                                                                                  
                        <body style="background-color: lightyellow;">                                                                            
                            <h1 style="color:lightgreen;font-family:arial;font-size:250%;text-align:center"> CHROMOSOME LENGTH</h1>              
                            <fieldset>                                                                                                           
                                <p style="color:black;font-family:arial;font-size:150%;text-align:center">{}</p>                                                                                              
                            </fieldset>                                                                                                          
                        <a href="/">Main page</a>                                                                                                
                        </body>                                                                                                                  
                        </html>                                                                                                                  
                        """.format(msg)

        elif "/geneSeq" in self.path:
            specie = self.path[self.path.find("=") + 1:] #finding specie (human)
            specie = specie.lower()
            gene = self.path[self.path.find("?")+1:self.path.find("=")] #finding gene
            message = ''
            info4 = gene_function(specie) #calling function
            if gene != "gene": #In case user types in incorrectly 'gene' in URL a warning message will pop up. It will also be perfomed in the following functions
                message += "No information available"
                pass
            elif info4 == "0": #if the gene does not exist. It will also be perfomed in the following functions
                message += "No information available"
            else:
                sequence = human_sequence(info4)
                message += sequence #adding sequence in order to print it out
            content = """
                                <!DOCTYPE html>
                                <html lang="en">
                                <head>
                                    <meta charset="UTF-8">
                                    <title>Information of gene sequence: </title>
                                </head>
                                <body style="background-color: lightyellow;">
                                    <h1 style="color:lightgreen;font-family:arial;font-size:250%;text-align:center"> GENE SEQUENCE</h1>
                                    <fieldset>
                                        <p style="color:black;word-break:break-all;font-family:arial;font-size:150%;text-align:center">{}</p>
                                        
                                    </fieldset>
                                <a href="/">Main page</a>
                                </body>
                                </html>
                                """.format(message)

        elif "/geneInfo" in self.path:
            specie = self.path[self.path.find("=") + 1:]
            gene = self.path[self.path.find("?") + 1:self.path.find("=")] #same as the previous function
            info4 = gene_function(specie)
            message = ''
            if gene != "gene":
                message += "No information available"
                pass
            elif info4 == "0":
                message += "No information available"
            else:
                sequence = info_function(info4)
                task1 = sequence["start"] #finding start, end, length, ID and chromosome
                task2 = sequence["end"]
                task3 = (task2 - task1)+1
                task4 = sequence["id"]
                task5 = sequence["seq_region_name"]
                message += "START: " + str(task1) + "<br>" + "END: " + str(task2) + "<br>" + "LENGTH: " + str(task3) + "<br>" + "ID: " + str(task4) + "<br>" + "CHROMOSOME: " + str(task5)
            content = """
                            <!DOCTYPE html>
                            <html lang="en">
                            <head>
                                <meta charset="UTF-8">
                                <title>Information of gene sequence: </title>
                            </head>
                            <body style="background-color: lightyellow;">
                                <h1 style="color:lightgreen;font-family:arial;font-size:250%;text-align:center"> GENE SEQUENCE INFORMATION </h1>
                                <fieldset>
                                        <p style="color:black;font-family:arial;font-size:150%;text-align:center">{}</p>
                                    </fieldset>
                            <a href="/">Main page</a>
                            </body>
                            </html>
                            """.format(message)

        elif "/geneCalc" in self.path:
            specie = self.path[self.path.find("=") + 1:] #same as the previous
            gene = self.path[self.path.find("?") + 1:self.path.find("=")]
            info4 = gene_function(specie)
            message = ''
            if gene != "gene":
                message += "No information available"
                pass
            elif info4 == "0":
                message += "No information available"
            else:
                sequence = human_sequence(info4)
                sequence = Seq(sequence) #Here I used a class created in one of the practices we did during the course
                total_length = "The total length of the sequence is " + str(sequence.len())
                percA = "The percentage of base A is: " + str(round(sequence.perc("A"), 2)) #perfoming all the calculations and rounding them
                percT = "The percentage of base T is: " + str(round(sequence.perc("T"), 2))
                percG = "The percentage of base G is: " + str(round(sequence.perc("G"), 2))
                percC = "The percentage of base C is: " + str(round(sequence.perc("C"), 2))
                message += str(total_length) + "<br>" + percA + "<br>" + percT + "<br>" + percG + "<br>" + percC + "<br>"
            content = """
                                    <!DOCTYPE html>
                                    <html lang="en">
                                    <head>
                                        <meta charset="UTF-8">
                                        <title>Information of gene sequence: </title>
                                    </head>
                                    <body style="background-color: lightyellow;">
                                        <h1 style="color:lightgreen;font-family:arial;font-size:250%;text-align:center"> GENE SEQUENCE CALCULATIONS</h1>
                                        <fieldset>
                                            <p style="color:black;font-family:arial;font-size:150%;text-align:center">{}</p>
                                        </fieldset>
                                    <a href="/">Main page</a>
                                    </body>
                                    </html>
                                    """.format(message)


        elif "/geneList" in self.path:
            geneList = "" #I had some problems when fixing the erros such as a wrong value, wrong URL, so I had to do it this way
            try:
                values = self.path.lstrip('/geneList').strip('?')
                parameters = values.split('&') #separating values introduced in a list
                chromo = parameters[0].lstrip("chromo=") #finding the actual value of each argument introduced
                start = parameters[1].lstrip("start=")
                end = parameters[2].lstrip("end=")
                chromo1 = parameters[0]
                start1 = parameters[1] #defining each parameters with its value (I did this in order to avoid some problems in case of introducing something incorrect
                end1 = parameters[2]
                hola = list_function(chromo, start, end) #calling function
                if ("chromo" not in chromo1) or ("start" not in start1) or ("end" not in end1):
                    geneList += "No information available"
                else:
                    for i in range(len(hola)):
                        geneList += str(i+1)+".) Gene: " + hola[i]["id"] + ";" #finding the id of each element
                        if "external_name" in hola[i]: #in case it has an external name, printing it out
                            geneList += " The common name is: " + hola[i]["external_name"] + '<br>'
                        else:
                            geneList += '<br>'
            except KeyError:
                pass
            content = """
                                                <!DOCTYPE html>
                                                <html lang="en">
                                                <head>
                                                    <meta charset="UTF-8">
                                                    <title>Information of gene sequence: </title>
                                                </head>
                                                <body style="background-color: lightyellow;">
                                                    <h1 style="color:lightgreen;font-family:arial;font-size:250%;text-align:center"> LIST</h1>
                                                    <fieldset>
                                                        <p style="color:black;font-family:arial;font-size:150%;text-align:center">{}</p>
                                                    </fieldset>
                                                <a href="/">Main page</a>
                                                </body>
                                                </html>
                                                """.format(geneList)




        else:
            f = open('error.html', 'r') #In case of an incorrect endpoint, the user will be directed to this page
            content = f.read()
            f.close()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(str.encode(content)))
        self.end_headers()
        self.wfile.write(str.encode(content))  #sending response message
        return


Handler = TestHandler #my new handler
with socketserver.TCPServer(("", PORT), Handler) as httpd: #opening socket server
    print("Serving at PORT", PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stoped by the user")
        httpd.server_close()