from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256
import os
import base64
import getpass
class Authentication:
    #Eric: Password-123
    #Ashley: SomethingAround!713
    #Gabe: 1GreatFr!3nd51
    __User_List = [
        {
            "Name": "Eric Paddler",
            "Username": "EricTheHasher",
            "Password": "zq0Gi7iOPgeqFAkm+oR4Ng==$EE8qgrL6Iqe3tusydWak/5f31u9CyHa6sH9iIPQJpsQ=",
            "Role": "Admin",
            "Email": "Eric.Paddler@gmail.com"
        },{
            "Name": "Ashley FuckOff",
            "Username": "ashley4707",
            "Password": "G8SkcXmYFZO9yxibPvf+cg==$QSnrHrvU7hRysiWavLumPWb1dDBfOEDEmco485IFvRo=",
            "Role": "Buyer",
            "Email": "ashley587@hotmail.ca"
        },{
            "Name": "Gabe Gabu",
            "Username": "Gabu011",
            "Password": "odJjPbx+AeAhpQ77cuH1JA==$uxX2Cbkm2Es+KY4Q4b0Sg0DWQBc7AoD1p/qrJ+VV3Go=",
            "Role": "Seller",
            "Email": "SnickerGabu@yahoo.ca"
        }
    ]
    def __init__(self): #If each logged in user is stored in a class then this will hold their name and role.
        self.Username = ""
        self.Role = ""

    @classmethod
    def __Hash_Password(self,Password, salt):
        iterations = 600_000          # Number of iterations, in this case 600k.
        key_length = 32              # Desired key length in bytes, 32 in this case for SHA256.

        # Generate PBKDF2 hash
        kdf = PBKDF2HMAC(
            algorithm=SHA256(),
            length=key_length,
            salt=salt,
            iterations=iterations,
        )
        return kdf.derive(Password)
    

    def Login_Menu(self):
        Store_name = "The nighthawk" #Whatever you want to name it.

        print(f"Welcome to {Store_name}!")
        print(f"Please enter the following credentials to login.")

        EmailOrUsername_Input = input("Username or Email: ")
        Password = getpass.getpass(prompt="Enter your password: ") #Password wont show up when you're typing for security.

        Username, Role = self.__class__.__Authenticate_Creds(EmailOrUsername_Input.strip(), Password) #Pass input creds for auth,
        
        self.Username = Username
        self.Role = Role
        print(f"Successfully logged in as:\nUsername: {self.Username}\nRole: {self.Role}")

    @classmethod
    def __Authenticate_Creds(cls,EmailOrUsername_Input, password):
        Found = 0
        for user in cls.__User_List: #Iterating through the list of Users.
            if EmailOrUsername_Input == user["Username"] or EmailOrUsername_Input == user["Email"]: #Checking for a match in username or email.
                Salt_And_hash_List = user["Password"].split("$",2) #If there's a match seperate the salt and hash from the user's profile.
                salt = base64.b64decode(Salt_And_hash_List[0]) #Turn the salt back into it's original state by decoding it from base64.
                # This salt will be needed when authenticating else the hash will be completely different.
                Byte_password = password.encode("utf-8")
                if cls.__Hash_Password(Byte_password, salt) == (base64.b64decode(Salt_And_hash_List[1])): #Check the passwords.
                    print("MATCH!")
                    Found = 1
                    return user["Username"], user["Role"] #Return the user's username and role.
        if Found != 1: #Else credentials were never found or didn't match.
            print("Credentials did not match!") 
            return "Invalid", "Invalid"
        
    @classmethod
    def Password_Create_Criteria(cls,Password):
        max_Pass_Len = 33 #Max password length variable.
        min_Pass_Len = 3 #Min password length variable.
        Allowed_Special_Char_List = ["!","@","#","$","%","^","&","*","_","+","-","=","|",":",";",",","?","/"]
        #^ List of special char's we allow.
        Len_Password = len(Password) #Getting the length of the password that the user input.
        if min_Pass_Len <= Len_Password <= max_Pass_Len: #See if it's within the length range.
            for Spec_Char in Allowed_Special_Char_List: #Going through the list of special chars.
                if Spec_Char in Password: #Checking to see if there's a special char.
                    print(Spec_Char)
                    return 0 #Return 0 if it all is good.
            return 1 #Return 1 if it matches the length but not the special char req.
        else:
            return 3 #Else if it doesn't match the word requirement then return 3.
        
    @classmethod
    def register(cls):
        Username = ""
        Password = ""
        Email = ""
        # Profile variables I want them to fill in when creating a new profile.
        Conditions_met = False #A variable to help decide if all 3 have been met.
        print("Please insert name below")
        Name = input("Name: ")  #We don't mind repeating names but we don't accept repeating usernames.
        while(Conditions_met == False): #Will loop as long as they don't meet the conditions.
            print("Please insert username below")
            Username = input("Username: ")
            for user_i in range(len(cls.__User_List)): #Going through the range of items in the user list.
                if cls.__User_List[user_i].get("Username") == Username: #Attempting to get the username and see if it exists.
                    print("Username already exists!")
                    break #If it exists break out of the for loop.
                elif user_i == (len(cls.__User_List)-1): #Else if it hits the end and still no match.
                    print("Please enter an email below") #Now we would like an email.
                    Email = input("Email: ")
                    if "@" not in Email: #If @ is not in the email it's invalid. Doesn't actually need a real email but the bar minimum.
                        print("Invalid email")
                        continue #It will exceed the loop and loop back asking for a username and then email again.
                    else:
                        print("Please insert a password below") #Now that we got the email and username done, the most resource intesive begins.
                        Password = input("Password: ")
                        Salt = os.urandom(16) #Create a random 16 byte salt using random os noise.
                        if cls.Password_Create_Criteria(Password) == 0: #If the password matches the criteria.
                            #^ Checks the Criteria by passing it to the function above and testing it for certain values and length.
                            print("Password good to go!")
                            Hashed_Pass = cls.__Hash_Password(Password.encode("utf-8"), Salt) #We'll create the password hash using the salt and byte password.
                            Password = base64.b64encode(Salt).decode()+"$"+base64.b64encode(Hashed_Pass).decode() #We'll combine the hashed password and salt into a string stored seperately as base64 seperated by "$".
                            Conditions_met = True #Conditions met is True.
        cls.__User_List.append( #We'll append on a new dictionary using the information provided to User List but default role set to "Buyer".
            {
                "Name": Name,
                "Username": Username,
                "Password": Password,
                "Role": "Buyer",
                "Email": Email
            }
        )
    @classmethod
    def __Admin_Modify_User_Data_Actions(cls, Action, Username, Item,Value):
        for Profile_Index in range(len(cls.__User_List)): #Iterate through the range of user profiles.
            if cls.__User_List[Profile_Index]["Username"] == Username: #If it finds the name.
                if cls.__User_List[Profile_Index]["Role"] == "Admin": #If the profile wanting to be modified is an adamin.
                    print("SECURITY VIOLATION!") #This isn't allowed.
                    print("You may not modify or see another administrator's profile.")
                    break #Stop the loop/Break out of the loop.
                elif Action == 1: #Else if the role is not admin and action is 1.
                    print("Action delete")
                    del cls.__User_List[Profile_Index] #Delete the profile at Profile Index.
                    break #Stop the loop/Break out of the loop.
                elif Action == 2: #Else if action is 2 then we're going to modify.
                    print("Action Modify")
                    cls.__User_List[Profile_Index][Item] = Value #Change the user profile item (Eg., Role, Email) to the new value.
                    break #Stop the loop/Break out of the loop.
                else:
                    print("Command could not be processed!")
        

        
    def Admin_Modify_User_Data_GUI(self):
        try:
            if self.Role == "Admin":
                print("This is a restricted feature, please insert password.")
                Password = getpass.getpass(prompt="Password: ")
                User, Role = self.__class__.__Authenticate_Creds(self.Username, Password) #Authenticating to increase integrity of the user.
                if (User != self.Username or Role != self.Role) and Role == "Admin": #Making sure the instances variables have not been modified to do an unauthorized action.
                    print("Access denied!")
                else:
                    while 1: #An inf loop that must be broken out of.
                        # Here is the menu of what an admin can regarding the user list.
                        print("What action would you like to perform?")
                        print("1) Modify/Update a user")
                        print("2) Register a user")
                        print("3) Read users?")
                        print("4) Go back to main menu") #Only way to leave this feature is by using 4.
                        try:
                            User_Input = int(input("> ")) #Going go try to accept an input and cast it to an int.
                        except: #If it can't cast or accept the input then:
                            print("Invalid option") #Print invalid option
                            continue #Loop back to the menu.
                        if 1 <= User_Input <= 4: #Even if it was casted to an int we must make sure it's within the proper range of options.
                            if User_Input == 1: #Modify option was selected.
                                # below is the modify menu with some examples.
                                print("Modification actions:")
                                print("DEL) Delete (Eg., DEL username) - Will delete the user profile with that username.")
                                print("MOD) Modify (Eg.m MOD username Email newEmail@gmail.com) - Will modify the profile with username and field Email.")
                                print("Note: All fields you wish to modify are case sensitive and only allows 1 field change at a time.")
                                print("-------------------------------------------------")
                                print("User data you may alter:") #We'll print out what user's the admin can modify but keeping the passwords a secret.
                                for userProfile in self.__class__.__User_List:
                                    if userProfile["Role"] != "Admin":
                                        print(f"Username: {userProfile["Username"]}\nName: {userProfile["Name"]}\nEmail: {userProfile["Email"]}\nRole: {userProfile["Role"]}")
                                        print("-------------------------------------------------")
                                print("-------------------------------------------------")
                                try:
                                    Command = input("Command: ")
                                    Extract_CMD_Parts = Command.split(" ", 3) #Going to create a list splitting at spaces but only a set amount.
                                    if Extract_CMD_Parts[0] == "DEL": #If DEL is the first item in the list then perform DELETE action.
                                        self.__class__.__Admin_Modify_User_Data_Actions(1,Extract_CMD_Parts[1],"Ignore", "Ignore")
                                        #^ Call the function that does action and let it know to delete via 1, user via Extract_CMD_Parts[1] and Ignore the other 2 values.
                                    elif Extract_CMD_Parts[0] == "MOD": #If MOD is the first item in the list then perform MODIFY action.
                                        self.__class__.__Admin_Modify_User_Data_Actions(2,Extract_CMD_Parts[1],Extract_CMD_Parts[2],Extract_CMD_Parts[3])
                                        #^ Same as DEL but says to use 2 which means modif and then instead of Ignore you have the item (eg., Role, Email) and The new value.
                                    else:
                                        print("Unknown command, please use ('DEL' or 'MOD')") #If the command could not be determined.
                                except:
                                    print("An error has occurred please contact IT support.")
                            elif User_Input == 2: #If the admin wants to register a user.
                                self.__class__.register() #Will call our register class function going to another GUI.
                                print("User successfully registered!")
                            elif User_Input == 3: #If the admin chooses to see all the users.
                                for userProfile in self.__class__.__User_List: #Showing all the users but keeping the passwords a secret.
                                    print(f"Username: {userProfile["Username"]}\nName: {userProfile["Name"]}\nEmail: {userProfile["Email"]}\nRole: {userProfile["Role"]}")
                                    print("-------------------------------------------------")
                            elif User_Input == 4:
                                break
            else: #If role is not Admin then they are forbidden from accessing this.
                print("Forbidden!") 
        except: #In case a problem happens.
            print("An error was detected in this feature, please contact administration if needed.")
    @property
    def Get_Info(self):
        return self.Username, self.Role #Will return the name and role of the user.


        #if[EmailOrUsername_Input]==[user["Username"]]or[EmailOrUsername_Input]==[user["Email"]]:print("Found user!")
        #^ Don't use this line lol. I just thought it was funny.

User1 = Authentication() #Creating an instance of authentication for User1.
User1.Login_Menu() # Calls the login GUI.
Info = User1.Get_Info #Will return 2 variables, Username, Role of instance User1.
Username = Info[0] # If you want to store the user's username.
Role = Info[1] #If you want to store the user's role.
User1.Admin_Modify_User_Data_GUI() #Call this if you want Admin to make changes to user profiles.
#User1.register()
#User2 = Authentication()
#User2.Login_Menu()
