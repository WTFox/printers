#!/usr/bin/python
from printers import Ricoh

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
    ricoh.add_user(userid='jean', name='James Dean', displayName='James D', email='jdean@gmail.com')

    # delete user (by id)
    ricoh.delete_user(138)
