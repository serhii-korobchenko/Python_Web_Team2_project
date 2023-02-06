
# Input - dict(name: telephone number)
# Requirements:
#              - telephone number format: 0675223345 - 10 digits;
#              - bot undestands commands:
#                          - "hello" - answear: "How can I help you?"
#                          - "add' name telephone number" - save new contact
#                          - "change' name telephone number" - change telephone number for existed contact
#                          - "phone' name" - show telephone number
#                          - "addnum' name telephone number" - add aditional tel number for certain contact
#                          - "del' name telephone number" - del tel number for certain contact
#                          - "help" - bot show commands explanations
#                          - "lookup' text" - find text in records (no difference which case of characters)
#                          - "delrec' name" - delete record from AddressBook
#                           - "addemail' name email" - add email to record
#                           - "changeemail" name new_email - change all emails on new one
#                           - "addadress' name text" - add adress to record
#                           - "addbirthday' name" - add birthday to record
# new                       - "addnote' note_title text" - add note to DB
# new                       - "delnote' note_title - del note from DB
# new                       - "addtag' text note title " - add tag to Note
# new                       - "deltag' text" - del tag from DB
#                           - "good bye" or "close" or "exit" - bot stops work and message "Good bye!"


import os
from ast import List
import re
from collections import UserDict
from datetime import datetime
import csv
from abc import abstractmethod, ABC
import sqlalchemy
from DB_handlers_cli_bot import *
from models import Email, Record, Adress, Phone
from db import db_session
from flask import flash


# GLOBALS

x = 0
page = 1
command_list = []

help_information = ' Bot undestands next commands:\
          - "hello" - answear: "How can I help you?"\
          - "add" name telephone number" - save new contact\
          - "change" name telephone number" - save new telephone number for existed contact\
          - "phone" name" - show telephone number\
          - "addnum" name telephone number" - add aditional tel number for certain contact\
          - "del" name telephone number" - del tel number for certain contact\
          - "help" - bot show commands explanations\
          - "lookup" text" - find text in records (no difference which case of characters)\
          - "delrec" name" - delete record from AddressBook\
          - "addemail" name email" - add email to record\
          - "changeemail" name new_email" - change all emails on new one\
          - "addnotes" name text" - add notes to record\
          - "addadress" name text" - add adress to record\
          - "addbirthday" name" - add birthday to record \
          - "daysbeforebirth" # days" - check birthdays in time period \
          - "addnote title text" - add note to DB\
          - "delnote title - del note from DB\
          - "addtag text note_title " - add tag to Note\
          - "deltag text" - del tag from DB\
          - "good bye" or "close" or "exit" - bot stops work and messege "Good bye!" '


class AddressBook (UserDict):

    def __init__(self):
        UserDict.__init__(self)
        self.notes_data = {}
        self.presenter = PresenterRecords()

    def add_record(self, name, phone):

        self.phone = phone
        Name.value = name
        self.data[name] = Record()

    def iterator(self):

        global x
        global page

        while x <= len(self.data):

            for key_in, value_in in self.data[list(self.data)[x]].record_dict.items():

                if value_in:
                    if isinstance(value_in, list):
                        print(
                            f"{key_in} : {', '.join(map(str, value_in))} | ", end=" ")
                    else:
                        print(f"{key_in} : { value_in} | ", end=" ")

            x += 1
            page += 1
            yield x

    def del_record(self, name):
        del self.data[name]




class Field:
    pass


class Name (Field):

    value = None


class Phone (Field):

    def __init__(self, value) -> None:
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):

        if re.match(r"^[0-9]{10,10}$", new_value):

            #print ('Number format has been checked successfully!')
            self.__value = new_value

        else:
            print('Telephone number does not match format!')
            flash('Telephone number does not match format!')

class Notes:

    def __init__(self):
        self.presenter = PresenterNotes()

    def change_notes(self, name, phone):  # name=tag phone=note
        self.tag = name
        self.note = phone
        self.result = {}

        with open('notes.csv', newline='') as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                self.result.update({row['tag']: row['note']})
        self.result.pop(self.tag)
        self.result.update({self.tag: self.note})

        counter = 0
        for k, v in self.result.items():
            if counter == 0:
                with open('notes.csv', 'w', newline='') as fh:
                    field_names = ['tag', 'note']
                    writer = csv.DictWriter(fh, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerow({'tag': k, 'note': v})
            else:
                with open('notes.csv', 'a', newline='') as fh:
                    field_names = ['tag', 'note']
                    writer = csv.DictWriter(fh, fieldnames=field_names)
                    # writer.writeheader()
                    writer.writerow({'tag': k, 'note': v})
            counter += 1
        print(f'Note with tag {self.tag} updated')

    def del_notes(self, name):  # name=tag
        self.tag = name
        self.result = {}
        with open('notes.csv', newline='') as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                self.result.update({row['tag']: row['note']})
        self.result.pop(self.tag)

        counter = 0
        for k, v in self.result.items():
            if counter == 0:
                with open('notes.csv', 'w', newline='') as fh:
                    field_names = ['tag', 'note']
                    writer = csv.DictWriter(fh, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerow({'tag': k, 'note': v})
            else:
                with open('notes.csv', 'a', newline='') as fh:
                    field_names = ['tag', 'note']
                    writer = csv.DictWriter(fh, fieldnames=field_names)
                    # writer.writeheader()
                    writer.writerow({'tag': k, 'note': v})
            counter += 1
        print(f'Note with tag {self.tag} deleted')


##########################################################


class Email (Field):

    def __init__(self) -> None:
        self.value = None

    def change_email(self, name, new_email):
        add_book.data[name].record_dict['Email'].clear()
        add_book.data[name].record_dict['Email'].append(new_email)


class Adress (Field):

    def __init__(self) -> None:
        self.value = None

    def change_adress(self):
        pass

class Birthday (Field):

    def __init__(self, value=None) -> None:
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):

        try:

            if re.match(r"\d{2}.\d{2}.\d{4}", new_value):

                birthday_data_list = new_value.split('.')

                birthday_datatime = datetime(year=int(birthday_data_list[2]), month=int(
                    birthday_data_list[1]), day=int(birthday_data_list[0])).date()

                self.__value = birthday_datatime
                print('Birthday date has been added successfully!')

            else:
                raise BirthdayDoesNotMathFormatError

        except BirthdayDoesNotMathFormatError:

            print("You have to set date in next format: dd.mm.yyyy! ")
            BirthdayDoesNotMathFormatError.status = 1

        except KeyError:
            print("This contact does not exist! First - set up appropriate contact")
            TryAgainError.status = 1

        except ValueError:
            print("You have to set date in next format: 1-31.1-12.0000-9999!")
            TryAgainError.status = 1
class Record:

    def __init__(self) -> None:

        self.name = Name()
        self.phone = Phone(add_book.phone)
        self.email = Email()
        self.adress = Adress()
        self.record_dict = {
            'Name': self.name.value,
            'Phone': [self.phone.value],
            'Birthday': None,
            'Email': None,
            'Adress': None
        }

    def add_phone(self, name, phone):
        # add_book.data[name].append(phone)
        add_book.data[name].record_dict['Phone'].append(phone)

    def del_phone(self, name, phone):
        add_book.data[name].record_dict['Phone'].remove(phone)

    def edit_phone(self, name, new_phone):
        add_book.data[name].record_dict['Phone'].clear()
        add_book.data[name].record_dict['Phone'].append(new_phone)


    def add_email(self, name, email):

        if add_book.data[name].record_dict['Email']:
            add_book.data[name].record_dict['Email'].append(email)

        else:
            add_book.data[name].record_dict['Email'] = []
            add_book.data[name].record_dict['Email'].append(email)

    def add_adress(self, name, adress):
        add_book.data[name].record_dict['Adress'] = adress

class TelDoesNotMathFormatError(Exception):
    status = 0

class BirthdayDoesNotMathFormatError(Exception):
    status = 0

class NameDoesNotExistError(Exception):
    status = 0

class TryAgainError(Exception):
    status = 0


class Presenter(ABC):

    @abstractmethod
    def see_iteration(self):
        pass

    @abstractmethod
    def show_all(self):
        pass


class PresenterRecords(Presenter): 

    def see_iteration(self, n):
        try:
            global x
            global page

            if len(add_book.data) - (x + 1) >= 0:
                print(f'Page #: {page}. ')
            else:
                print('Stop listing!')
            record_generator = add_book.iterator()
            for x in range(x, x + int(n)):
                next(record_generator)

        except IndexError:

            print(f"Sorry, no more records! Use 'show all' command!")

    def show_all(self):
        pass



class PresenterNotes(Presenter):

    def see_iteration(self, n):
        pass

    def show_all(self):
        print('')
        print('EXISTED NOTES:')
        for key, value in add_book.notes_data.items():
            print(f"Tag: {key} | Note: {value}  ")

            print('')


def command_parser(command):  # command`s parser
    command_id = ''
    name = ''
    phone = ''

    parsered_list = command.split(" ")

    if len(parsered_list) == 1:
        command_id = parsered_list[0].lower()  # make all letters small

    elif len(parsered_list) == 2:
        command_id = parsered_list[0].lower()
        name = parsered_list[1]
    elif len(parsered_list) == 3:
        command_id = parsered_list[0].lower()
        name = parsered_list[1]
        phone = parsered_list[2]
    elif len(parsered_list) > 3:
        command_id = parsered_list[0].lower()
        name = parsered_list[1]
        slice_parser = parsered_list[2:]
        phone = ' '.join(map(str, slice_parser))
        # phone = parsered_list[2]
    else:
        print("Number of arguments do not fit to reqirements. Please try again!")
        flash('Number of arguments do not fit to reqirements. Please try again!')
    return command_id, name, phone



# Decorator
def input_error(func):  # decorator

    def inner(*args, **kwargs):

        func(*args, **kwargs)

        if TelDoesNotMathFormatError.status == 1:  # added functional zone
            print('Format does not match')
            flash('Format does not match')
            TelDoesNotMathFormatError.status = 0
        elif NameDoesNotExistError.status == 1:
            print('Enter user name please')
            flash('Enter user name please')
            NameDoesNotExistError.status = 0
        elif TryAgainError.status == 1:
            print('Please, Try again!')
            flash('Please, Try again!')
            TryAgainError.status = 0
        elif BirthdayDoesNotMathFormatError.status == 1:
            print('Please, Try again!')
            flash('Please, Try again!')
            BirthdayDoesNotMathFormatError.status = 0

    return inner

# Handlers:
def hello_func():
    print('How can I help you?')
    flash('How can I help you?')

@input_error
def add_func(name, phone):  # 1&2

    try:
        if re.match(r"^[0-9]{10,10}$", phone):

            #add_book.add_record(name, phone)  # 2
            add_records_DB(name, phone)

            print('Information has been added successfully!')
            flash('Information has been added successfully!')
        else:
            raise TelDoesNotMathFormatError

    except TelDoesNotMathFormatError:

        print("Telephone number does not match format - should be 10 digits")
        flash("Telephone number does not match format - should be 10 digits")
        TelDoesNotMathFormatError.status = 1

    except sqlalchemy.exc.IntegrityError:
        print("This user already exist. Try new one")
        flash("This user already exist. Try new one")

@input_error
def change_func(name, phone):  # 1&2

    try:
        if name in add_book.data:
            if re.match(r"^[0-9]{10,10}$", phone):

                #Record().edit_phone(name, phone)  # 2
                change_phone_DB(name, phone)

                print('Phone number has been changed successfully!')
                flash('Phone number has been changed successfully!')
            else:
                raise TelDoesNotMathFormatError

        else:
            raise NameDoesNotExistError

    except TelDoesNotMathFormatError:

        print("Telephone number does not match format - should be 10 digits")
        flash("Telephone number does not match format - should be 10 digits")
        TelDoesNotMathFormatError.status = 1

    except NameDoesNotExistError:

        print('Name does not exist')
        NameDoesNotExistError.status = 1

@input_error
def phone_func(name):  # 1&2

    try:

        if name in add_book.data:  # 2

            mystring = ', '.join(
                map(str, add_book.data[name].record_dict['Phone']))

            print(f'Phone number assigned for requested name is: {mystring}')
            flash(f'Phone number assigned for requested name is: {mystring}')

        else:
            raise NameDoesNotExistError

    except NameDoesNotExistError:

        print('Name does not exist.')  # - decorator
        flash('Name does not exist.')
        NameDoesNotExistError.status = 1




@input_error
def addnum_func(name, phone):  # 1&2

    try:
        if re.match(r"^[0-9]{10,10}$", phone):

            #Record().add_phone(name, phone)  # 2
            add_phone_DB(name, phone)

            print('Information has been added successfully!')
            flash('Information has been added successfully!')
        else:
            raise TelDoesNotMathFormatError

    except TelDoesNotMathFormatError:

        print("Telephone number does not match format - should be 10 digits")
        flash("Telephone number does not match format - should be 10 digits")
        TelDoesNotMathFormatError.status = 1

@input_error
def del_func(name, phone):  # 1&2

    try:
        if re.match(r"^[0-9]{10,10}$", phone):

            #Record().del_phone(name, phone)  # 2
            del_phone_DB(name, phone)

            print('Telephone number has been deleted successfully!')
            flash('Telephone number has been deleted successfully!')
        else:
            raise TelDoesNotMathFormatError

    except TelDoesNotMathFormatError:

        print("Telephone number does not match format - should be 10 digits")
        flash("Telephone number does not match format - should be 10 digits")
        TelDoesNotMathFormatError.status = 1

    except ValueError:
        print("Number assigned for deletion does not exist!")
        flash("Number assigned for deletion does not exist!")
        TryAgainError.status = 1





def help_func():
    print(help_information)
    flash(help_information)


def load_func():

    try:

        res = load_DB()

        for key, value in res.items():

            add_book.add_record(key, '0000000000')
            add_book.data[key].phone = value.get('Phone')
            add_book.data[key].adress = value.get('Adress')
            add_book.data[key].email = value.get('Email')
            add_book.data[key].record_dict = value

        ### FUNC_DB
                
        print('Data base has been loaded successfully!')


    except FileNotFoundError:
        print(
            "File not found! Please, make sure file is exist or name was written correctly!")

def lookup_func(text):
    look_up_DB (text)


def birthdaylook_func(number_days):
    birthday_in_days(number_days)

def addnote_func(title, text):
    addnote_func_DB(title, text)
    print('Note has been added successfully!')
    flash('Note has been added successfully!')

def delnote_func(title):
    delnote_func_DB(title)
    print('Note has been deleted successfully!')
    flash('Note has been deleted successfully!')


def addtag_func(name, note):
    pass

def deltag_func(name):
    pass


        
@input_error
def del_record_hand(name):  # ---- !!!!!
    try:

        if name in add_book.data:

            #add_book.del_record(name)
            del_rec_DB(name)

            print(f'Record :{name} has been deleted successfully!')
            flash(f'Record :{name} has been deleted successfully!')

        else:
            raise NameDoesNotExistError

    except NameDoesNotExistError:

        print('Record does not exist.')
        flash('Record does not exist.')
        NameDoesNotExistError.status = 1

@input_error
def add_email_head(name, email):

    try:
        if re.match(r"[a-z0-9]+@[a-z]+\.[a-z]{2,3}", email):

            #Record().add_email(name, email)  # 2
            add_email_DB(name, email)

            print('Email has been added successfully!')
            flash('Email has been added successfully!')
        else:
            raise TelDoesNotMathFormatError

    except TelDoesNotMathFormatError:

        print("Email does not match format - should be 1@1.1")
        flash("Email does not match format - should be 1@1.1")
        TelDoesNotMathFormatError.status = 1

    except KeyError:
        print("User with this email does not exist. Try other option")
        flash("User with this email does not exist. Try other option")

@input_error
def change_email_head(name, email):

    try:
        if re.match(r"[a-z0-9]+@[a-z]+\.[a-z]{2,3}", email):

            #Email().change_email(name, email)  # 2
            change_email_DB(name, email)

            print('Email has been changed successfully!')
            flash('Email has been changed successfully!')
        else:
            raise TelDoesNotMathFormatError

    except TelDoesNotMathFormatError:

        print("Email does not match format - should be 1@1.1")
        flash("Email does not match format - should be 1@1.1")
        TelDoesNotMathFormatError.status = 1

@input_error
def add_adress_head(name, adress):
    #try:
        #Record().add_adress(name, adress)  # 2
        add_adress_DB(name, adress)
        print('Adress has been added successfully!')
        flash('Adress has been added successfully!')


def list_string(list):  # servise function for lookup function
    if list is List:
        return ', '.join(map(str, list))
    else:
        return str(list)


def good_buy_func():
    print('Good bye!')
    flash('Good bye!')
    return 'stop'

def main(command):

    global add_book
    add_book = AddressBook()
    
    ### Reading existed notes
    if(os.path.exists('notes.csv') and os.path.isfile('notes.csv')):
            with open('notes.csv', newline='') as fh:
                reader = csv.DictReader(fh)
                for row in reader:
                    add_book.notes_data[row['tag']] = row['note']


    commands_dict = {'hello': hello_func, 'add': add_func, 'change': change_func,
                     'phone': phone_func,  'good': good_buy_func,
                     'close': good_buy_func, 'exit': good_buy_func, 'addnum': addnum_func, 'del': del_func,
                      'help': help_func, 'lookup': lookup_func,
                     'addnote': addnote_func, 'delnote': delnote_func,
                     'addtag': addtag_func, 'deltag': deltag_func,

                     'delrec': del_record_hand, 'addemail': add_email_head, 'addadress': add_adress_head,
                     'changeemail': change_email_head, 'daysbeforebirth':birthdaylook_func
                     }

    stop_flag = ''

    print("Bot has been started!\nFor additional information enter 'help'")

    load_func()
    #while True:
    try:

        print('')
        command_id, name, phone = command_parser(command)  # passing vars to another func
        for key, value in commands_dict.items():
            if command_id == key and name == '' and phone == '':
                res = value()
                stop_flag = res

            elif command_id == key and name.lower() == 'bay' and phone == '':
                res = value()
                stop_flag = res

            elif command_id == key and name.lower() == 'all' and phone == '':
                res = value()

            elif command_id == key and name != '' and phone == '':
                res = value(name)

            elif command_id == key and name != '' and phone != '':
                res = value(name, phone)

        if command_id not in commands_dict:
            print('I do not know this command!')
            flash('I do not know this command!')

        if stop_flag == 'stop':
            pass
            #break

    except TypeError as err:
        print('Unsuccessful operation. Please, try again')
        flash('Unsuccessful operation. Please, try again')


    except EOFError as e:
        print(e)


if __name__ == '__main__':
    main()
