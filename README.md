# sqlalchemy-challenge - Assignment 10
This challenge have 2 parts.
   Part 1: Analyze and Explore the Climate Data
   Part 2: Design the Climate App
In part 1
      I have used the provided files (climate_starter.ipynb and hawaii.sqlite) to complete my climate analysis and data exploration.

     Use the SQLAlchemy create_engine() function to connect to my SQLite database.

     Use the SQLAlchemy automap_base() function to reflect the tables into classes, and then save references to the classes named station and measurement.

     Link Python to the database by creating a SQLAlchemy session.

     Perform a precipitation analysis and then a station analysis by completing the steps in the following two subsections.
     
 In part 
     After completed the initial analysis, I've designed a Flask API based on the queries that I just developed. To do so, use Flask to create my routes as follows:

        1. Main Route /
        2. Precipitation Route
        3. Precipitation Route
        4. Stations Route
        5. Tobs Route
        6. start and end  Route(User can give a start date/end date ibn the data set and get the min,max,ave tempretaures.
