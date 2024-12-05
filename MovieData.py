from header import *

'''
Author: Tina Nosrati
Last Update: 11/8/2024

Description: 
This script will prepare general movie information
'''


##########call_database##########
'''
Arguments:
input:

Output: connection and cursor to work with database

Description: 
This function will connect to database

'''
def call_database():
    conn = psycopg2.connect(
    host="localhost",
    dbname="moviedata",
    user="postgres",
    password="1234",
    port=5432)
    cur = conn.cursor()
    return conn,cur


##########get_movie_info##########
'''
Arguments:
input:
imdb_id --> id of the selected movie

Output: A dataframe containing information for the selected movie

Description: 
This function will return a dataframe of information for a selected
movie from the database.
'''

def get_movie_info(name):
    imdb_id=find_movie_id(name)
    try:
        conn, cur = call_database()
        query = "SELECT * FROM movies WHERE imdb_id = %s"        
        cur.execute(query, (imdb_id,))       
        rows = cur.fetchall()     
        column_names = [desc[0] for desc in cur.description]     
        df = pd.DataFrame(rows, columns=column_names) 
        df = df.sample(frac=1).reset_index(drop=True) 
        df = df.drop(['adult','belongs_to_collection',
                      'id','popularity', 'poster_path', 'production_companies',       
       'production_countries','spoken_languages', 'status','video',], axis=1)
        return df
    
    except OperationalError as e:
        print("An operational error occurred:", e)
    except Error as e:
        print("A database error occurred:", e)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

##########find_movie_id##########
'''
input:
name --> name of the movie we are processing

output: imdb_id of the movie

Description:
This function will return the id of the movie from
the database using the movie name
'''
def find_movie_id(name):
    try:
        conn,cur=call_database()
        query = "SELECT * FROM movies WHERE original_title = %s"        
        cur.execute(query, (name,))  
        rows = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        df = pd.DataFrame(rows,columns=column_names)
        return df.loc[0,'imdb_id']
    except OperationalError as e:
        print("An operational error occurred:", e)
    except Error as e:
        print("A database error occurred:", e)
    finally:
        cur.close()
        conn.close()

##########clean_dictionary##########
'''
input:
input_dict --> dictionary with values that may contain nested dictionaries as strings.

output:
A simplified dictionary with only inner values.

Description:
This function parses values that are lists of dictionaries in string form, extracting only the 'name' fields. 
If parsing fails or the value isn't nested, it remains unchanged.
'''

def clean_dictionary(input_dict):
    output_dict = {}
    for key, value in input_dict.items():
        # Check if the value is a string
        if isinstance(value, str):
            try:
                # Safely evaluate the string to check if it's a list of dictionaries
                parsed_value = ast.literal_eval(value)
                # If it's a list of dictionaries, extract the 'name' values
                if isinstance(parsed_value, list) and all(isinstance(item, dict) for item in parsed_value):
                    output_dict[key] = [item.get('name') for item in parsed_value if 'name' in item]
                else:
                    output_dict[key] = value
            except (ValueError, SyntaxError):
                # If parsing fails, keep the original value
                output_dict[key] = value
        else:
            output_dict[key] = value
    return output_dict


# main program
if __name__ == "__main__":
    # get movie data
    #imdb_id = "tt0113987"
    name="Jarhead"
    df = get_movie_info(name)
    info_dict = df.iloc[0].to_dict()
    cleaned_data = clean_dictionary(info_dict)
    print(cleaned_data)
    