#!/usr/bin/env python3

import sys
sys.path.append('../common')

import util
import dbcon
from multiprocessing.pool import ThreadPool


class SensitivityBenchmark:

    def __init__(self,
                 sPathToDB="sensitivity_tests.db",
                 sBaseFolder="../data/sensitivity_results/",
                 aHashes=[],
                 lNumberOfThreads=4
                 ):

        # set hash algos
        self.aHashes = aHashes

        # set nr of threads
        self.lNumberOfThreads = lNumberOfThreads

        # create folders if not existent
        self.sBaseFolder = util.create_path(sBaseFolder)

        # create db file if not existent
        self.sPathToDB = self.sBaseFolder + sPathToDB
        open(self.sPathToDB, 'a').close()
        dbData = dbcon.Dbcon(self.sPathToDB)
        sDbSchema = """
            BEGIN TRANSACTION;
            CREATE TABLE IF NOT EXISTS `images_hashes` (
                `image_id`	INTEGER NOT NULL,
                `hash_id`	INTEGER NOT NULL,
                FOREIGN KEY(`hash_id`) REFERENCES `hashes`(`id`) ON UPDATE CASCADE ON DELETE RESTRICT,
                FOREIGN KEY(`image_id`) REFERENCES `images`(`id`) ON UPDATE CASCADE ON DELETE RESTRICT,
                PRIMARY KEY(`image_id`,`hash_id`)
            );
            CREATE TABLE IF NOT EXISTS `images` (
                `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                `name`	TEXT NOT NULL,
                `collection_id`	INTEGER NOT NULL,
                FOREIGN KEY(`collection_id`) REFERENCES `collections`(`id`) ON UPDATE CASCADE ON DELETE RESTRICT
            );
            CREATE TABLE IF NOT EXISTS `hashes` (
                `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                `hash`	NPARRAY NOT NULL,
                `hash_type_id`	TEXT NOT NULL,
                FOREIGN KEY(`hash_type_id`) REFERENCES `hash_types`(`id`) ON UPDATE CASCADE ON DELETE RESTRICT
            );
            CREATE TABLE IF NOT EXISTS `hash_types` (
                `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                `name`	TEXT NOT NULL,
                `params`	TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS `collections` (
                `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                `name`	TEXT NOT NULL UNIQUE
            );
            COMMIT;
        """
        dbData.execute_sql_query_manipulation_script(sDbSchema)

# ----- setter ------
    def set_hashes(self, aHashes):
        """ set hashes list
            use the following structure:
            [
                (hashFn1, {}),
                (hashFn1, {"lHashSize": 512}),
                (hashFn2, {})
            ]
        """
        self.aHashes = aHashes

    def set_nr_of_threads(self, lNumberOfThreads):
        """set the number of threads used to run the test
        """
        self.lNumberOfThreads = lNumberOfThreads

# ----- getter ------
    def get_dbcon(self):
        """ get db connection object"""
        return dbcon.Dbcon(self.sPathToDB)

# ---- private runner --------
    def __hash_single_image(self, sPathToImage, lCollectionId, bAddSave=True):
        """ hash a single image and add it to db"""
        # connect do db
        dbData = self.get_dbcon()

        sImageName = sPathToImage.split("/")[-1]
        aImage = util.load_image(sPathToImage)
        # # if add save mode is enabled, test whether file is existend
        # if bAddSave:

        # add image to db
        lImageId = dbData.execute_sql_query_manipulation(
            "INSERT INTO images (name, collection_id) VALUES (?,?);", (
                sImageName, lCollectionId))

        # process hashing
        for fnHash, dicHashParameters in self.aHashes:
            sHashName = fnHash.__name__
            sHashParameters = str(dicHashParameters)
            tpValues = (sHashName, sHashParameters)

            # hash type handling
            aExistentHashTypes = dbData.execute_sql_query_select(
                "SELECT id FROM hash_types WHERE name=? AND params=?;", tpValues)
            if not aExistentHashTypes:
                lHashTypeId = dbData.execute_sql_query_manipulation(
                    "INSERT INTO hash_types (name, params) VALUES (?, ?);", tpValues)
            else:
                lHashTypeId = aExistentHashTypes[0][0]

            # hash handling
            aHash = fnHash(aImage, **dicHashParameters)
            tpValues = (lHashTypeId, aHash)
            lHashId = dbData.execute_sql_query_manipulation(
                "INSERT INTO hashes (hash_type_id, hash) VALUES (?, ?);", tpValues)

            # add image-hash correlation to db
            dbData.execute_sql_query_manipulation(
                "INSERT INTO images_hashes (image_id, hash_id) VALUES (?, ?);", (lImageId, lHashId))


#------ add imageset to db and hash every image --------

    def hash_imageset(self, sPathToImages):
        """ hash all images of given directory by all hashing algos set
            images with file extension [".png", ".bmp", ".jpg", ".jpeg", ".tiff"]
            are considered
        """
        aImagePathes = util.list_all_images_in_directory(sPathToImages)

        # error handling
        if not aImagePathes:
            raise Exception(
                "given path %s does not contain any images" % sPathToDB)
        if not self.aHashes:
            raise Exception("you forgot to set hashing functions")
        if not self.lNumberOfThreads >= 1:
            raise Exception(
                "the numbers of threads you defined is invalid: %i" % lNumberOfThreads)

        # connect do db
        dbData = self.get_dbcon()

        # get name of collection
        aCollectionName = sPathToImages.split("/")
        sCollectionName = aCollectionName[-1] if aCollectionName[-1] else aCollectionName[-2]

        # Save collection in db if not already existend
        aCollection = dbData.execute_sql_query_select(
            "SELECT id FROM collections WHERE name=?;", (sCollectionName,))
        if not aCollection:
            lCollectionId = dbData.execute_sql_query_manipulation(
                "INSERT INTO collections (name) VALUES (?);", (sCollectionName,))
        else:
            lCollectionId = aCollection[0][0]

        # cerate thread for every image
        oPool = ThreadPool(processes=self.lNumberOfThreads)
        aTaskPoolThreads = []
        for sPathToImage in aImagePathes:
            pThread = oPool.apply_async(
                self.__hash_single_image, (sPathToImage, lCollectionId))
            aTaskPoolThreads.append(pThread)

        # catch threads -- have no returns
        for i in range(len(aImagePathes)):
            aTaskPoolThreads[i].get()
