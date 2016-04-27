# Ricoh

## About
Whenever my organization hires or fires someone, I have to go into each of our 5 printers and add/remove the user. This is often the step I forget to do, and it's definitely the one I like the least. 

So I've written a python wrapper for dealing with these machines from Hell. 

## Compatibility
This works on the following models:

* Ricoh Aficio MP 6002
* Ricoh MP C6502
* Ricoh Aficio MP 9002

## Installation
```bash git clone https://github.com/WTFox/printers.git
cd printers
python setup.py install
```

## Usage 
```python from printers import Ricoh

printer_conn = dict(
    host='10.10.2.13',
    username='admin',
    password=''
)

# Access via context manager so that all connections are closed automatically.
with Ricoh(**printer_conn) as ricoh:
    print(repr(ricoh))
    # <Ricoh(10.10.2.8)> at 51441168
    
    print(ricoh)
    # There are 94 users in 10.10.2.8
    
    print(len(ricoh))
    # 94
    
    for user in ricoh:
        print(user.id, user.name)
        # 1 John Doe
        # 2 Billy Bob
        # 3 ...
        
        # add a user
        r.add_user(userid='jean', name='James Dean', displayName='James D', email='jdean@gmail.com') 
        
        # delete user (by id)
        r.delete_user(138) 
```

Contact me [here](anthonyfox1988@gmail.com) for questions or concerns. Thanks!