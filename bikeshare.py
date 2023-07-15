import time
import pandas as pd
import datetime as dt

# enables to print all columns of the dataframe
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# declare variables
city_options = {
    1: 'Chicago',
    2: 'New York City',
    3: 'Washington'
}

month_options = {
    0: 'all',
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June'
}

day_options = {
    0: 'all',
    1: 'Sunday',
    2: 'Monday',
    3: 'Tuesday',
    4: 'Wednesday',
    5: 'Thursday',
    6: 'Friday',
    7: 'Saturday'
}

city2data = {
    'Chicago': 'chicago.csv',
    'New York City': 'new_york_city.csv',
    'Washington': 'washington.csv'
}

def print_menu(menu):
    """Function to print the appropriate and formatted menu based on input parameter."""

    # print the related menu based on input parameter
    if menu == 'city':
        for key in city_options.keys():
            print (key, '-', city_options[key])
    elif menu == 'month':
        for key in month_options.keys():
            print (key, '-', month_options[key])
    else:
        for key in day_options.keys():
            print (key, '-', day_options[key])

def convert_seconds(title,nsec):
    """Function to convert number of seconds in a human readable format."""
    
    # convert input in INT datatype
    sec = int(nsec)
    # create timestamp string based on input express in seconds
    str_tm = str(dt.timedelta(seconds=sec))
    # added an IF condition to manage if day should be calculate or not
    if nsec >= 86400:
        # splits timestamp string by ',' and assigns the first part
        day = str_tm.split(',')[0]
        # splits timestamp string by ',' to gets the second part and splits it by ':' to obtain hour, minute and second
        hour, minute, second = str_tm.split(',')[1].split(':')
        print(title, f'{day}{hour} hour {minute} min {second} sec')
    else:
        # since the number of second is less 1 day, the timestamp string is composite from hour, minute and seconds only
        hour, minute, second = str_tm.split(':')
        print(title, f'0 days {hour} hour {minute} min {second} sec')

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        print('\nWould you like to see data for Chicago, New York, or Washington?\n')
        print_menu('city')
        option = ''
        try:
            option = int(input('\nEnter a value (1 - 3):\n'))
        except ValueError:
            print ('Invalid input. Enter a value between 1 - 3')
            continue
        # check
        if not option in range(1, 4):
            print ('Invalid input. Enter a value between 1 - 3')
            continue
        else:
            city = city_options[option]
            break


    # get user input for month (all, january, february, ... , june)
    while True:
        print('\nWhich month would you like to filter by? Type number between 1 - 6 or type 0 if you do not have any preference?\n')
        print_menu('month')
        option = ''
        try:
            option = int(input('\nEnter a value (0 - 6):\n'))
        except ValueError:
            print ('Invalid input. Enter a value between 0 - 6')
            continue
        # check
        if not option in range(0, 7):
            print ('Invalid input. Enter a value between 0 - 6')
            continue
        else:
            month = month_options[option]
            break


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        print('\nAre you looking for a particular day? Type number between 1 - 7 or type 0 if you do not have any preference?\n')
        print_menu('day')
        option = ''
        try:
            option = int(input('\nEnter a value (0 - 7):\n'))
        except ValueError:
            print ('Invalid input. Enter a value between 0 - 7')
            continue
        # check
        if not option in range(0, 8):
            print ('Invalid input. Enter a value between 0 - 7')
            continue
        else:
            day = day_options[option]
            break


    print('='*40)
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
    
    # load data file into a dataframe
    df = pd.read_csv(city2data[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('Most common month:', month_options[common_month])

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most common day of week:', common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('Most common hour:', common_hour)

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('='*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station:', common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Most commonly used end station:', common_end_station)

    # display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station'] + '~' + df['End Station']
    common_combination = df['combination'].value_counts().idxmax()
    common_combination_splitted = common_combination.split('~')
    print('Most commonly used combination of start station and end station trip respectively:')
    print('=> Start Station: ', common_combination_splitted[0])
    print('=> End Station  : ', common_combination_splitted[1])

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('='*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    convert_seconds('Total travel time: ', sum(df['Trip Duration']))
    
    # display mean travel time
    convert_seconds('Mean travel time: ', round(df['Trip Duration'].mean()))

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('='*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types
    cnt_users = df['User Type'].value_counts()
    print('Count of user types:\n', cnt_users)

    # display counts of gender
    try:
        cnt_gender = df['Gender'].value_counts()
        print('\nCounts of gender:\n', cnt_gender)
    except KeyError:
        print('\nCounts of gender:\n=> No data available for these filters')

    # display earliest, most recent, and most common year of birth
    try:
        earliest_yr = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        most_common = df['Birth Year'].value_counts().idxmax()
        print('\nSome statistics about Year Of Birth:')
        print('=> Earliest year of birth: ', earliest_yr)
        print('=> Most recent year of birth: ', most_recent)
        print('=> Most common year of birth: ', most_common)
    except KeyError:
        print('\nSome statistics about Year Of Birth:\n=> No data available for these filters')


    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('='*40)


def print_raw_data(df):
    """Ask user if they want to see a sample of 5 lines of raw data."""

    # setup row index
    row_idx = 0

    # remove columns not involved in the original raw data. Using inplace option to avoid df reassignment
    df.drop(['month','day_of_week','hour','combination'], axis=1, inplace=True)

    # setup total rows
    total_row = df.shape[0]

    # gets the input
    row_display = input('\nDo you want to see five lines of raw data? Yes or No:\n').lower()

    while True:
        # if input not matches, repeat the question
        if row_display not in ['yes', 'no']:
            row_display = input('Invalid input. Please type Yes or No: ').lower()

        # if YES, shows raw data
        elif row_display == 'yes':

            # exit-condition for reaching the end of the file
            if row_idx >= total_row:
                print('\nThe end of the raw data has been reached, there are no more lines to display\n')
                return
            else:
                print(df.iloc[row_idx : row_idx + 5])
                row_idx += 5

            # again
            restart = input('\nDo you want to see more? Yes or No?\n').lower()
            if restart == 'no':
                break
            elif restart == 'yes':
                row_display = 'yes'
            else:
                row_display = input('Invalid input. Please type Yes or No: ').lower()
        # if NO, exit
        elif row_display == 'no':
            return


def main():
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        city, month, day = get_filters()
        print('\nYour choices are: City => \'{}\' | Month => \'{}\' | Day => \'{}\''.format(city, month, day))
        df = load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        print_raw_data(df)

        restart = input('\nWould you like to restart? Enter Yes or No.\n').lower()
        if restart != 'yes':
            break


if __name__ == "__main__":
    main()
