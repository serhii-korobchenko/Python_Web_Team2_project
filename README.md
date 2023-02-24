# Python_Web_Team2_project
`Personal assistant`

`Purpose:` Assist in keeping personal information regarding contacts, notes, files and latest news (using web cli cmd)

Used Technologies: Python, Flask, bcrypt, beautifulsoup, Jinja2, marshmallow, pandas, psycopg2, requests, SQLAlchemy, PostgreSQL (Elephantsql), etc.


`Installation:`
- option 1: use code from the repository (run app_flask)
- option 2: use Docker image on DockerHub: docker pull jchild2008/cliwebbot-image:1.0.

`Operations CLI:`
    - bot understands commands:
    
                           - "hello" - answer: "How can I help you?
                           - "add' name telephone number" - save new contact
                           - "change' name telephone number" - change telephone number for existed contact
                           - "addnum' name telephone number" - add additional  tel number for certain contact
                           - "del' name telephone number" - del tel number for certain contact
                           - "help" - bot show commands explanations
                           - "lookup' text" - find text in records (no difference which case of characters)
                           - "delrec' name" - delete record from AddressBook
                           - "addemail' name email" - add email to record
                           - "changeemail" name new_email - change all emails on new one
                           - "addadress' name text" - add address  to record
                           - "changeadress' name new_address" - change  adress
                           - "addbirthday' name " - add birthday to record
                           - "findbytag' tag" - looking for note by tag
                           - "delbirthday' name" - delete birthday from record
                           - "daysbeforebirth" # days" - check birthdays in time period
                           - "addnote' note_title text" - add note to DB
                           - "delnote' note_title - del note from DB
                           - "addtag' text note title " - add tag to Note
                           - "deltag' text" - del tag from DB
                           - "good bye" or "close" or "exit" - bot stops work and message "Good bye!"
                           
     - interactive: outlook contacts, notes, videos, pictures, files, news (BBC world)
     
