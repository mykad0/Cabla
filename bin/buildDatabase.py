#!/usr/bin/env python
# coding: utf-8

# Migrate data from Microsoft Access to MongoDB

import datetime
from pymongo import MongoClient
import csv

EMPTY_DATE = '0'
EMPTY_STRING = ''


def ingestPersons(file, collection):
    collection.remove()
    with open(file, 'rb') as csvFile:
        reader = csv.DictReader(csvFile, delimiter=',')
        for row in reader:
            document = {}
            document['uid'] = int(row['Indice'])
            document['name'] = row['Nom']
            document['firstName'] = row['Prenom1']
            document['firstNames'] = [
                row['Prenom2'],
                row['Prenom3'],
                row['Prenom4']
            ]
            document['gender'] = row['Sexe']
            document['parentRelationship'] = int(row['N_Parents'])

            document['birth'] = {}
            document['birth']['place'] = row['LieuNaiss']
            document['birth']['date'] = convertToDate(row['DatNaiss'])
            document['birth']['docs'] = row['RéfActeNaiss']
            document['birth']['note'] = row['RéfActeDécès']

            if row['N_Couple'] != EMPTY_DATE:
                document['relationships'] = int(row['N_Couple'])

            if row['DatDeces'] != EMPTY_DATE:
                document['death'] = {}
                document['death']['place'] = row['LieuDeces']
                document['death']['date'] = convertToDate(row['DatDeces'])
                document['death']['docs'] = row['RéfActeDécès']
                document['death']['note'] = row['RéfActeDécès']

            if row['NotePrs'] != EMPTY_STRING:
                document['more'] = row['NotePrs']

            collection.insert(document)


def convertToDate(date):
    if date != EMPTY_DATE:
        try:
            return datetime.datetime(
                int(date[0:4]),
                int(date[4:6]),
                int(date[6:8])
            )
        except ValueError:
            return datetime.datetime(int(date[0:4]), 1, 1)


def ingestRelationships(file, collection):
    collection.remove()
    with open(file, 'rb') as csvFile:
        reader = csv.DictReader(csvFile, delimiter=',')
        for row in reader:
            document = {}
            document['uid'] = int(row['Indice'])
            document['spouses'] = [
                int(row['N_ConjointF']),
                int(row['N_ConjointM'])
            ]

            if row['DatMariage'] != EMPTY_DATE:
                document['marriage'] = {}
                document['marriage']['place'] = row['LieuMariage']
                document['marriage']['date'] = convertToDate(row['DatMariage'])
                document['marriage']['docs'] = row['RéfActeMariage']
                document['marriage']['notes'] = row['NoteMariage']

            if row['NoteCouple'] != EMPTY_STRING:
                document['more'] = row['NoteCouple']

            collection.insert(document)


def addChildrenToRelationships(personsCollection, couplesCollection):
    couples = couplesCollection.find({}, {'uid': 1, '_id': 0})
    for couple in couples:
        childrenUids = []
        children = personsCollection.find(
            {'parentRelationship': couple['uid']}
        )
        for child in children:
            childrenUids.append(child['uid'])
        couplesCollection.update_one(
            {'uid': couple['uid']},
            {'$set': {'children': childrenUids}}
        )


def initLevelOfCertainty(collection):
    sample = collection.find_one({}, {'_id': 0})
    keys = sample.keys()
    for key in keys:
        collection.update_many(
            {},
            {'$set': {'certainty.' + key: 'NA'}}
        )


def openMongoConnection(host, port):
    return MongoClient(host + ':' + str(port))


if __name__ == '__main__':
    connection = openMongoConnection('127.0.0.1', 27017)
    db = connection.test

    ingestPersons('./PRS.csv', db.persons)
    ingestRelationships('./CPL.csv', db.relationships)
    addChildrenToRelationships(db.persons, db.relationships)
    # initLevelOfCertainty(db.persons)
    # initLevelOfCertainty(db.relationships)
