def mongo_connect(address,db,collection):

    from pymongo import MongoClient

    mongoclient = MongoClient(address) #mongo접속
    db_local = mongoclient[db]   #database 연결
    insert_collection = db_local[collection]

    return insert_collection