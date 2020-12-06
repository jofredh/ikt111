import re
import time
askForId = "To help you best we will need your customer ID. It can be found on your contract or invoice\nIt looks something like this: '1-456'"
noIdOrInvalid = "You either did not provide a valid id, or we couldn't find it in our database.\nTo better help you we will refer you to our customer service department."
running = True

cities = {'1':"New York",'2':"Los Angeles",'3':"Seattle"}


class Customer:
    def __init__(self, id, name, age, technical=False):
        self.id = id
        self.name = name
        self.age = age
        self.technical = technical
        self.location = cities[id.split('-')[0]] #Lookup customer location based on id format.

class Database: #Customer Database for chatbot
    def __init__(self,customers):
        self.outages = {'New York':['cable','cellular'],'Seattle':['internet'],'Los Angeles':['satelite']}
        self.customers = customers
        self.cities = [customer.location for customer in customers if customer.location]
    
    def checkId(self, id):
        return [customer for customer in self.customers if customer.id == id] #Gets the first customer with matching ID.

    def checkOutages(self, customer):
        if customer.location in self.outages:
            return self.outages[customer.location]

#Customer class instances
#Customers can 'move' across the country
#   To do this, change first digit of ID.
#   Currently only 1-3 are valid IDs.
Bob = Customer('1-234','Bob Jones', 23, True)
Bobb = Customer('1-234','Bobb Jones', 23, True) #Duplicate ID, will be ignored when ID is searched.
Bridget = Customer('1-364','Bridget Jamie', 78)
Simon = Customer('3-192','Simon Richardson',42)
John = Customer('2-453','John Jameson',240)
cList = [Bob,Bobb,Bridget,Simon,John]
db = Database(cList)

def referToHuman():
    time.sleep(2)
    print("This chatlog along with a call request has been forwarded to our customer service department.")
    time.sleep(2)
    print("You will receive a call from a real person in a moment.")
    time.sleep(2)
    print("Please wait patiently.")
    time.sleep(2)
    quit()

def Greet(name=None):
    a = f"." if name==None else f" {name}."
    print(f"Thank you for contacting Telecompany support{a}")
    time.sleep(2)
    print("I am a chatbot designed to help fix simple issues.")
    time.sleep(2)
    print("Please describe your problem in simple terms.")

def getId():
    print(askForId)
    idResponse = input()
    if re.match(r'\d{1}-\d{3}',idResponse) is not None:
        customers = db.checkId(re.match(r'\d{1}-\d{3}',idResponse).string)
        if customers:
            customer = customers[0]
            print(f"Thank you {customer.name.split(' ')[0]}.")
            return customer
        else:
            print(noIdOrInvalid)
            time.sleep(3)
            referToHuman()

def internetRoutine(customer):
    if customer.technical:
        print(f"Hi {customer.name}. As you are registered as technically competent, we will skip the basic plug-unplug stuff,-\nand will now directly hand your case to customer support. Thank you.")
        referToHuman()
    else:
        print("Imagine instructions for solving internet problems here.")
        time.sleep(1)
        print("Did that resolve your problem?")
        time.sleep(1)
        ans = input()
        if 'yes' in ans:
            print("Great. Have a nice day.")
            quit()
        else:
            print("We apologize for the inconvenience.")
            print("To better help you we will refer you to our customer service department.")
            referToHuman()


while running:
    Greet()
    problemInput = input()
    customer = getId()
    outages = db.checkOutages(customer)
    if(outages):
        print(f"We are currently experiencing outages in {customer.location} for {outages} services.")
        time.sleep(2)
        print("We are sorry about this. Is your problem related to these services?")
        ans = input()
        if('yes' in ans):
            print("We apologize for the inconvenience. Technicians are working on the problem as we speak!\nPlease contact us again in an hour if the problem has not been resolved.\nThank you again for contacting Telecompany Support.")
        else:
            if('internet' in problemInput):        
                internetRoutine(customer)
            else:
                print("We either didn't understand your request, or don't offer automated responses for your issue.")
                print("To better help you we will refer you to our customer service department.")
                referToHuman()
    if('internet' in problemInput):        
        internetRoutine(customer)
    else:
        print("We either didn't understand your request, or don't offer automated responses for your issue.")
        print("To better help you we will refer you to our customer service department.")
        referToHuman()


