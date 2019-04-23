import http.client
import json
import socketserver
import http.server

# Define the Server's port
PORT = 8000
socketserver.TCPServer.allow_reuse_address = True

# -- API information
HOSTNAME = "rest.ensembl.org"
ENDPOINT1 = "/info/species?content-type=application/json"
ENDPOINT2 = "/info/assembly/"
ENDPOINT3 = "/info/assembly/"
ENDPOINT4 = "/sequence/id/"
ENDPOINT5 = "/lookup/symbol/homo_sapiens/"


METHOD = "GET"

# -- Here we can define special headers if needed
headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection(HOSTNAME)
conn.request(METHOD, ENDPOINT1, None, headers)
# -- Print the status
r1 = conn.getresponse()
print()
print("Response received: ", end='')
print(r1.status, r1.reason)
text_json = r1.read().decode("utf-8")
basic = json.loads(text_json)

if 'species' in ENDPOINT1:
    names = []
    for i in basic["species"]:
        names.append(i)
    list1 = []
    for i in range(len(names)):
        list1.append(names[i]["display_name"])


def karyotype_function(type):
    conn = http.client.HTTPSConnection(HOSTNAME)
    conn.request(METHOD, ENDPOINT2 + type + "?content-type=application/json", None, headers)
    # -- Print the status
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
    # -- Print the status
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
    # -- Print the status
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
        elif "listSpecies" in self.path:
            listspecies = "List of species available: " + "\n"
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
                        listspecies += "Your limit must be an integer between 0 and " + str(len(list1))
                        listspecies2 += "Try again"
                    else:
                        listspecies = " We'll show " + str(limit) + " out of " + str(len(list1)) + " species"
                        listspecies2 = " "
                        for i in range(limit):
                            listspecies2 += "Specie nº " + str(i + 1) + ": " + list1[i] + "<br>"
            else:
                listspecies = "Available species: " + "\n"
                listspecies2 = " "
                for i in list1:
                    listspecies2 += "\t" + i + "\n"
            content = """
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <title>Information of species: </title>
                    </head>
                    <body style="background-color: lightgreen;">
                        <h1>{}</h1>
                        <h2>{}</h2>

                    <a href="/">Main page</a>
                    </body>
                    </html>
                    """.format(listspecies, listspecies2)

        elif "karyotype" in self.path:
            type = self.path[self.path.find("=") + 1:]
            type = type.replace("+", "")
            info2 = karyotype_function(type)
            chromosomes = ""
            message = type.upper()
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
                    <body style="background-color: lightgreen;">
                        <h1>{}</h1>
                        <h2>{}</h2>

                    <a href="/">Main page</a>
                    </body>
                    </html>
                    """.format(message, chromosomes)

        elif "chromosomeLength" in self.path:
            type = self.path[self.path.find("=") + 1:self.path.find("&")]
            length = karyotype_function(type)
            message = type.upper()
            if "top_level_region" in length:
                list3 = length["top_level_region"]
                list3_names = []
                for i in range(len(list3)):
                    list3_names.append(list3[i]["length"])
                num = int(self.path[self.path.find("o=") + 2:])
                length1 = list3_names[num - 1]
                msg = str(length1)
                print(msg)
            else:
                msg = "There is not available information for " + type


            content = """
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <title>Information of chromosome's length: </title>
                    </head>
                    <body style="background-color: lightgreen;">
                        <h1>CHROMOSOME LENGTH</h1>
                        
                        <fieldset>
                            <legend>{}</legend>
                            <p>{}</p>
                        </fieldset>


                    <a href="/">Main page</a>
                    </body>
                    </html>
                    """.format(message, msg)

        elif "geneSeq" in self.path:
            specie = self.path[self.path.find("=") + 1:]
            print(specie)
            info4 = gene_function(specie)
            print(info4)
            if info4 == 0:
                message = "No information available"
            else:
                sequence = human_sequence(info4) #info4 is your sequence
                message = "Sequence for that gene: " + sequence
            content = """
                                <!DOCTYPE html>
                                <html lang="en">
                                <head>
                                    <meta charset="UTF-8">
                                    <title>Information of gene sequence: </title>
                                </head>
                                <body style="background-color: lightgreen;">
                                    <h1>GENE SEQUENCE</h1>
                                    <h2>{}</h2>

                                <a href="/">Main page</a>
                                </body>
                                </html>
                                """.format(message)


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

    # -- Main loop: Attend the client. Whenever there is a new
    # -- clint, the handler is called
    try:

        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stoped by the user")
        httpd.server_close()