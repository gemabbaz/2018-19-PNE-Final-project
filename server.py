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
    conn.request(METHOD, ENDPOINT2+type+"?content-type=application/json", None, headers)
    # -- Print the status
    r1 = conn.getresponse()
    print()
    print("Response received: ", end='')
    print(r1.status, r1.reason)
    text_json = r1.read().decode("utf-8")
    karyotype = json.loads(text_json)
    list2 = karyotype["karyotype"]

    return list2

def chromosome_function(type):
    conn = http.client.HTTPSConnection(HOSTNAME)
    type = input("Introduce the specie you want to know the chromosome length of: ")
    conn.request(METHOD, ENDPOINT3+type+"?content-type=application/json", None, headers)
    # -- Print the status
    r1 = conn.getresponse()
    print()
    print("Response received: ", end='')
    print(r1.status, r1.reason)
    text_json = r1.read().decode("utf-8")
    length = json.loads(text_json)
    list3 = length["top_level_region"]
    list3_names = []
    for i in range(len(list3)):
        list3_names.append(list3[i]["length"])

    return list3_names



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
            if "limit" in self.path:
                limit = self.path[self.path.find("=")+1:]
                if limit == '':
                    listspecies = "List of species available: " + "\n"
                    listspecies2 = " "
                    for i in list1:
                        listspecies2 += "\t" + i + "\n"
                else:
                    limit = int(limit)
                    listspecies = " We'll show " + str(limit) + " out of " + str(len(list1)) + " species"
                    listspecies2 = " "
                    for i in range(limit):
                        listspecies2 += "\t" + list1[i] + "," + "\n"
            else:
                listspecies = "List of available species: " + "\n"
                listspecies2 = " "
                for i in list1:
                    listspecies2 += "\t" + i + "\n"


            file = open("listSpecies.html")
            content = file.read().format(listspecies, listspecies2)
            file.close()

        elif "karyotype" in self.path:
            type = self.path[self.path.find("=")+1:]
            info2 = karyotype_function(type)
            chromosomes = ""
            for i in range(len(info2)):
                chromosomes += info2[i] + "\n"
            message = "The karyotype of this specie is: "

            file = open("karyotype.html")
            content = file.read().format(message, chromosomes)
            file.close()

        elif "chromosomeLength" in self.path:
            type = self.path[self.path.find("=") + 1:]
            info3 = chromosome_function(type)
            chromosomes = ""
            for i in range(len(info3)):
                chromosomes += info3[i] + "\n"
            message = "The length of the chromosome is: "

            file = open("chromsome_length.html")
            content = file.read().format(message, chromosomes)
            file.close()


        self.send_response(200);
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



