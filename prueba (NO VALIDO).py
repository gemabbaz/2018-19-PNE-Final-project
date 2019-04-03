def karyotype_function(ENDPOINT2):
    conn = http.client.HTTPSConnection(HOSTNAME)
    type = input("Introduce the specie you want to know the karyotype of: ")
    conn.request(METHOD, ENDPOINT2+type+"?content-type=application/json", None, headers)
    # -- Print the status
    r1 = conn.getresponse()
    print()
    print("Response received: ", end='')
    print(r1.status, r1.reason)
    text_json = r1.read().decode("utf-8")
    karyotype = json.loads(text_json)
    list2 = karyotype["top_level_region"]
    list2_names = []
    for i in range(len(list2)):
        list2_names.append(list2[i]["name"])

    return list2_names

info2 = karyotype_function(ENDPOINT2)
for i in info2:
    print("\t", i, end = "\n")



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
    for i in list1:
        print("\t", i, end = "\n")

def karyotype_function(ENDPOINT2):
    conn = http.client.HTTPSConnection(HOSTNAME)
    type = input("Introduce the specie you want to know the karyotype of: ")
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

info2 = karyotype_function(ENDPOINT2)
for i in info2:
    print("\t", i, end = "\n")

def chromosome_function(ENDPOINT3):
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

info3 = chromosome_function(ENDPOINT3)
for i in info3:
    print("\t", i, end = "\n")




