import json
from datetime import datetime

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from my_api.models import Author, Book


@csrf_exempt
def create_book(request):
    try:
        if request.method == "POST":
            req_data = request.body.decode('utf-8')
            data = json.loads(req_data)
            name = data.get('author_name')
            city = data.get('city')
            book_name = data.get('book_name')
            description = data.get('description')

            add_author = Author(name=name, city=city)
            add_author.save()

            add_book = Book(book_name=book_name, description=description, author=add_author,
                            created_date=datetime.today())
            add_book.save()

            return JsonResponse({
                "message": "data created succefully"
            })

        else:
            return JsonResponse({"message": "data not created"})

    except Exception as e:
        return JsonResponse(
            {
                "error accured": e
            }
        )


@csrf_exempt
def get_details(request):
    name = request.GET.get('name')
    data_list = []
    try:
        if request.method == 'GET':
            if name:
                data = Author.objects.filter(name=name)
                if data:
                    for value in data:
                        data_list.append(
                            {
                                "name": value.name,
                                "city": value.city
                            }
                        )

                    return JsonResponse(data_list)

                if not data:
                    book_data = Book.objects.filter(book_name=name)
                    if book_data:
                        for val in book_data:
                            data_list.append(
                                {
                                    "Book_Name": val.book_name,
                                    "Description": val.description,
                                    "Author": val.author.id,
                                    "Created_at": val.created_date,
                                    "book_id": val.id

                                }
                            )

                        return JsonResponse(data_list)

                    else:
                        return JsonResponse(
                            {
                                "message": "data not found"
                            }
                        )



            else:
                books_data = Book.objects.all()
                if books_data:
                    for val in books_data:
                        data_list.append(
                            {
                                "Book_Name": val.book_name,
                                "Description": val.description,
                                "Author": val.author.id,
                                "Created_at": val.created_date,
                                "book_id": val.id
                            }
                        )

                    return JsonResponse(data_list)

                else:
                    return JsonResponse(
                        {
                            "message": "no books data available"
                        }
                    )


    except Exception as e:
        return JsonResponse(
            {
                "message": "something went wrong"
            }
        )


@csrf_exempt
def update_book(request):
    if request.method == 'PATCH':
        req_data = request.body.decode('utf-8')
        data = json.loads(req_data)
        book_name = data.get('book_name')
        author_id = data.get('author_id')

        book = Book.objects.get(book_name=book_name, author=author_id)
        if book:
            book.book_name = data.get('book_update')
            book.description = data.get('book_description')
            book.save()
            return JsonResponse(
                {
                    "message": book.book_name
                }
            )
        else:
            JsonResponse(
                {
                    "message": "not updated"
                }
            )
        # return JsonResponse({"book_name": book_name, "author_id": author_id})


@csrf_exempt
def delet_by_id(request):
    id = request.GET.get('id')

    if request.method == 'DELETE':
        if id:
            req_data = Book.objects.get(id=id)
            if req_data:
                req_data.delete()
                return JsonResponse(
                    {
                        "MESSAGE": "RECORD DELETED SUCCEFULLY"
                    }
                )
            else:
                return JsonResponse(
                    {
                        "message": "book data not find"
                    }
                )
        else:
            return JsonResponse(
                {
                    "message": "please enter id"
                }
            )
