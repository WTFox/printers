# A python module for Ricoh Printers

## Example 
```python
    printer_ip = '10.10.2.8'
    
    with Ricoh('10.10.2.8', 'admin', '') as ricoh:
        print(repr(ricoh))
        # <Ricoh(10.10.2.8)> at 51441168
        
        print(ricoh) 
        # There are 94 users in 10.10.2.8
        
        print(len(ricoh))
        # 94 
        
        for user in ricoh:
            print(user.name)
        
        # John Doe
        # Billy Bob
        # ...
        
        # add a user
        r.add_user(userid='jean', name='James Dean', displayName='James D', email='jdean@gmail.com') 
        
        # delete user (by id)
        r.delete_user(138) 
```