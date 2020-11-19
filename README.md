# sqlalchemy-challenge

# Climate Analysis and Exploration
    #   Use Python and SQLAlchemy to do basic climate analysis and data exploration of your climate database. All of the following analysis should be completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.

# Precipitation Analysis
    # Design a query to retrieve the last 12 months of precipitation data.
    # Select only the date and prcp values.
    # Load the query results into a Pandas DataFrame and set the index to the date column.
    # Sort the DataFrame values by date.
    # Plot the results using the DataFrame plot method.
    
# Station Analysis
    # Design a query to calculate the total number of stations.
    # Design a query to find the most active stations.
    # List the stations and observation counts in descending order.
    # Which station has the highest number of observations?
    # Hint: You will need to use a function such as func.min, func.max, func.avg, and func.count in your queries.
    # Design a query to retrieve the last 12 months of temperature observation data (TOBS).
    # Filter by the station with the highest number of observations.
    # Plot the results as a histogram with bins=12.
    
# Bonus Temperature Analysis I
    # Hawaii is reputed to enjoy mild weather all year. Is there a meaningful difference between the temperature in, for example, June and December?
    # You may either use SQLAlchemy or pandas's read_csv() to perform this portion.
    # Identify the average temperature in June at all stations across all available years in the dataset. Do the same for December temperature.
    # Use the t-test to determine whether the difference in the means, if any, is statistically significant. Will you use a paired t-test, or an unpaired t-test? Why?
    
    
# Climate App
    # design a Flask API based on the queries that you have just developed
    
# Set Routes
    # Home page
    # Precipitation
    # Stations
    # Tobs
    # Start and Start-End
        # Calculates mix, max, avg temperature for dates later than start date, or between start-end dates 


