
import sqlite3


import sqlite3
s3 = sqlite3.connect('test.db')
s3.execute('CREATE TABLE person (person_id INTEGER PRIMARY KEY, name TEXT, height REAL)')
result = s3.execute('INSERT INTO person VALUES (NULL, ?, ?)', ('Jean-Luc', 187))
print(result.lastrowid)
# 1
s3.execute('INSERT INTO person VALUES (NULL, ?, ?)', ('Jodie', 185.5))
data = {'name': 'fred', 'height': 155.2}
result = s3.execute('INSERT INTO person VALUES (NULL, :name, :height)', data)

# could be a list of lists or list of tuples
# or list of dictionaries if you use the :parameter format above in the query
data = [('sam', 155.2), ('martha', 141.2)]
result = s3.executemany('INSERT INTO person VALUES (NULL, :name, :height)', data)
print(result.rowcount)
# 2

# showing a select witn one parameter (a tuple that has just one thing in it)
result = s3.execute("SELECT * FROM person WHERE height > ?", (159,) )
rows = result.fetchall()
print(rows)
# [(1, 'Jean-Luc', 187.0), (2, 'Jodie', 185.5)]

# showing a new table that has some missing data
s3.execute('CREATE TABLE ages (ages_id INTEGER PRIMARY KEY, name TEXT, age INTEGER)')
data = [
    ('Jean-Luc', 23),
    ('sam', 31),
    ('john', 31),

    ('martha', None),  # None will get changed to NULL
    ('jim', 12),       # note a trailing comma is okay even tho no next thing
]
s3.executemany('INSERT into ages VALUES (NULL, ?, ?)', data)
# to match NULL you have to use "is NULL" or "is not NULL"
result = s3.execute("SELECT  * from ages where age is NULL")
result.fetchall()
# [(3, 'martha', None)]

# to join and sort it's best to add an index to columns you join on.
s3.execute("CREATE  INDEX person_name_index ON person(name)")
# in a UNIQUE index only one of each value can be present.
s3.execute("CREATE UNIQUE INDEX ages_name_index ON ages(name)")

# connect the person table to the ages table
#   using the name field as a key between the two.
#   If there's more than one matching row in either table both will be in the result.
result = s3.execute("""
    SELECT person.name as name, person.height as hgt, ages.age as age
    FROM  person 
    inner join ages on ages.name = person.name
    """)
# connect the person table to the ages table
#   using the name field as a key between the two.
#   If there's no matching row in ages though, that row will have None entries.

result = s3.execute("""
    SELECT person.name as name, person.height as hgt, ages.age as age
    FROM  person 
    left join ages on ages.name = person.name
    order by ages.age
    """)
rows = result.fetchall()
# [('Jean-Luc', 187.0, 23), ('Jodie', 185.5, None), ('fred', 155.2, None),
# ('sam', 155.2, 31), ('martha', 141.2, None)]

# you can get a list of the headings with a list comprehension
#    which builds a list out of an embedded for loop.
headings = [d[0] for d in result.description]  # get the column headings
# ['name', 'hgt', 'age']


# Would be nice:  connect the person table to the ages table
#   using the name field as a key between the two.
#   If there's no matching row in either table though, that row will have None entries.
# SQLite does not support this, but other DBs do.
result = s3.execute("""
    SELECT person.name as name, person.height as hgt, ages.age as age
    FROM  person 
    outer join ages on ages.name = person.name
    """)

result = s3.execute("""
    SELECT person.name as name, person.height as hgt, ages.age as age
    FROM  person 
    join ages on ages.name = person.name
    """)
# sqlite3.OperationalError: RIGHT and FULL OUTER JOINs are not currently supported

# update rows - showing how you can do wildcards with where clause
result = s3.execute("UPDATE ages SET age=45 where name='jodie'")
result = s3.execute("UPDATE ages SET age=3 where name LIKE '%ed%'")

# delete
result = s3.execute("Delete from person where height > 160")
print(result.rowcount)
# 2

# if you do not put your changes inside a with statement, you must commit any changes.
s3.commit()


# select resutls are iterable
s3 = sqlite3.connect('test.db')
people = s3.execute("select person_id, name, height from person")
for p in people:
    (person_id,name,height) = p
    print(f"  {person_id}  {name}  {height}")
