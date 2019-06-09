import json

with open("Data/SelectorList.json", 'r') as Selector_json:
    Selector_data = json.load(Selector_json)

with open("Data/WordData.json", 'r') as Word_json:
    Word_data = json.load(Word_json)

with open("Data/adverbs.txt", 'r') as Adverb:
    advlist = Adverb.readlines()

with open("Data/adjectives.txt", 'r') as Adj:
    adjlist = Adj.readlines()

with open("Data/nouns.txt", 'r') as Noun:
    nounlist = Noun.readlines()

headers = {'User-Agent': 'Chrome/66.0.3359.181'}

dicdata = {}

c_advlist = []
c_adjlist = []
c_nounlist = []

count = 4000

for e in advlist:
    c_advlist.append(e.strip('\n'))

for e in adjlist:
    c_adjlist.append(e.strip('\n'))

for e in nounlist:
    c_nounlist.append(e.strip('\n'))


li = list(Word_data.keys())

for game in li[4000:]:
    oplistr = Word_data[game]["Opencritic"]
    melistr = Word_data[game]["Metacritic"]
    ignlistr = Word_data[game]["IGN"]

    dicdata[game] = {"Opencritic": [], "Metacritic": [], "IGN": []}

    if (oplistr is not None):
        if (type(oplistr) is list):
            opli = oplistr[:]
        else:
            opli = oplistr.split(', ')
            opli[0] = opli[0][1:]
            opli[-1] = opli[0][1:]

        for word in opli:
            if ((word in c_advlist) or (word in c_adjlist) or (word in c_nounlist)):
                print("{0} is 1 / {1}".format(word, count))

                with open("Debug_Analyzed_5.txt", 'a') as Data:
                    Data.write("{} / {} / {} / {} \n".format(game, "Opencritic", word, 1))

            else:
                opli.remove(word)

                with open("Debug_Analyzed_5.txt", 'a') as Data:
                    Data.write("{} / {} / {} / {} \n".format(game, "Opencritic", word, 0))

        dicdata[game]["Opencritic"].extend(opli)

    if (melistr is not None):
        if (type(melistr) is list):
            meli = melistr[:]
        else:
            meli = melistr.split(', ')
            meli[0] = meli[0][1:]
            meli[-1] = meli[0][1:]

        for word in meli:
            if ((word in c_advlist) or (word in c_adjlist) or (word in c_nounlist)):
                print("{0} is 1 / {1}".format(word, count))

                with open("Debug_Analyzed_5.txt", 'a') as Data:
                    Data.write("{} / {} / {} / {} \n".format(game, "Metacritic", word, 1))
            else:
                meli.remove(word)

                with open("Debug_Analyzed_5.txt", 'a') as Data:
                    Data.write("{} / {} / {} / {} \n".format(game, "Metacritic", word, 0))

        dicdata[game]["Metacritic"].extend(meli)

    if (ignlistr is not None):
        if (type(ignlistr) is list):
            ignli = ignlistr[:]
        else:
            ignli = ignlistr.split(', ')
            ignli[0] = ignli[0][1:]
            ignli[-1] = ignli[0][1:]

        for word in ignli:
            if ((word in c_advlist) or (word in c_adjlist) or (word in c_nounlist)):
                print("{0} is 1 / {1}".format(word, count))

                with open("Debug_Analyzed_5.txt", 'a') as Data:
                    Data.write("{} / {} / {} / {} \n".format(game, "IGN", word, 1))
            else:
                ignli.remove(word)

                with open("Debug_Analyzed_5.txt", 'a') as Data:
                    Data.write("{} / {} / {} / {} \n".format(game, "IGN", word, 0))

        dicdata[game]["IGN"].extend(ignli)

    count += 1

with open("Data/AnalyzedWordData_5.json", 'w') as output_json:
    output_json.write(json.dumps(dicdata))