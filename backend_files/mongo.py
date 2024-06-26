from pymongo import MongoClient

mongo_client = None

async def connectdb():
    global mongo_client
    
    if not mongo_client:
        try:
            mongo_client = MongoClient('mongodb://localhost:27017/')
            print("Connected to MongoDB")
        except Exception as e:
            print(f"Error connecting to MongoDB: {str(e)}")

def get_index(index_name):
    if mongo_client:
        return mongo_client[index_name]
    else:
        print("connect to db before connecting to index")

async def dbconnect(index_name,collection_name):
    await connectdb()
    try:
        index_connect = get_index(index_name)
        print("connected to index")
        collection_connect = index_connect[collection_name]
        return collection_connect
    except Exception as e:
        print(f"Error while connecting to db collection {e}")


