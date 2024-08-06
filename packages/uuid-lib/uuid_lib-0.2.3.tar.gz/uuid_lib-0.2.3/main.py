from uuid_lib import *
from uuid import uuid4

print(f'uuid1: {uuid1()}')
print(f'uuid2: {uuid2()}')
print(f'uuid3: {uuid3()}')
print(f'uuid4: {uuid4()}')
print(f'uuid5: {uuid5()}')
print(f'uuid6: {uuid6()}')
print(f'uuid7: {uuid7().__repr__()}')
print(f'uuid8: {uuid8(uuid4().bytes)}')

print(uuid7().__hash__())
print(type(uuid7()))


for i in range(10):
    print(uuid7())