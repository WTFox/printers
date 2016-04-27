# A python module for Ricoh Printers

## Example 
```python
    from printers import Ricoh
    
    r = Ricoh('10.10.2.13', 'admin', 'pass')
    
    # prints out the length of users in the address book
    print(len(r.users))
     
    # print out the user's names
    for user in r.users():
        print(user['name'])
    
    # add a user
    r.add_user(userid='pcouts', name='Patricia Couts', displayName='Patricia C') 
    
    # delete user (by id)
    r.delete_user(138) 
    
    r.disconnect()
```