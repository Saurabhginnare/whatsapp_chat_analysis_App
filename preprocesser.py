import re
import pandas as pd


def perprocess(data):
    pattern = "\\d{2}/\\d{2}/\\d{4}, \\d{2}:\\d{2}"
    dates = re.findall(pattern, data)
    messages = re.split(pattern, data)[1:]
    
    pattern = re.compile(r'\u202fam - (.*?): (.*)')

    # Extracted messages list
    extracted_messages = []
    # Loop through each message and apply the regex
    for message in messages:
        match = pattern.match(message)
        if match:
            name = match.group(1)
            msg = match.group(2)
            extracted_messages.append(f'{name}: {msg}')
    

            # Define the regex pattern to match the unwanted part and extract name and message
            pattern = re.compile(r'\u202fam - (.*?): (.*)')

            # Extracted messages list
            extracted_messages = []

            # Loop through each message and apply the regex
            for message in messages:
                match = pattern.match(message)
                if match:
                    name = match.group(1)
                    msg = match.group(2)
                    extracted_messages.append(f'{name}: {msg}')
            
            trimmed_dates = dates[:len(extracted_messages)]


                        # Function to convert date format
            from datetime import datetime
            def convert_date_format(date_str):
                # Parse the date string to a datetime object
                dt = datetime.strptime(date_str, '%d/%m/%Y, %H:%M')
                # Format the datetime object to the desired format
                return dt.strftime('%Y-%m-%d %H:%M:%S')

            # Convert all dates in the list
            converted_dates = [convert_date_format(date) for date in dates]
            

            converted_dates = converted_dates[:len(extracted_messages)]
            

            # Create a DataFrame
            df = pd.DataFrame({
                'user_message': extracted_messages,
                'message_date': converted_dates
            })

            df.rename(columns={'message_date': 'date'},inplace=True)

            users = []
            messages = []
            for message in df['user_message']:
                entry= re.split('([\W\W]+?):\s',message)
                if entry[1:]:
                    users.append(entry[1])
                    messages.append(entry[2])
                else:
                    users.append('group_notification')
                    messages.append(entry[0])
            df['user'] = users
            df['message'] = messages

            df.drop(columns=['user_message'], inplace=True)



            # Function to split message into user and message content
            def split_message(msg):
                match = re.match(r'(.*?): (.*)', msg)
                if match:
                    user = match.group(1)
                    message_content = match.group(2)
                    return pd.Series([user, message_content], index=['user', 'message_content'])
                else:
                    # If the format is not as expected, return None for user and the full message as message_content
                    return pd.Series([None, msg], index=['user', 'message_content'])

            # Apply the function to the 'message' column
            df[['user', 'message_content']] = df['message'].apply(split_message)

            # Drop the original 'message' column if no longer needed
            df.drop(columns=['message'], inplace=True)

            df['date'] = pd.to_datetime(df['date'])
            df['year'] = df['date'].dt.year
            df['month'] = df['date'].dt.month_name()
            df['day'] = df['date'].dt.day
            df['hour'] = df['date'].dt.hour
            df['minute'] =df['date'].dt.minute
            df.rename(columns={'message_content':'message'},inplace=True)
            return df