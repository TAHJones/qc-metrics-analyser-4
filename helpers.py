import os
# from os import path
# if path.exists("env.py"):
#     import env
from flask import Flask, render_template, redirect, request, url_for, flash, session, json
from flask_pymongo import PyMongo
# from datetime import datetime
# from helpers import Helpers

class Helpers:
    """ Mongodb query that counts the number incidences of each catergory for a given data type for a selected user or for all users if no user parameter is given.
    Data types can either be 'experiment' or 'chemistry'. 
    For the data type 'experiment' catergories are 'Genome', 'Exome' or 'Capture'.
    For the data type 'chemistry' catergories are 'Mid300', 'Mid150' or 'High300'. """
    @staticmethod
    def getDataCount(database, dataType, dataCatergory, user="N/A"):
        if user == "N/A":
            databaseQuery = [
                {
                    '$match': {
                        dataType: dataCatergory
                    }
                },
                {
                    '$group': {
                        '_id': 'null',
                        'count': { '$sum': 1 },
                    }
                }
            ]
        else:
            databaseQuery = [
            {
                '$match': {
                    '$and': [ {'user': user}, {dataType: dataCatergory} ]
                }
            },
            {
                '$group': {
                    '_id': 'null',
                    'count': { '$sum': 1 },
                }
            }
            ]
        if databaseQuery == []:
            databaseQuery = [{'count': 0}]
        return list(database.aggregate(databaseQuery))


    """ Mongodb query that gets the min, max & average values for data that matchs the parameter 'param'.
    The query can be for a selected user or for all users if no user parameter is given.
    'param' parameter should be 'yields', 'clusterDensity', 'passFilter' or 'q30'. """
    @staticmethod
    def getDataSummary(database, param, user="N/A"):
        dollarParam = "${}".format(param)
        if user == "N/A":
            databaseQuery = [
            {
                '$match': {
                    'user': {'$exists': 'true'}
                }
            },
            {
                '$group': {
                    '_id': 'null',
                    'count': { '$sum': 1 },
                    'average': {'$avg': dollarParam},
                    'minimum': {'$min': dollarParam},
                    'maximum': {'$max': dollarParam}
                }
            }]
        else:
            databaseQuery = [
            {
                '$match': {
                    'user': user
                }
            },
            {
                '$group': {
                    '_id': 'null',
                    'count': { '$sum': 1 },
                    'average': {'$avg': dollarParam},
                    'minimum': {'$min': dollarParam},
                    'maximum': {'$max': dollarParam}
                }
            }]
        return list(database.aggregate(databaseQuery))


    """ Take nested list of experiment types & catergory names & uses a nested loop to feed them into getDataCount function.
    Takes the mongodb connect string as a parameter & user as an optional parameter which are passed to the getDataCount function.
    Returns a dict object containing the number for each catergory for each experiment type """
    @staticmethod
    def getExperimentData(database, user="N/A"):
        experiments = {"experiment": ("Genome", "Exome", "Capture"), "chemistry": ("Mid300", "Mid150", "High300")}
        experimentData = {}
        for experiment in experiments:
            for catergory in experiments[experiment]:
                if user == "N/A":
                    catergoryValue = Helpers.getDataCount(database, experiment, catergory)[0]['count']
                else:
                    catergoryValue = Helpers.getDataCount(database, experiment, catergory, user)[0]['count']
                catergoryDict = {catergory.lower():catergoryValue}
                experimentData.update(catergoryDict)
        return experimentData


    """ Take dict list of qc metrics types & uses a loop to feed them into getDataSummary function.
    Takes the mongodb connect string as a parameter & user as an optional parameter which are passed to the getDataSummary function.
    Returns a dict object containing the min, max & avg values for each qc metrics type """
    @staticmethod
    def getRunData(database, user="N/A"):
        metrics = ("yield", "clusterDensity", "passFilter", "q30")
        metricsData = {}
        for metric in metrics:
            if user == "N/A":
                metricValue = Helpers.getDataSummary(database, metric)
            else:
                metricValue = Helpers.getDataSummary(database, metric, user)
            if metric == "yield":
                metric = "yields"
            metricDict = {metric:metricValue}
            metricsData.update(metricDict)
        return metricsData


    """ Takes dict object from getExperimentData & getRunData functions, joins them together then adds them to qcData dict.
    Takes the mongodb connect string as a parameter which is passed to the getExperimentData & getRunData functions.
    Returns a dict object containing all the qc data generated by the getExperimentData & getRunData functions. """
    @staticmethod
    def getQCData(database):
        qcData = {}
        experimentData = Helpers.getExperimentData(database)
        runData = Helpers.getRunData(database)
        experimentData.update(runData)
        qcData = experimentData
        return qcData
