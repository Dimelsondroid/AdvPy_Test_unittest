documents = [
    {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
    {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
    {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"},
    {"type": "insurance", "number": "12-4", "name": "Ипполит Павлов"},
    {"type": "invoice", "number": "123", "name": "Геннадий Завывакин"},
]

directories = {
    '1': ['2207 876234', '11-2', '5455 028765'],
    '2': ['10006', '098765'],
    '3': ['12-4'],
    '4': []
}


### Optional function to use before the inputs for tips\outputs
def ref_listing(type=None):
    if type == "doc":
        print("All documents on shelves for reference:")
        list_shelves()
    else:
        print("Shelves content for reference:")
        list_shelves()


### Input document number and get owner name - 'p'
def person_by_number(docs=documents, doc_num=None):
    while True:
        ref_listing("doc")
        # doc_num = input("Input document number for search or 'q' to quit: ")
        if doc_num == "q":
            return
        for doc in docs:
            if doc["number"] == doc_num:
                print("\nDocument owner is", doc["name"])
                return doc["name"]
        print("\nThere's no such document number\n")
        continue


### Input document number and get shelf number with this document - 's', 'sl' - as of it's functionality, it's solo use is quite useless with little data
def shelf_by_number(dirs=directories, a=None, doc_num=None):
    while True:
        if a == None:
            ref_listing()
        elif a == "move":
            while not bool(doc_num):
                # doc_num = input("Input document number or 'q' to quit: ")
                if doc_num == "q":
                    return
        for shelf, number_list in dirs.items():
            if doc_num in number_list:
                if a == "sl":
                    print(f"- The document is on shelf {shelf}")
                else:
                    print(f"\nThe document is on shelf {shelf}")
                return shelf, doc_num
        dif_set_doc, dif_set_dir = compare_docs_dirs(type="sl")
        if bool(dif_set_doc):
            print("- The document is not on a shelf yet or doesn't exist")
            return None
        else:
            print("\nThere's no such document number\n")
        a = None
        continue


### Prints all available documents - 'l' or with shelf position - 'sl'
def all_docs(docs=documents, dirs=directories, a=None):
    # processing input variables
    if a == "add":
        print("\nNew list of documents:")
    elif a == "del":
        pass
    else:
        print("\nListing all documents:")
    # Printing with defined formating
    for doc in docs:
        for key, val in doc.items():
            if key == "type":
                print(f'{val} ', end="")
            else:
                print(f'"{val}" ', end="")
        if a == "sl":
            shelf_by_number(a="sl", doc_num=doc["number"])
        else:
            print()
    return


### Compares content of documents and directories to find inconsistancies - 'c'
def compare_docs_dirs(docs=documents, dirs=directories, type=None):
    temp_doc = []
    dir_set = set()
    for key, val in dirs.items():
        dir_set = dir_set | set(val)
    for doc_num in docs:
        temp_doc.append(doc_num["number"])
    doc_set = set(temp_doc)
    dif_set_doc = doc_set - dir_set

    if bool(dif_set_doc) and type == None:
        print(f"\nThe following documents {list(dif_set_doc)} are NOT on the shelves")
    dif_set_dir = dir_set - doc_set
    if bool(dif_set_dir) and type == None:
        print(f"\nThe following document numbers {list(dif_set_dir)} are listed on the shelves but don't have any data")
    if not bool(dif_set_doc | dif_set_dir) and type == None:
        print("\nAll data match")
    return (dif_set_doc, dif_set_dir)


### Adds document and positions it on desired shelf - 'a'
def add_doc(docs=documents, dirs=directories, doc_type=None, doc_num=None, doc_name=None, doc_shelf=None, new_shelf_req=None):
    # doc_type = input("Input document type: ")
    # doc_num = input("Input document number: ")
    # doc_name = input("Input document owner: ")
    while True:  # Loop to define user desire about new\old shelf for the new document
        print("Available shelves: ", list(dirs.keys()))
        # doc_shelf = input("Input where document will be stored or 'q' to quit: ")
        if doc_shelf in dirs.keys():
            break
        else:
            # new_shelf_req = input("There's no such shelf, want to add new one? y/n: ")
            if new_shelf_req in ["y", "ye", "yes"]:
                add_shelf(new_shelf=doc_shelf, type="add")
                break
    doc_dict = dict(type=doc_type, number=doc_num, name=doc_name)
    docs.append(doc_dict)
    for key, value in dirs.items():
        if key == doc_shelf:
            value.append(doc_num)
    print(f"\nNew document {doc_num} added to shelf {doc_shelf}.")
    all_docs(a="add")
    return


### Deletes all document data - 'd'
def del_doc(doc_num=None, type=None, docs=documents, dirs=directories):
    while True:
        ref_listing()
        # doc_num = ""
        # while not bool(doc_num):
        #     doc_num = input("Input document number to delete or 'q' to quit: ")
        if doc_num == "q":
            return
        presence = False
        print("\nSearching for document and deleting...")
        for i in range(len(docs)):
            if docs[i]["number"] == doc_num:
                del docs[i]
                presence = True
                print(f"\nDocument with number {doc_num} deleted from documents...\n")
                for key, val in dirs.items():
                    for n in range(len(val)):
                        if val[n] == doc_num:
                            del val[n]
                            dirs[key] = val
                            presence = True
                            print("...and from shelf...\n")
                            all_docs(a="del")
                            return
        # Processing documents on shelves without record in 'documents'
        for key, val in dirs.items():
            for n in range(len(val)):
                if val[n] == doc_num:
                    del val[n]
                    dirs[key] = val
                    presence = True
                    print(f"\nOld document with number {doc_num} deleted from shelves...\n")
                    return
        if not presence:
            return 'There"s no such document'
            # print("\nThere's no such document.\n")


### Deletes all empty shelves - 'ds'
def del_shelf(dirs=directories):
    e_shelves = 0
    temp_dirs = dirs.copy()
    for key, val in temp_dirs.items():
        if val:
            continue  # print("\nThere's no empty shelves")
        else:
            del dirs[key]
            e_shelves += 1
    if e_shelves > 0:
        print(f"\n{e_shelves} empty shelves deleted as they are empty.\n")
    else:
        print("\nThere's no empty shelves")
    list_shelves()
    return


### Moves selected document number withing desires shelves - 'm'
def move_doc(dirs=directories, shelf=None, doc_num=None, shelf_move=None, new_shelf_req=None):
    print("Shelves content for reference:")
    list_shelves()
    # doc_num = input("Input document number: ") - old version, current uses shelf_by_number for input
    # shelf, doc_num = shelf_by_number(a="move")
    # shelf_move = input("Which shelf you want to move it to? ")
    if shelf_move not in dirs.keys():
        # new_shelf_req = ''
        # while not bool(new_shelf_req):
            # new_shelf_req = input("There's no such shelf, want to add new one? y/n: ")
        if new_shelf_req in ["y", "ye", "yes"]:
            add_shelf(new_shelf=shelf_move, type="move")
            # break
        if new_shelf_req in ['q', 'n', 'no']:
            return new_shelf_req
    dirs[shelf].remove(doc_num)
    dirs[shelf_move].append(doc_num)
    print(f"\nShelf for {doc_num} changed from {shelf} to {shelf_move}")
    list_shelves()
    return


### Adds new shelf - 'as'
def add_shelf(dirs=directories, new_shelf=None, type=None):
    while True:  # Loop for correct user input
        if new_shelf is None:
            # new_shelf = input("Input new shelf number or 'q' to quit: ")
            # for test
            new_shelf = 'asd'
            if new_shelf == "q":
                return
            if new_shelf.isnumeric() == False:
                new_shelf = None
                return "Please use numbers"
                print("Please use numbers")
                continue
        # Processing and unacceptable data handling
        if new_shelf not in dirs.keys() and int(new_shelf) > 0:
            dirs[new_shelf] = []
            if type == "move" or type == "add":
                return new_shelf
            else:
                print("New shelf added, listing:")
                list_shelves()
                new_shelf = None
                return new_shelf
        else:
            if int(new_shelf) <= 0:
                print("Our shelves can't have zero or negative numeration.")
                return 'Negative not allowed'
                new_shelf = None
            elif new_shelf in dirs.keys():
                print("There's already shelf with this number.")
                return 'Already exists'
                new_shelf = None


### Shows the content of all shelves - 'sn'
def list_shelves(dirs=directories):
    for key, val in dirs.items():
        print(f"Shelf {key} - {val}")
    return


### Main menu cycle
def main():
    """
    __________________________________________
    p - searches person name by document number
    s - search on which shelf document is
    l - lists all available information
    sl - list all available information and shelves they are stored on
    c - compares docs and dirs and gives inconsistencies
    a - adds new document to 'documents' and where it will be stored
    d - fully delete document data
    ds - delete unused shelves
    m - move existing document
    as - adds new shelf
    sn - shows shelves content
    h - this help
    q - quits the programm
    __________________________________________

    """
    while True:
        print("For help type 'h'.")

        command = input("Input action: ")
        if command == "p":
            person_by_number()
            print("\nReturning to menu...\n")
        elif command == "s":
            shelf_by_number()
            print("\nReturning to menu...\n")
        elif command == "l":
            all_docs()
            print("\nReturning to menu...\n")
        elif command == "sl":
            all_docs(a="sl")
            print("\nReturning to menu...\n")
        elif command == "c":
            compare_docs_dirs()
            print("\nReturning to menu...\n")
        elif command == "a":
            add_doc()
            print("\nAdded, returning to menu...\n")
        elif command == "d":
            del_doc()
            print("\nReturning to menu...\n")
        elif command == "ds":
            del_shelf()
            print("\nReturning to menu...\n")
        elif command == "m":
            move_doc()
            print("\nReturning to menu...\n")
        elif command == "as":
            add_shelf()
            print("\nReturning to menu...\n")
        elif command == "sn":
            list_shelves()
            print("\nReturning to menu...\n")
        elif command == "h":
            help(main)
        elif command == "q":
            print("Quiting...")
            break
        else:
            print()


# main()

