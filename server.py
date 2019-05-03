import http.client
import json
import socketserver
import http.server
from seq import Seq


PORT = 8000
socketserver.TCPServer.allow_reuse_address = True


HOSTNAME = "rest.ensembl.org"
ENDPOINT1 = "/info/species?content-type=application/json"
ENDPOINT2 = "/info/assembly/"
ENDPOINT4 = "/sequence/id/"
ENDPOINT5 = "/lookup/symbol/homo_sapiens/"
ENDPOINT6 = "/lookup/id/"
ENDPOINT7 = "/overlap/region/human/"
METHOD = "GET"
headers = {'User-Agent': 'http-client'}

def list_species(basic):
    names = []
    for i in basic["species"]:
        names.append(i)
    list1 = []
    for i in range(len(names)):
        list1.append(names[i]["display_name"])

    return list1


def karyotype_function(specie):
    conn = http.client.HTTPSConnection(HOSTNAME)
    conn.request(METHOD, ENDPOINT2 + specie + "?content-type=application/json", None, headers)
    print(ENDPOINT2 + specie + "?content-type=application/json")
    r1 = conn.getresponse()
    print()
    print("Response received: ", end='')
    print(r1.status, r1.reason)
    text_json = r1.read().decode("utf-8")
    karyotype = json.loads(text_json)

    return karyotype


def human_sequence(specie):
    conn = http.client.HTTPSConnection(HOSTNAME)
    conn.request(METHOD, ENDPOINT4 + specie + "?content-type=application/json", None, headers)
    r1 = conn.getresponse()
    print()
    print("Response received: ", end='')
    print(r1.status, r1.reason)
    text_json = r1.read().decode("utf-8")
    human = json.loads(text_json)
    print(human)
    sequence = human['seq']

    return sequence


def gene_function(gene):
    conn = http.client.HTTPSConnection(HOSTNAME)
    conn.request(METHOD, ENDPOINT5 + gene + "?expand=1;content-type=application/json", None, headers)
    r1 = conn.getresponse()
    print()
    print("Response received: ", end='')
    print(r1.status, r1.reason)
    text_json = r1.read().decode("utf-8")
    gen = json.loads(text_json)
    print(gen)
    if 'id' in gen:
        id = gen['id']
    else:
        id = '0'

    return id

def info_function(specie):
    conn = http.client.HTTPSConnection(HOSTNAME)
    conn.request(METHOD, ENDPOINT6 + specie + "?content-type=application/json;expand=1", None, headers)
    r1 = conn.getresponse()
    print()
    print("Response received: ", end='')
    print(r1.status, r1.reason)
    text_json = r1.read().decode("utf-8")
    human = json.loads(text_json)

    return human

def list_function(chromo, start, end):
    conn = http.client.HTTPSConnection(HOSTNAME)
    conn.request(METHOD, ENDPOINT7 + chromo + ":" + start + "-" + end + "?content-type=application/json;feature=gene;feature=transcript;feature=cds;feature=exon;content-type=application/json", None, headers)
    r1 = conn.getresponse()
    print()
    print("Response received: ", end='')
    print(r1.status, r1.reason)
    text_json = r1.read().decode("utf-8")
    list = json.loads(text_json)

    return list



class TestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        print("GET received")
        print("Request line" + self.requestline)
        print("       Cmd:  " + self.command)
        print("Path:  " + self.path)
        if self.path == "/":
            file = open("main.html")
            content = file.read()
            file.close()
        elif "/listSpecies" in self.path:
            conn = http.client.HTTPSConnection(HOSTNAME)
            conn.request(METHOD, ENDPOINT1, None, headers)
            r1 = conn.getresponse()
            print()
            print("Response received: ", end='')
            print(r1.status, r1.reason)
            text_json = r1.read().decode("utf-8")
            basic = json.loads(text_json)
            list1 = list_species(basic)
            listspecies = "LIST OF AVAILABLE SPECIES: " + "\n"
            listspecies2 = " "
            if "limit" in self.path:
                limit = self.path[self.path.find("=") + 1:]
                if limit == '':
                    for i in list1:
                        listspecies2 += "Specie: " + i + "<br>"
                elif limit.isalpha():
                    listspecies2 += "Your limit must be an integer!"
                else:
                    limit = int(limit)
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
                    """.format(listspecies, listspecies2)

        elif "/karyotype" in self.path:
            specie = self.path[self.path.find("=") + 1:]
            specie = specie.replace("+", "")
            specie = specie.upper()
            info2 = karyotype_function(specie)
            chromosomes = ""
            message = specie.upper()
            if "karyotype" in info2:
                list2 = info2["karyotype"]
                for i in range(len(list2)):
                    chromosomes += list2[i] + "\n"
            else:
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
                specie = self.path[self.path.find("=") + 1:self.path.find("&")]
                specie1 = self.path[self.path.find("?")+1:self.path.find("=")]
                msg = ""
                karyotype_json = karyotype_function(specie)
                karyotype = karyotype_json["top_level_region"]
                length = dict()
                for element in range(len(karyotype)):
                    if specie1 != "specie":
                        msg += "Error"
                        pass
                    elif karyotype[element]["coord_system"] == "chromosome":
                        length[karyotype[element]["name"]] = karyotype[element]["length"]
                    else:
                        length[karyotype[element]["name"]] = karyotype[element]["length"]
                num = self.path[self.path.find("o=") + 2:]
                num = num
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
            specie = self.path[self.path.find("=") + 1:]
            specie = specie.lower()
            gene = self.path[self.path.find("?")+1:self.path.find("=")]
            message = ''
            info4 = gene_function(specie)
            if gene != "gene":
                message += "No information available"
                pass
            elif info4 == "0":
                message += "No information available"
            else:
                sequence = human_sequence(info4)
                message += sequence
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
            gene = self.path[self.path.find("?") + 1:self.path.find("=")]
            info4 = gene_function(specie)
            message = ''
            if gene != "gene":
                message += "No information available"
                pass
            elif info4 == "0":
                message += "No information available"
            else:
                sequence = info_function(info4)
                task1 = sequence["start"]
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
            specie = self.path[self.path.find("=") + 1:]
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
                sequence = Seq(sequence)
                total_length = "The total length of the sequence is " + str(sequence.len())
                percA = "The percentage of base A is: " + str(round(sequence.perc("A"), 2))
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
            geneList = ""
            try:
                values = self.path.lstrip('/geneList').strip('?')
                parameters = values.split('&')
                chromo = parameters[0].lstrip("chromo=")
                start = parameters[1].lstrip("start=")
                end = parameters[2].lstrip("end=")
                chromo1 = parameters[0]
                start1 = parameters[1]
                end1 = parameters[2]
                hola = list_function(chromo, start, end)
                if ("chromo" not in chromo1) or ("start" not in start1) or ("end" not in end1):
                    geneList += "No information available"
                else:
                    for i in range(len(hola)):
                        geneList += str(i+1)+".) Gene: " + hola[i]["id"] + ";"
                        if "external_name" in hola[i]:
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
            f = open('error.html', 'r')
            content = f.read()
            f.close()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(str.encode(content)))
        self.end_headers()
        self.wfile.write(str.encode(content))
        return


Handler = TestHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at PORT", PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stoped by the user")
        httpd.server_close()