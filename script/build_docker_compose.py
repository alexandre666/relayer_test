#!/usr/bin/env python3

import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
            exit("use: python3 build_docker_compose.py <nombre de noeud>")

    cantons = ("zurich", "berne", "lucerne", "uri", "schwyz", "obwald", "nidwald", "glaris",
               "zoug", "fribourg", "soleure", "bale-ville", "bale-campagne", "schaffhouse", 
               "appenzellrhext", "appenzellrhint", "saint-gall", "grisons", "argovie",
               "thurgovie", "tessin", "vaud", "valais", "neuchatel", "geneve", "jura")
    
    probability_cantons = (0.179290419930871, 0.119915325542664, 0.048178422777298, 0.004226026036976,
                          0.018816766354218, 0.004420079442945, 0.005044222368877, 0.004707894230165,
                          0.014889867111901, 0.037774991110745, 0.032203302663022, 0.022320223338677,
                          0.033673280536968, 0.009625352144541, 0.006380555288952, 0.001874994387728,
                          0.059663142412693, 0.023130956078041, 0.081034906405967, 0.03293555106211,
                          0.040400543023005, 0.093998700168712, 0.040415586826713, 0.020213857582293,
                          0.056385459102487, 0.008479574071433
)

    ports = 26000
    ip = "192.168.10.2"
    id = 2 
    file = open("../ltacker_x/supplychainx/docker-compose.yml", "w")
    identifiant = 1

    #build heading
    file.write("version: '3.3'"+"\n")
    file.write("services:"+"\n")

    #build validators
    for canton in cantons:
        file.write("  "+ canton +":"+"\n")
        file.write("    build:"+"\n")
        file.write("      context: ."+"\n")
        file.write("      dockerfile: test_validator.Dockerfile"+"\n")
        file.write("    ports:"+"\n")
        file.write("      - "+ "\""+ str(ports)+ ":" + str(ports) +"\""+"\n")

        ports = ports + 1

        file.write("    networks:"+"\n")
        file.write("      localnet:"+"\n")
        file.write("        ipv4_address: " + ip +"\n")

        id = id + 1
        ip = "192.168.10." + str(id)

        file.write("    environment:"+"\n")
        file.write("      - MONIKER=validator"+"\n")

    #build nodes
    for index in range(len(cantons)):
        probability = int(sys.argv[1]) * probability_cantons[index]
        print(int(probability))
        while int(probability) > 0:
            file.write("  menage"+ str(identifiant) +":"+"\n")
            identifiant = identifiant + 1
            file.write("    build:"+"\n")
            file.write("      context: ."+"\n")
            file.write("      dockerfile: test.Dockerfile"+"\n")
            file.write("    depends_on:"+"\n")
            file.write("      - "+cantons[index]+"\n")
            ports = ports + 1

            file.write("    networks:"+"\n")
            file.write("      localnet:"+"\n")
            file.write("        ipv4_address: " + ip +"\n")

            id = id + 1
            ip = "192.168.10." + str(id)

            file.write("    environment:"+"\n")
            file.write("      - MONIKER=test"+"\n")
            probability = probability - 1

    #build network
    file.write("networks:"+"\n")
    file.write("  localnet:"+"\n")
    file.write("    driver: bridge"+"\n")
    file.write("    ipam:"+"\n")
    file.write("      driver: default"+"\n")
    file.write("      config:"+"\n")
    file.write("      -"+"\n")
    file.write("        subnet: 192.168.10.0/16" +"\n")

    file.close()
