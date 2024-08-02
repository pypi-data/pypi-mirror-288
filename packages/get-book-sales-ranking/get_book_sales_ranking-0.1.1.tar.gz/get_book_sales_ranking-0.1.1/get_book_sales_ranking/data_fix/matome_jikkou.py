import asyncio

from get_book_sales_ranking.api.google_api import get_book_data_google
from get_book_sales_ranking.api.sru_api import get_book_data_sru
from get_book_sales_ranking.api.opendb_api import get_book_data_opendb
from get_book_sales_ranking.api.opensearch_api import get_book_data_opensearch


# 実行部分の関数
async def jikkou(isbn):
    google_fetched = get_book_data_google(isbn)
    sru_fetched = get_book_data_sru(isbn)
    opendb_fetched = get_book_data_opendb(isbn)
    opensearch_fetched = get_book_data_opensearch(isbn)

    results = await asyncio.gather(
      google_fetched, 
      sru_fetched, 
      opendb_fetched, 
      opensearch_fetched
    )

    google_fetched_data, sru_fetched_data, opendb_fetched_data, opensearch_fetched_data = results

    google_fetch = google_fetched_data['google_data']
    sru_fetch = sru_fetched_data['sru_data']
    opendb_fetch = opendb_fetched_data['opendb_data']
    opensearch_fetch = opensearch_fetched_data['opensearch_data']

    print(f"google_fetch: {google_fetch}, sru_fetch: {sru_fetch}, opendb: {opendb_fetch}, opensearch: {opensearch_fetch}")



    if google_fetch == True:
      # google_ok+sru_ok
      if sru_fetched_data['sru_data'] == True:
          print("google+sru")
          return {
              "isbn": isbn,
              "caption": google_fetched_data['description'],
              "publishedDate": google_fetched_data['publishedDate'],
              "publisher": sru_fetched_data['publisher'],
              "price": sru_fetched_data['price'],
              "page_count": sru_fetched_data['page_count'],
          }

      if opendb_fetch and opendb_fetched_data['price'] == "" and (sru_fetch or opensearch_fetch):
        if sru_fetch == True:
          print("google+opendb[price==""] [sru]")
          price = sru_fetched_data['price']
          page_count = sru_fetched_data['page_count']
        elif sru_fetch == False and opensearch_fetch == True:
          print("google+opendb[price==""] [opensearch]")
          price = opensearch_fetched_data['price']
          page_count = opensearch_fetched_data['page_count']
        else:
          print("google+opendb[price==""] [opendb]")
          price = opendb_fetched_data['price']
          page_count = opendb_fetched_data['page_count']

        return {
            "isbn": isbn,
            "caption": google_fetched_data['description'],
            "publishedDate": google_fetched_data['publishedDate'],
            "publisher": opendb_fetched_data['publisher'],
            "price": price,
            "page_count": page_count,
        }

      if opendb_fetch == True and opendb_fetched_data['price'] != "":
        if sru_fetch == True:
          print("google+opendb[price!=""] [sru]")
          page_count = sru_fetched_data['page_count']
        else:
          print("google+opendb[price!=""] [opendb]")
          page_count = opendb_fetched_data['page_count']
        return {
            "isbn": isbn,
            "caption": google_fetched_data['description'],
            "publishedDate": google_fetched_data['publishedDate'],
            "publisher": opendb_fetched_data['publisher'],
            "price": opendb_fetched_data['price'],
            "page_count": page_count,
        }


      if opensearch_fetch == True and opensearch_fetched_data['price'] == "" and (sru_fetch == True or opendb_fetch == True):
        if sru_fetch == True:
          print("google+opensearch[price==""] [sru]")
          price = sru_fetched_data['price']
          page_count = sru_fetched_data['page_count']
        else:
          print("google+opensearch[price==""] [opendb]")
          price = opendb_fetched_data['price']
          page_count = opendb_fetched_data['page_count']

        return {
            "isbn": isbn,
            "caption": google_fetched_data['description'],
            "publishedDate": google_fetched_data['publishedDate'],
            "publisher": opensearch_fetched_data['publisher'],
            "price": price,
            "page_count": page_count,
        }

      if opensearch_fetch == True and opensearch_fetched_data['price'] != "":
        print("google+opensearch[price!='']")
        return {
            "isbn": isbn,
            "caption": google_fetched_data['description'],
            "publishedDate": google_fetched_data['publishedDate'],
            "publisher": opensearch_fetched_data['publisher'],
            "price": opensearch_fetched_data['price'],
            "page_count": opensearch_fetched_data['page_count'],
        }

      # googleがokで他はダメな場合が抜けてた 2024/7/28
      if opendb_fetch == False and opensearch_fetch == False and sru_fetch == False:
        print("google only")
        return {
            "isbn": isbn,
            "caption": google_fetched_data['description'],
            "publishedDate": google_fetched_data['publishedDate'],
            "publisher": google_fetched_data['publisher'],
            "price": google_fetched_data['price'],
            "page_count": google_fetched_data['page_count'],
        }


    elif google_fetch == False:
      if sru_fetched_data['sru_data'] == True:
          print("sru")
          return {
              "isbn": isbn,
              "caption": "",
              "publishedDate": sru_fetched_data['sales_date'],
              "publisher": sru_fetched_data['publisher'],
              "price": sru_fetched_data['price'],
              "page_count": sru_fetched_data['page_count'],
          }

      if opendb_fetch == True:
        print("opendb")
        return {
            "isbn": isbn,
            "caption": "",
            "publishedDate": opendb_fetched_data['sales_date'],
            "publisher": opendb_fetched_data['publisher'],
            "price": opendb_fetched_data['price'],
            "page_count": opendb_fetched_data['page_count'],
        }

      if opensearch_fetch == True:
        print("opensearch == True")
        return {
            "isbn": isbn,
            "caption": "",
            "publishedDate": opensearch_fetched_data['sales_date'],
            "publisher": opensearch_fetched_data['publisher'],
            "price": opensearch_fetched_data['price'],
            "page_count": opensearch_fetched_data['page_count'],
        }


      if opensearch_fetch == True and opensearch_fetched_data['price'] == "" and (sru_fetch == True or opendb_fetch == True):
        if sru_fetch == True:
          print("opensearch+sru[price==''] [sru]")
          price = sru_fetched_data['price']
          page_count = sru_fetched_data['page_count']
        else:
          print("opensearch+opendb[price==''] [opendb]")
          price = opendb_fetched_data['price']
          page_count = opendb_fetched_data['page_count']

        return {
            "isbn": isbn,
            "caption": "",
            "publishedDate": opensearch_fetched_data['sales_date'],
            "publisher": opensearch_fetched_data['publisher'],
            "price": price,
            "page_count": page_count,
        }

      if opensearch_fetch == True and opensearch_fetched_data['price'] != "":
        print("opensearch[price!='']")
        return {
            "isbn": isbn,
            "caption": "",
            "publishedDate": opensearch_fetched_data['sales_date'],
            "publisher": opensearch_fetched_data['publisher'],
            "price": opensearch_fetched_data['price'],
            "page_count": opensearch_fetched_data['page_count'],
        }


    else:
      print("else")
      return {
          "isbn": isbn,
          "caption": "",
          "publishedDate": "",
          "publisher": "",
          "price": 0,
          "page_count": "",
      }