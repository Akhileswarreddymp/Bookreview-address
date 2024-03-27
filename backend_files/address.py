from fastapi import APIRouter,HTTPException
from models import *
from mongo import *
from bson.objectid import ObjectId

router = APIRouter(prefix="/address")

@router.post("/create_address",tags=["Address"])
async def add_address(request : address):
    try:
        if not isinstance(request,dict):
            data = dict(request)
        else:
            data = request
        collection = await dbconnect('Address','adress')
        add_address = collection.insert_one(data)
        return {"msg" : "Address added Successfully"}
    except Exception as error:
        raise HTTPException(status_code=500, detail="Error While adding the Address")

@router.put("/update_address",tags=["Address"])
async def update_address(request : address):
    filter = {'name': request.name}
    try:
        collection = await dbconnect('Address','adress')
        get_address = collection.find(filter)
        
        address = []
        for doc in get_address:
            doc['_id'] = str(doc['_id'])
            address.append(doc)
        if not address:
            print("Entred into if block")
            raise HTTPException(status_code=404,detail="address not found")
        update_document = {
            '$set': {
                'name': request.name,
                'latitude' : request.latitude,
                'longitude' : request.longitude
            }
        }
        
        update_address = collection.update_one(filter, update_document)
        return {"msg" : "address details updated successfully"}
    except Exception as e:
        print("Exception raised while updating the address")
        raise HTTPException(status_code=500,detail="Unable to update the address")
    
@router.get("get_address/{name}",tags=["Address"])
async def sort_address(name : str):
    collection = await dbconnect('Address','adress')
    filter = {'name': name}
    try:
        get_address = collection.find(filter)
        
        address = []
        for doc in get_address:
            doc['_id'] = str(doc['_id'])
            address.append(doc)
        if not address:
            raise HTTPException(status_code=404,detail="address not found")
        return address
    except Exception as e:
        print("Exception raised while fetching the address based on name",e)

@router.delete("/delete_address",tags=["Address"])
async def delete_address(address_id : str):
    print("delete address function triggred")
    query = {'_id': ObjectId(address_id)}
    try:
        collection = await dbconnect('Address','adress')
        get_address = collection.find(query)
        address = []
        for doc in get_address:
            doc['_id'] = str(doc['_id'])
            address.append(doc)
        print(address)
        if not address:
            raise HTTPException(status_code=404,detail="address not found")
        delete_address = collection.delete_one(query)
        return {"msg" : "address deleted successfully"}
    except Exception as e:
        print("Exception raised while deleting the address.",e)

@router.get("/get_address/{latitude}/{longitude}",tags=["Address"])
async def sort_address(longitude : float,latitude:float):
    collection = await dbconnect('Address','adress')
    filter = {"longitude": {"$lte": latitude}, "latitude": {"$gte": longitude}}
    try:
        get_address = collection.find(filter)
        
        address = []
        for doc in get_address:
            doc['_id'] = str(doc['_id'])
            address.append(doc)
        if not address:
            raise HTTPException(status_code=404,detail="address not found")
        return address
    except Exception as e:
        print("Exception raised while fetching the address based on name",e)
