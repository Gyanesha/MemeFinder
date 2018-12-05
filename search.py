import nltk
from nltk.corpus import wordnet
import pickle


def generateQuery(query):
    """  Generated extended related queries based on the user query. """
    queryList = (" ".join(("".join((char if char.isalpha() else " ")
                                   for char in query)).split(','))).split()
    keywords = []
    for query in queryList:
        for syn in wordnet.synsets(query):
            for l in syn.lemmas():
                keywords.append(l.name())
    return keywords


def create_index(database):
    """ Creates a dictionary of file name and associated text attribues from the database. """
    db = open(database, 'r')
    INDEX = {}
    db.readline()  # ignoring the column headers
    for entry in db:
        entry = entry.split(',')
        filename = entry[0]
        text = ' '.join(entry[1:])
        text = (" ".join(("".join((char if char.isalpha() else " ")
                                  for char in text)).split(','))).split()
        INDEX[filename] = text
    index_file = open("index.pickle", "wb")
    pickle.dump(INDEX, index_file)
    index_file.close()
    return INDEX


def getScore(INDEX, keywords):
    """ Scores each entry in the database on the basis of its relevance to the keywords. """
    totalEntries = len(INDEX)
    keyList = list(INDEX.keys())
    valueList = list(INDEX.values())
    serialList = list(range(totalEntries))
    scoreList = [0 for i in range(totalEntries)]
    # Assigning score proportional to relevance
    for word in keywords:
        for i in range(totalEntries):
            if word.lower() in [x.lower() for x in valueList[i]]:
                scoreList[i] = scoreList[i] + 1
    score_file = open("score.pickle", "wb")
    pickle.dump(scoreList, score_file)
    score_file.close()

    matched_files = []
    for t in range(len(scoreList)):
        if scoreList[t] > 0:
            matched_files.append(keyList[t])

    while 0 in scoreList:
        scoreList.remove(0)

    matched = {}
    l = len(scoreList)

    for i in range(l):
        matched[matched_files[i]] = scoreList[i]

    import operator
    sorted_list = sorted(matched.items(), key=operator.itemgetter(1))

    # return scoreList, matched_files
    memes = [x[0] for x in sorted_list]
    return memes[::-1]


def load_index(index_name):
    """ Returns an object from given pickle file. """
    index_file = open(index_name, "rb")
    return pickle.load(index_file)

# print(generateQuery(raw_input()))

# print(len(create_index("data3.txt")))

# print(getScore(create_index("data3.txt"), generateQuery('team sucks')))
