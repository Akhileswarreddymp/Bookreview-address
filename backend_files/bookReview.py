from fastapi import FastAPI,HTTPException
from mongo import *
from models import *
from bson.objectid import ObjectId
import smtplib
from email.message import EmailMessage
from address import router as route

app = FastAPI()
app.include_router(route)

@app.post("/books/addNewBook",tags=["Book"])
async def new_book(request : NewBook):
    try:
        if not isinstance(request,dict):
            data = dict(request)
        else:
            data = request
        collection = await dbconnect('Books','books')
        add_book = collection.insert_one(data)
        return {"msg" : "New Book added Successfully"}
    except Exception as error:
        raise HTTPException(status_code=500, detail="Error While adding the Book")

@app.post("/books/{book_id}/reviews",tags=["Book"])
async def book_review(book_id : str,request : book_reviews):
    if not isinstance(request,dict):
        data = dict(request)
    else:
        data = request
    try:
        filter = {'_id': ObjectId(book_id)}
        collection = await dbconnect('Books','books')
        get_books = collection.find(filter)
        if not get_books:
            raise HTTPException(status_code=404, detail="Book not found")
        review_book = await dbconnect('Books','reviews')
        review_book.insert_one({"book_id": book_id, **data})
        await send_mail(request)
        return {"msg": "Your review submitted successfully"}
    except Exception as e:
        print("Exception raised while rating the book",e)


@app.get("/books/get_book/{auther}",tags=["Book"])
async def sort_books(auther : str):
    collection = await dbconnect('Books','books')
    filter = {'author': auther}
    try:
        get_books = collection.find(filter)
        
        books = []
        for doc in get_books:
            doc['_id'] = str(doc['_id'])
            books.append(doc)
        if not books:
            raise HTTPException(status_code=404,detail="Book not found")
        return books
    except Exception as e:
        print("Exception raised while fetching the book based on author name",e)

@app.put("/books/update_book",tags=["Book"])
async def update_book(request : update_book):
    filter = {'title': request.title}
    try:
        collection = await dbconnect('Books','books')
        get_books = collection.find(filter)
        
        books = []
        for doc in get_books:
            doc['_id'] = str(doc['_id'])
            books.append(doc)
        if not books:
            raise HTTPException(status_code=404,detail="Book not found")
        update_document = {
            '$set': {
                'title': request.title,
                'author' : request.author,
                'published_year' : request.published_year
            }
        }
        update_book = collection.update_one(filter, update_document)
        return {"msg" : "book details updated successfully"}
    except Exception as e:
        print("Exception raised while updating the book")
        raise HTTPException(status_code=500,detail="Unable to update the book")

@app.delete("/books/delete_book",tags=["Book"])
async def delete_book(book_id : str):
    print("delete book function triggred")
    query = {'_id': ObjectId(book_id)}
    try:
        collection = await dbconnect('Books','books')
        get_books = collection.find(query)
        books = []
        for doc in get_books:
            doc['_id'] = str(doc['_id'])
            books.append(doc)
        print(books)
        if not books:
            raise HTTPException(status_code=404,detail="Book not found")
        delete_book = collection.delete_one(query)
        return {"msg" : "Book deleted successfully"}
    except Exception as e:
        print("Exception raised while deleting the book.",e)

@app.post("/send_mail", tags=["OTP"])
async def send_mail(request: review_details):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("akhileswarreddymp@gmail.com", "xodgydwslhywjare")

    message = EmailMessage()
    message["Subject"] = "Review of Your Book"
    message = f"Your Book got 1 new review that is {request.rating} and the review is : {request.text_review}"
    s.subject = "Verification code"

    s.sendmail("akhileswarreddymp@gmail.com","mpakhileswarreddy@gmail.com", message)
    s.quit()
    return {"msg" : "mail Sent Successfully"}




