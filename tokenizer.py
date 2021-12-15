import pathlib
import xml.etree.ElementTree as ET
import csv


def parse_csv(stoplist):
    fields = []
    rows = []
    dic = {}
    record_num = 0
    with open('reviews.csv', mode='r') as file:
        reader = csv.reader(file)

        # extracting field names through first row
        fields = next(reader)

        # extracting each data row one by one
        for row in reader:
            rows.append(row)

    for row in rows:
        user_name = row[1]
        title = row[2]
        rating = row[3]
        date = row[4]
        review_body = row[5]
        all_words = title + " " + review_body + " " + user_name

        # tokenized_all_words = tokenize(all_words, stoplist)
        dic[record_num] = all_words, user_name, title, rating, date, review_body
        record_num += 1
    return dic


def parse_xml(filename, stoplist):
    root = ET.parse(filename).getroot()
    dic = {}
    for record in root.findall('RECORD'):

        record_num = int(record.findall('RECORDNUM')[0].text)
        title = record.findall('TITLE')
        if len(title) == 0:
            title = ""
        else:
            title = str(title[0].text)

        source = record.findall('SOURCE')
        if len(source) == 0:
            source = ""
        else:
            source = str(source[0].text)

        all_words = ""
        abstract = record.findall('ABSTRACT')
        if len(abstract) == 0:
            abstract = ""
        else:
            abstract = str(abstract[0].text)
        all_words += " " + abstract

        extract = record.findall('EXTRACT')
        if len(extract) == 0:
            extract = ""
        else:
            extract = str(extract[0].text)
        all_words += " " + extract

        majorsubj = record.findall('MAJORSUBJ')
        if len(majorsubj) != 0:
            majorsubj = majorsubj[0]
            for topic in majorsubj.findall('TOPIC'):
                all_words += " " + str(topic.text)

        minorsubj = record.findall('MINORSUBJ')
        if len(minorsubj) != 0:
            minorsubj = minorsubj[0]
            for topic in minorsubj.findall('TOPIC'):
                all_words += " " + str(topic.text)

        authors = record.findall('AUTHORS')
        if len(authors) != 0:
            authors = authors[0]
            for author in authors.findall('AUTHOR'):
                all_words += " " + str(author.text)

        tokenized_all_words = tokenize(all_words, stoplist)
        dic[record_num] = title, all_words, source, tokenized_all_words
    return dic


def tokenize(file, stoplist):
    words = file.strip().split()
    res = []
    for w in words:
        if any(ch.isdigit() for ch in w):
            continue
        removed_w = remove_punctuation(w.lower())
        for r in removed_w:
            if "'" not in r and r not in stoplist:
                res.append(r)
    return res


def remove_punctuation(word):
    res = []
    punctuation = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    word = word.strip(punctuation)
    word = word.replace('/', '-')
    word = word.replace('+', '-')
    word = word.replace(':', '-')
    word = word.replace(';', '-')
    word = word.replace('.', '-')
    word = word.replace('(', '-')
    word = word.replace(')', '-')
    words = word.split('-')
    for word in words:
        if not word:
            continue
        word = word.strip(punctuation)
        res.append(word)
    return res


def token_document():
    stop_words = []
    with open('stoplist.txt') as f:
        lines = f.readlines()
        for line in lines:
            stop_words.append(line)
    inverted_list = parse_csv(stop_words)
    return inverted_list


def parse_query():
    root = ET.parse('cfquery.xml').getroot()
    queries = set()
    for query in root.findall('QUERY'):
        text = str(query.findall('QueryText')[0].text)
        queries.add(text)
    return queries
