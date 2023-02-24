# Danger Log


#### User may forget his/her account

We find that user may forget his/her username or password, and we do not have the function to let them find their account back. In order to fix it, we may give some rights, such as finding their account by typing email or phone.


#### User email account may be invalid.

When a user tries to register, his/her email account may be invalid. This would make the web can't remind him/her that rides have been confirmed. To avoid this situation, We probably can check the validity of the user email when a user account is being created.


#### User email can be registered more than once.

When a new user start to register, we do not have any limitation about the email, which means an email can be used more than once, which violates some rules of the riding app in the real world. So, we may need to add another condition to make sure we can also use email to login and find users' account.


#### Legal Name may be used more than once

When a user tries to register, we have make sure that his/her user name should not be the same with the user account that already exists in our database. However, for different username, they can edit their profile with the same legal name, which should be invalid and may cause some problems, although some people have the same legal name. To avoid that, we may need to add another condition like ID or driver license to make sure every person only has one account.


#### Less security about the database for url

User can change the url to view other data from database after logging, which did not guarantee the security of database in real world. Therefore, in real world, we need to add some limitation about the url access rights to avoid revealing the data.


#### Didn't check the validity of license plate number

In real world, the license plate number of a vehicle should be valid, which means that it must be officially registered, so that the platform could have better supervision on drivers. However on our web, we just accept any string the user type in, even all of it is number. In other words, we just allowed anyone to be a driver. This could cause huge danger problem. To eliminate this, we need the help of the official department to check the validity of the license plate number.


#### Didn't check the validity of destination

When a user tried to start a ride, this system would not check the validity of destination, which may cause problems to make this ride invalid. To eliminate this, we think it's better to add a process to check if the destination exist in the google map or not.


### Did not have the checking process of the time

After the arrive time of the request ride, this order will not disappear even if it is the past time. To avoid this, it's better to add a function to check the time by ascending order and drop the order from the order lists if time is up.



#### Driver can hold multiple rides whose driving period overlap

Driver could hold multiples ride at the same time. This may cause problem when two rides' arrival time are too close. In this circumstance, it will be impossible for a driver to accomplish these rides all on time. Our web should be able to forbid a driver to get rides that may conflict with each other. To achieve this, we may need information like how long it usually takes from one place to another and do complicated computation to decide whether two rides will have overlap.
