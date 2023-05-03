#  Postman Testing
To run this API, use the command : 

```python
python manage.py runserver 8001
```


If you wish to test the APIs using Postman, follow the instructions below:

1- Create a superuser by using the command python manage.py createsuperuser.

2- To get all jobs, use the URL "http://127.0.0.1:8001/api/jobs/".

3- To get a job by ID, use the URL "http://127.0.0.1:8001/api/jobs/str:id/".

4- To get job statistics, enter a job stats through the URL "http://127.0.0.1:8001/api/stats/str:topic/".

## To test the next URLs, you must be logged in.


- To register, use the URL "http://127.0.0.1:8001/api/auth/register/". Add the fields "first_name", "last_name", "password", and "email" in Postman Body's form-data.

- To get the access token of a particular user to log in add the fields "username" ( your email ) and "password" to body then use the URL "http://127.0.0.1:8001/api/token/". Then, add the access token to Postman headers: "Authorization" : "Bearer Token".

5- To update a job, use the URL "http://127.0.0.1:8001/api/jobs/str:id/update/".

6- To add a job, use the URL "http://127.0.0.1:8001/api/jobs/addjob/".

7- To delete a job, use the URL "http://127.0.0.1:8001/api/jobs/str:id/delete/".

8- To apply to a job, use the URL "http://127.0.0.1:8001/api/jobs/str:id/apply/".

9- To get a list of jobs to which the user has applied, use the URL "http://127.0.0.1:8001/api/me/jobs/applied/".

10- To get a list of a user's jobs, use the URL "http://127.0.0.1:8001/api/me/jobs/".

11- To check if a user has applied to a job or not, use the URL "http://127.0.0.1:8001/api/jobs/str:id/check/".

12- To get a list of candidates who have applied to a particular job, use the URL "http://127.0.0.1:8001/api/job/str:id/candidates/".

13- To upload a resume, use the URL "http://127.0.0.1:8001/api/upload/resume/" using form-data in Postman with the KEY "resume" and VALUE "resume.pdf".

14- To get the current user, use the URL "http://127.0.0.1:8001/api/me/".

15- To update a user, use the URL "http://127.0.0.1:8001/api/me/update/".

# GeoLocation Package

- To install the gdal geolocation package in the gdal folder install it running this command :
 
```python
pip install  GDAL-3.4.3-cp311-cp311-win_amd64.whl
```


## Still in review: It isn't done yet.