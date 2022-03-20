##################################-- Bibliothèques --##################################

import requests
from bs4 import BeautifulSoup
import csv
import os

####################################-- Fonctions --####################################

def get_the_categories_of_the_website():
    response = requests.get(web_Site)
    soup = BeautifulSoup(response.content, "html.parser")
    list_all_categories = []
    for get_categories in soup.find("ul", class_="nav nav-list").find_all("a"):
        name_categories = (get_categories.text.strip())
        link_categories = (web_Site + get_categories.get("href").strip())
        list_all_categories.append((name_categories, link_categories))
    return list_all_categories

def get_book_in_the_categories(category_link):
    list_all_books = []
    check_exist = True
    while check_exist:
        response = requests.get(category_link)
        soup = BeautifulSoup(response.content, "html.parser")
        try:
            for book_in_categories in soup.find("ol", class_="row").find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3"):
                title_books = book_in_categories.find_all("img", class_="thumbnail")[0].get("alt")

                search_book_link = book_in_categories.find("div", class_="image_container").find("a").get("href")
                links_books_link = (web_Site + search_book_link).replace("../../..", "catalogue")

                search_cover_book = book_in_categories.find("img", class_="thumbnail").get("src")
                links_cover_books = (web_Site + search_cover_book).replace("/../../../..", "")

                list_all_books.append((title_books, links_books_link, links_cover_books))

            search_next_button = soup.find("li", class_="next").find("a").get("href")

            if search_next_button is not None:
                split_next = category_link.split("/")
                next_link = ("/".join(split_next[0:7])) + "/" + search_next_button
                category_link = next_link
            else:
                check_exist = False
        except:
            check_exist = False
    return list_all_books

def get_information_from_the_books(book_link):
    response = requests.get(book_link)
    soup = BeautifulSoup(response.content, "html.parser")
    information_list_of_books = []
    for tr in soup.find_all("tr"):
        th = tr.find("th").text
        td = tr.find("td").text
        information_list_of_books.append((th + " : " + td + " ,"))
    synopsis = soup.find_all("p")[3].text
    information_list_of_books.append((synopsis))
    return information_list_of_books

############################-- Traitement des fonctions --#############################

web_Site = "https://books.toscrape.com/"
response = requests.get(web_Site)
soup = BeautifulSoup(response.content, "html.parser")
if response.status_code == 200:

    headers_name = ["Name categories", "Links categories",
                    "Title of the book", "Book link", "Cover of the book",
                    "UPC", "product_type", "price_excl_tax", "price_incl_tax", "tax", "available_in_stock", "number_of_review", "synopsis"]

    list_of_categories = get_the_categories_of_the_website()
    for index_categories in list_of_categories:
        categories = index_categories[0]
        if index_categories[0] != "Books":
            name_categories = index_categories[0]
            links_categories = index_categories[1]
            csv_name = ((name_categories + ".csv").replace(" ", "_"))

            folder_csv_file = "./folder_csv_file"
            os.makedirs("folder_csv_file", exist_ok=True)

            csv_name = f"{folder_csv_file}/{csv_name}"

            with open(csv_name, "w", newline="", encoding="utf8") as csv_files:
                csv_writer = csv.writer(csv_files)
                csv_writer.writerow(headers_name)

                list_of_book = get_book_in_the_categories(links_categories)
                for index_book in list_of_book:
                    title_book = index_book[0]
                    link_book = index_book[1]
                    cover_book = index_book[2]

                    list_of_informations = get_information_from_the_books(link_book)
                    for index_information in list_of_informations:
                        UPC = list_of_informations[0]
                        product_type = list_of_informations[1]
                        price_excl_tax = list_of_informations[2]
                        price_incl_tax = list_of_informations[3]
                        tax = list_of_informations[4]
                        available_in_stock = list_of_informations[5]
                        number_of_review = list_of_informations[6]
                        synopsis = list_of_informations[7]

##################-- Écriture des variables dans les fichiers csv --##################

                    csv_writer.writerow([name_categories, links_categories,
                                         title_book, link_book, cover_book,
                                         UPC, product_type, price_excl_tax, price_incl_tax, tax,
                                         available_in_stock, number_of_review, synopsis])

#########-- Téléchargement des images dans le dossier folder_image_of_book --#########

                    folder_image_of_book = "./folder_image_of_book"
                    os.makedirs("folder_image_of_book", exist_ok=True)

                    response = requests.get(cover_book, allow_redirects=True)
                    pictures_file = (str(title_book))
                    pictures_name = ''.join(filter(str.isalnum, pictures_file))

                    pictures_name = f"{folder_image_of_book}/{pictures_name}"
                    with open(pictures_name + ".jpg", "wb") as file:
                        file.write(response.content)