<img src="https://github.com/yangco-le/query_answering_system/blob/master/img-folder/20200424182322.png" align="middle" />

# Query & Answer System for SJTU


### Technical Description
The development front end is implemented using `html`, `js` and `css`, using the `bootstrap` framework, and the back end using the `django` framework, using the `python` language for implementation.

### Type of Users
The student who asked the question, the student or teacher who answered the question, the system administrator.

### Main Functions
* Register and log in: Users can register an account and log in with the registered account, or log in as a tourist.
* Posting function: The poster will send out his own difficult and confused questions in the form of a post. The poster needs to be classified according to the course to which the question belongs (The course is manually added by the administrator. If there is no such course in the system, the user can apply to the administrator to add it).
* Reply function: users can reply and discuss under the post.
* Modify and delete: Users can modify and delete the questions they post.
* Search function: Users can search for questions raised by other users and their responses through keyword search and course name, and can quickly find the questions they need to query for browsing.
* Reporting function: Users can report posts that violate relevant laws and school rules. The administrator will delete the reported post after verification.
* Like function: Users can like high-quality posts, and posts with more likes can be selected as priority.
* Collection function: Users can bookmark questions, and the bookmarked questions will appear on the personal homepage.
* User homepage: Users can modify their personal information through their homepage settings, view their questions and their responses. At the same time, users can view their favorite posts on the homepage.
