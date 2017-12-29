#!/usr/bin/env python
# coding: utf-8

# Migrate data from Microsoft Access to MongoDB

#   PRS to persons
# Indice                  1                   uid
# Sexe                    "M"                 gender
# DatNaiss                19670514            dateOfBirth
# N_LieuNaiss             1                   -
# LieuNaiss               "Montbéliard"       placeOfBirth
# N_LieuDécès                                 placeOfDeath
# N_Parents               1                   mother/father
# ConfLienParents         1                   ?
# RéfActeLienParents                          ?
# N_Couple                457                 relationships
# N_Puiné                 110                 -
# N_Nom                   1                   -
# N_Prénom2                                   -
# N_Prénom3                                   -
# N_Prénom1                                   -
# N_Prénom4                                   -
# N_Asc                                       -
# NotePrs                                     notes
# NoteNaiss                                   ?
# NoteDécès                                   ?
# RéfActeNaiss            "25388N19670947"    docs.birthCertificate
# RéfActeDécès                                docs.deathCertificate
# N_Desc                                      ?
# Docs                    "00054"             -
# Nom                     "MOUGIN"            name
# Prenom1                 "Thierry"           firstName
# DatDeces                                    dateOfDeath
# LieuDeces                                   placeOfDeath
# Prenom2                 "Marie"             firstNames
# Prenom3                 "Roger"             firstNames
# Prenom4                                     firstNames
# AgeDeces                                    dateOfDeath
# Hypoth                  "00054"             ?
# DefDoc                                      ?

#   CPL to relationships
# Indice                                      uid
# N_ConjointM                                 spouses
# N_ConjointF                                 spouses
# NbreEnfants                                 childrens
# N_Ainé                                      -
# N_AutreCoupleM                              -
# N_AutreCoupleF                              -
# N_LieuMariage                               -
# NoteCouple                                  notes
# NoteMariage                                 notes
# NbreEnfantsTotal                            -
# RéfActeMariage                              docs.marriageCertificate
# DatMariage                                  dateOfMarriage
# LieuMariage                                 placeOfMarriage
# AgeMariageF                                 -
# AgeMariageM                                 -


import datetime
from pymongo import MongoClient
import csv


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
                row['Prenom1'],
                row['Prenom2'],
                row['Prenom3'],
                row['Prenom4']
            ]
            document['gender'] = row['Sexe']
            document['parents'] = int(row['N_Parents'])
            document['placeOfBirth'] = row['LieuNaiss']
            document['dateOfBirth'] = convertToIsoDate(row['DatNaiss'])
            document['placeOfDeath'] = row['LieuDeces']
            document['dateOfDeath'] = convertToIsoDate(row['DatDeces'])
            document['relationships'] = int(row['N_Couple'])
            document['docs'] = {}
            document['docs']['birthCertificate'] = row['RéfActeNaiss']
            document['docs']['deathCertificate'] = row['RéfActeDécès']
            document['notes'] = {}
            document['notes']['aboutDeath'] = row['NoteDécès']
            document['notes']['aboutBirth'] = row['NoteNaiss']
            document['notes']['about'] = row['NotePrs']

            document['levelOfCertainty'] = {}
            document['levelOfCertainty']['dateOfBirth'] = ''
            document['levelOfCertainty']['placeOfBirth'] = ''
            collection.insert(document)


def convertToIsoDate(date):
    if date != '0':
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
            document['placeOfMarriage'] = row['LieuMariage']
            document['dateOfMarriage'] = convertToIsoDate(row['DatMariage'])
            document['docs'] = {}
            document['docs']['marriageCertificate'] = row['RéfActeMariage']
            document['notes'] = {}
            document['notes']['aboutMarriage'] = row['NoteMariage']
            document['notes']['about'] = row['NoteCouple']
            collection.insert(document)


def addChildrenToRelationships(personsCollection, couplesCollection):
    couples = couplesCollection.find({})
    for couple in couples:
        childrenUids = []
        children = personsCollection.find({'parents': couple['uid']})
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
            {'$set': {'levelOfCertainty.' + key: 'NONE'}}
        )


def openMongoConnection(host, port):
    return MongoClient(host + ':' + str(port))


if __name__ == '__main__':
    connection = openMongoConnection('127.0.0.1', 27017)
    db = connection.test

    ingestPersons('./Hugues_2010.mdb/PRS.csv', db.persons)
    ingestRelationships('./Hugues_2010.mdb/CPL.csv', db.relationships)
    addChildrenToRelationships(db.persons, db.relationships)
    initLevelOfCertainty(db.persons)
    initLevelOfCertainty(db.relationships)
