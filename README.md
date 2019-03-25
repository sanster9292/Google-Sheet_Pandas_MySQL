# Google-Sheet_Pandas_MySQL
# Pull data from Google Sheet and use pandas to data wrangle and upload to your database.

The purpose of this project is to show my work which I did to upload the data of a google sheet into a database using MYSQL and the google sheets api. 

# THE MOTIVATION:
    •  I have been keeping track of all the books that I am reading or have read. 
    •  Some past entries I am making based on memory, but I had a google sheet for all the books I read in 2017.
    •  In 2017 I had tried reading a book a week and I logged all the entries in a google sheet.
    •  Though, I was only able to read 33 books instead of the 52 I had hoped, but I was happy with the experience and also by        the record which I had kept. 
    
# THE THINKING
    • I had a database established where i was keeping a record of my books which I was currently reading and updating it with        entries from the past and as I remembered them. 
    • The schema of the database had 6  columns.
        ◦ ID(auto generated)
        ◦ Book ID
        ◦ Author
        ◦ Genre(upto 3 to describe the book)
        ◦ thoughts about the book.
        ◦ Date: When the entry was added in the dataabase.
    • I wanted to store the information in my google sheet in this schema. 
    
# THE PROCESS:
    • I used the Google Sheet API to load the data from the google sheet. 
    • Then, I loaded the data into Python Pandas’ for easier manipulation.
    • Once I had wrangled the data from the sheet to match the schema, I used SQLAlchemy and Pandas’ to_sql function to upload the data to my database. 
