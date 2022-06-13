# Web-App-Assessmen tReport



This report intends to explain the work and intentions taken related to the case study of the Web App creation for a local community allowing two interfaces. When deciding on a webapp it is ideal to select the routing and functions that are far easier and less complex for users to utilise than the intended use. 

Athlete Interface:

The Webapp created, first routing and functions reqiures to divided into two major interface users. One is for general viewing purposes and editing non-sensitive personal information such as bio data. The users with simpler uses of the 
system identified as atheletes.
Hence main route ('/') will direct to athlete users allowing them to use with minimal functionality. 

@app.route("/")
Default route: 

With the route  ('/'), concluded to include an admin login intended for advanced users, yet due to potential compromise with absence of a password to login to the system default page will be presented with a dropdown with user names. 

The design of the webapp is to include a drop down for users to login to the system selecting their name. Dropdown menu accomodated with a submit button for users to view the events. The select query passed to obtain teh firstname and lastname and called by the index number in the html template. Boostrap file link utilised in all the pages to provide a better user experience. 

User would expect to have access to the system without any password requirements. Hence no password or security questions are provided as premeasures to avoid the confusion advsied to select the name from the dropdown. 

There are two main factores that would need to fullfill with the athelete interface. One expectation is to provde users the ability to view the completed and upcoming events when they select and enter in to the system. On the other hand, we would allow users to edit their information. The users  who would have like to contact the community management for any queries or to raise concerns.

Therefore, I divded the bottom of the page on each access using navigation bars and providing the contact information as use of the space that remained. 

When the user enter to the portal via the dropdown menu choosing the name, it would have been ideal display a customised message saying Welcome __ __ !. At the time of the writing, above idea wasn't implemented on this web application.

Utilising the function 'pastevents' accessed via the route athlete/events produced the interface to show past events and upcoming events with necessary information. Also, used 'get' method to obtain the data and the union function to join multiple data sets to display the key fields most suitable for the users.  Future events are assumed that of from today or the current date of the athlete veiwing the information, hence appropriate parameters utilsied to show the tables based on past and future. The space of the web interface divided in to two tables and showed by rendering the athelete_events html. 

As the user, an athelete has now already chosen the name to enter to the system, and suddenly decided to change details after rembered or seeing some information missing in the name after seeing the events table. In hypothetical scenarios a user will have to reenter the name, and finding the correct place to navigate to to change the information could be complicated and difficult to find takinga glance.

Hence used navigation bars in to return to menu is seen as ideal underneath tables. Created two navigation keys to return back to the athlete login page should the user have mistakeenly chosen the incorrect name.  Ther remaining navigation key named "update details" and passed the function 'athleteUpdate' acces via '/athlete/update. As the athlete would be already in the designated user portal,  it would be convinient for the user and would also minimise the error ratio due to user friendly interface. By clicking the button 'update the details' it would call the function used as form to fill the provided fields. 

Admin Interface:

Admin route is accessed via route("/admin") and has decided to not to provide the navigational key in the athlete interface. After careful consideration, implemented a return button to athelete page via admin page using the quick navigation. 

On top of the admin interface, provided a dropdown to accomodate the function "adminUpdate".  

In this scenario, a dropdown helps the navigator or a admin user who can identify and conviniently be able to viewi  through dropdown menu using the first and last name. Then this would allow the user to call 'get' and 'post' function and update the fields available in the form.

 Next, I utilised a wide naigational panel to call the functions related to adding a new user or event. 

 The navigation keys were reating to three sperate forms with the same function of adding events or users. The 'add' part allows admin users to return to once place to add any of the information using quick navigation. Using ref functoin all the added forms are called inside the main html document (admin_home_) and then directed to the user to the specific site. Then additional navigation keys are provided at each form end to return back to the main page. 

For non qualifying users parameter used where pointstoqualify > pointsscore, allowed admin to change the fields related to the points.

Regards to the reports decided to include links to navigate to each function and displayed the information as tables for more viewing comfort. 

In order to list the team members by name according to the first name and last name a for loop utilised and then only included the list by first name option in the main admin interface. If a user click the navigation it will lead to the table with all team names listed by first name grouped by teams. And the navigation key to change the viewing to view by last name provided at bottom vice versa for the both pages. 

Understood that the assessor and admin users would be more convinced and make key decisions if we were to design the medal counts and qualification information grouped by the individual user for each calling parameter with the "functions" of the  countbyesrs and reportselection. 

Using the union and join function, report aims to provide a table output of the aviailbale data grouped by the relevent selector. 

In conclusion, html scripts has allowed the sql outputs to be precisely positioned  in tables and displaying the content in an organised manner. Further, due to lack of CSS utilsisation colour and design use within the interface could reduce the user experience and the experience. 
