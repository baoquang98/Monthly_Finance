from glob import glob
import csv
import os 
from argparse import ArgumentParser, Action, ArgumentError

card_info = {
    "Discover": {
        "name_match": "Discover-Statement-*.csv",
        "raw_data": [],
        "process_data": []
    },
    
    "Chase": {
        "name_match": "Chase*.CSV",
        "raw_data": [],
        "process_data": []
    },
    
    "TD": {
        "name_match": "transactions*.csv",
        "raw_data": [],
        "process_data": []
    },

    "WF": {
        "name_match": "CreditCard2*.csv",
        "raw_data": [],
        "process_data": []
    },

    "USBank": {
        "name_match": "Credit Card - *.csv",
        "raw_data": [],
        "process_data": []
    },
    
    "Bilt": {
        "name_match": "CreditCard1*.csv",
        "raw_data": [],
        "process_data": []
    },    
    
    "Paypal": {
        "name_match": "Download*.CSV",
        "raw_data": [],
        "process_data": []
    }
}

def read_csv_input(args):
    for card, info in card_info.items():
        file_list = glob(os.path.join(args.input, info["name_match"]))
        if file_list:
            file_name = file_list[0]
            print(file_name)
        else:
            print("Can't find csv file for {}".format(card))
            continue
            # exit()
        with open(file_name, mode ='r') as file:
            csvFile = csv.reader(file)
            raw_data = [l for l in csvFile]
            info["raw_data"] = raw_data

def preprocess_data_discover():
    card = "Discover"
    raw_data = card_info[card]["raw_data"]

    raw_data = raw_data[1:]
    process_data = []
    #Discover raw data header: Trans. Date,Post Date,Description,Amount,Category
    for l in raw_data:
        if l[2].find("INTERNET PAYMENT - THANK YOU") == -1:
            process_l = [card, l[0], l[1], l[2], l[3], find_category(l[2]), ""]
            process_data.append(process_l)
    
    card_info[card]["process_data"] = process_data

def preprocess_data_chase():
    card = "Chase"
    raw_data = card_info[card]["raw_data"]
    raw_data = raw_data[1:]
    process_data = []
    #Chase raw data header: Transaction Date,Post Date,Description,Category,Type,Amount,Memo
    for l in raw_data:
        if l[2].find("Payment Thank You") == -1:
            process_l = [card, l[0], l[1], l[2], -float(l[5]), find_category(l[2]), ""]
            process_data.append(process_l)
    
    card_info[card]["process_data"] = process_data

def preprocess_data_td():
    card = "TD"
    raw_data = card_info[card]["raw_data"]
    raw_data = raw_data[1:]
    process_data = []
    # TD raw data header: Date,Account Number,Description,Debit,Credit
    #                      "Card", "Transaction Date", "Post Date", "Description", "Amount", "Category", "Note"
    for l in raw_data:
        if l[2].find("PAYMENT RECEIVED") == -1:
            process_l = [card, l[0], l[0], l[2], float(l[3]), find_category(l[2]), ""]
            process_data.append(process_l)
    
    card_info[card]["process_data"] = process_data

def preprocess_data_wf():
    card = "WF"
    raw_data = card_info[card]["raw_data"]
    process_data = []
    # WF raw data header: Date,Amount,,,Description
    #                      "Card", "Transaction Date", "Post Date", "Description", "Amount", "Category", "Note"
    for l in raw_data:
        if l[4].find("PAYMENT THANK YOU") == -1:
            process_l = [card, l[0], l[0], l[4], -float(l[1]), find_category(l[4]), ""]
            process_data.append(process_l)
    
    card_info[card]["process_data"] = process_data

def preprocess_data_usbank():
    card = "USBank"
    raw_data = card_info[card]["raw_data"]
    raw_data = raw_data[1:]
    process_data = []
    # USBank raw data header:"Date","Transaction","Name","Memo","Amount"
    #                      "Card", "Transaction Date", "Post Date", "Description", "Amount", "Category", "Note"
    for l in raw_data:
        if l[2].find("PAYMENT THANK YOU") == -1:
            process_l = [card, l[0], l[0], l[2], -float(l[4]), find_category(l[2]), ""]
            process_data.append(process_l)
    
    card_info[card]["process_data"] = process_data

def preprocess_data_bilt():
    card = "Bilt"
    raw_data = card_info[card]["raw_data"]

    process_data = []
    # Bilt raw data header: Date,Amount,,,Description
    #                      "Card", "Transaction Date", "Post Date", "Description", "Amount", "Category", "Note"
    for l in raw_data:
        if l[4].find("PAYMENT THANK YOU") == -1:
            process_l = [card, l[0], l[0], l[4], -float(l[1]), find_category(l[4]), ""]
            process_data.append(process_l)
    
    card_info[card]["process_data"] = process_data

def preprocess_data_paypal():
    card = "Paypal"
    raw_data = card_info[card]["raw_data"]

    process_data = []
    # Bilt raw data header: "Date","Time","TimeZone","Name","Type","Status","Currency","Amount","Fees","Total","Exchange Rate","Receipt ID","Balance","Transaction ID","Item Title"
    #                       "Card", "Transaction Date", "Post Date", "Description", "Amount", "Category", "Note"
    for l in raw_data:
        if l[4] == "General PayPal Debit Card Transaction":
            process_l = [card, l[0], l[0], l[3], -float(l[7]), find_category(l[3]), ""]
            process_data.append(process_l)
    
    card_info[card]["process_data"] = process_data

def preprocess_data():
    preprocess_data_discover()
    preprocess_data_chase()
    preprocess_data_td()
    preprocess_data_wf()
    preprocess_data_usbank()
    preprocess_data_bilt()
    preprocess_data_paypal()

def find_category(desc):
    kword_to_cat = [
        (["bps"], "Housing"),
        (["state farm", "comcast", "annual membership fee", "energy"], "Utilities"),
        (["peacock", "stubhub", "movie", "amc", "spotify"], "Entertainment"),
        (["chewy", "petsmart", "petco"], "Pet"),
        (["walgreens", "cvs"], "Medical"),
        (["h mart", "lidl", "costco whse", "walmart", "wal-mart", "www costco com"], "Groceries"),
        (["costco gas", "sheetz", "shell", "liberty", "gas"], "Gas"),
        (["goodwill", "temu", "amazon", "planet aid", "uniqlo"], "Merchandise"),
        (["tbaar", "seafood", "lobster", "nishiki", "canteen", "outback", "kusshi", "pho", "wine kitchen", "swirls", "grill", "bubble tea", "lucky corner", "teado"], "Restaurants"),
        (["lift", "uber", "travel"], "Travel")
    ]
    
    for kword_list, category in kword_to_cat:
        for kword in kword_list:
            if desc.lower().find(kword) != -1:
                return category
    return ""

def write_csv_output(args):
    output = []
    if args.header:
        output = [["Card", "Transaction Date", "Post Date", "Description", "Amount", "Category", "Note"]]

    for info in card_info.values():
        output += info["process_data"]

    print(output)
    with open(os.path.join(args.output, "output.csv"), 'w') as file:
        writer = csv.writer(file)
        writer.writerows(output)

def main():
    args = parse_args()
    if not args.input:
        args.input = os.getcwd()
    if not args.output:
        args.output = os.getcwd()
        
    read_csv_input(args)
    preprocess_data()
    write_csv_output(args)



# =============================================================================
def parse_args(args=None):
    parser = ArgumentParser()
    
    parser.add_argument(
        "-H",
        "--header",
        action="store_true",
        help="Enable header on output file",
    )
    parser.add_argument(
        "-i",
        "--input",
        help="Input location, default to current directory",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output location, default to current directory",
    )
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    main()