import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
  
    print('Hello! Let\'s explore some US bikeshare data!')

    # make sure that the inputs (city, month & day) from the user is true.....
    # through making lists and compare the user inputs with the lists and give the user hint if it's invalid input...
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ['chicago,new york city, washington']
    city = input( "which of these citys do you choose chicago,new york city, washington: \n ")
    while city not in CITY_DATA.keys():
        print("invalid city!")
        #city = input("which of these citys do you choose chicago,new york city, washington:  ").lower().strip()
        if city not in CITY_DATA:
            print('Wrong City Name Please Enter a Valid City Name')

        city = input('Would you like to see data for (Chicago, New York City, or Washington)?:   \n').lower().strip()
        # elif city in CITY_DATA:
        #   break
        # else:
        #   print("Sorry it is invalid city!, kindly write the right city from (Chicago, New York City, or Washington)")
        # get user input for month (all, january, february, ... , june)


    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month =  input('Which month? (January, February, March, April, May, June, or all) :   \n').lower().strip()
        if month in months:
            month = months.index(month) + 1
            break
        else:
            print("Sorry it is invalid month!, kindly write the right month among the first 6 months")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday','All']
    while True:
        day = input('Which day? (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or all) :   \n').title().strip()
        if day in days:
            break
        else:
            print("Sorry it is invalid day!, kindly write the right day name of week")

    print('-'*40)
    return city, month, day
    

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load the CITY_DATA file into data frame
    df = pd.read_csv(CITY_DATA[city]) 
    # convert Start Time coln. to datetime
    df['Start Time']= pd.to_datetime(df['Start Time'])
    # extract month name from Start Time coln. into new one
    df['month']= df['Start Time'].dt.month
    # extract day name of week from Start Time coln. into new one
    df['day_name']= df['Start Time'].dt.day_name()
    # extract start hour from Start Time coln. into new one
    df['hour']= df['Start Time'].dt.hour

    #conditional statement to make sure that the inputs are valid and make a data frame by filterring 
    # filter by month
    if month != 7 :
        #months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
        #month = months.index(month) + 1
        print(month)
        df= df[df['month'] == month]

    # filter by day
    if day != 'All':
        df = df[df['day_name'] == day]

    print(df.head())
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    # extraxt some descriptive statistics about the most common month, day and hour of renting bikes
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month of year
    common_month = df['month'].mode()[0]
    print('The common month is {} \n'.format(common_month))

    # display the most common day of week
    common_day_of_week = df['day_name'].mode()[0]
    print('The common day of week is {} \n'.format(common_day_of_week))

    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('The common hour is {} \n'.format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    # extraxt some descriptive statistics about the most common start and end station
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('The most popular Start Station is {} \n'.format(common_start_station))
     
    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('The most popular End Station is {} \n'.format(common_end_station))

    # display most frequent combination of start station and end station trip
    combination_SS_ED = df.groupby(['Start Station','End Station']).size().sort_values(ascending=False).head(1)
    #.nlargest(1)    #.sort_values(ascending=False), .size().idxmax()   
    print('The frequent combination of start station and end station trip is {}'.format(combination_SS_ED))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    # extraxt some descriptive statistics about the total and average time the trip takes

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum().round()
    print('The total trip duration is: {} \n'.format(total_travel_time))

    # display mean travel time
    average_mean_time = df['Trip Duration'].mean()
    print('The average trip duration is: {} \n'.format(average_mean_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    #print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    #count how many subscribers and customers using the system
    users_type = df['User Type'].value_counts().to_frame()
    print('The counts of user types are: {} \n'.format(users_type))

        #Display counts of gender
        #using (if) conditional statement because the gender and year of birth are given data only in chicago & new york city
        #have to make sure taht this function is running only for only those 2 cities ti avoide any error
    if city == 'chicago' or city == 'new_york_city':
        gender = df['Gender'].value_counts().to_frame()
        print('The counts of gender are: {} \n'.format(gender))

        #Display earliest, most recent, and most common year of birth
        year_of_birth = df['Birth Year']
        earlist_year_of_birth = year_of_birth.max()
        most_recent_year_of_birt = year_of_birth.min()
        most_common_year_of_birt = year_of_birth.mode()[0]
        print('The earliest year of birth is: {} \n'.format(earlist_year_of_birth))
        print('The most recent year of birth is: {} \n'.format(most_recent_year_of_birt))
        print('The most common year of birth is: {} \n'.format(most_common_year_of_birt))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df) :
#this this raw data function to ask the user if wants to see the raw data if yes 
#will print 5 raws and ih yes again will print 5 extra 5 rwas, finally if no
#will break from the loop and function.............  
    print(df.head())
    count = 0
    while True:
        view_raw_data = input('\nWould you like to view next five row of raw data? Enter yes or no.\n')
        if view_raw_data.lower() != 'yes':
            print('Thank you for you interset:)')
            break
        count = count + 5
        print(df.iloc[count:count+5])


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
                
       
            
        print(df.head())

if __name__ == "__main__":
    main() 
