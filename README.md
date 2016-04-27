# A python module for Ricoh Printers

## Example 
```python
    printer_ip = '10.10.2.8'
    with Ricoh(printer_ip, 'admin', '') as r:
        print("There are {} users in {}".format(len(r)), printer_ip)
        # There are 94 users in 10.10.2.8
        
        print(r)
        # <Ricoh(10.10.2.8)> at 51355824
      
        for user in r.users():
            print(user['name'])
            # print out the user's names
        
        # add a user
        r.add_user(userid='jean', name='James Dean', displayName='James D', email='jdean@gmail.com') 
        
        # delete user (by id)
        r.delete_user(138) 
```