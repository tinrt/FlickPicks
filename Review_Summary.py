from header import *

'''
Author: Tina Nosrati
Last Update: 10/14/2024

Description: 
This script will summarize movie reviews for a selected movie.
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


##########summarize_review##########
'''
Arguments:
input:
text --> string input to be summarized

Output: A summary of the input text limited to 200 tokens

Description: 
This function uses a lightweight LLM to summarize a given string input. This will be
used for the summary of all reviews because it is capable of generating more tokens.
'''

def summarize_review(text):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model_name = "google/flan-t5-small" 
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)
    tokenized_text = tokenizer.encode(text, return_tensors="pt").to(device)
    summary_ids = model.generate(tokenized_text,
                                    num_beams=4,
                                    no_repeat_ngram_size=3,
                                    min_length=100,
                                    max_length=200,
                                    length_penalty=2.0,
                                    #emperature=0.8
                                    )
    output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return output


##########summarize_text##########
'''
Arguments:
input:
text --> string input to be summarized

Output: A summary of the input text limited to 50 tokens

Description: 
This function uses a lightweight LLM to summarize a given string input.
'''

def summarize_text(text):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model_name = "google/flan-t5-small" 
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)
    tokenized_text = tokenizer.encode(text, return_tensors="pt").to(device)
    summary_ids = model.generate(tokenized_text,
                                    do_sample=True,
                                    num_beams=4,
                                    no_repeat_ngram_size=3,
                                    min_length=30,
                                    max_length=50,
                                    length_penalty=2.0,
                                    temperature=0.8
                                    )
    output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return output

##########get_reviews_for_imdb_id##########
'''
Arguments:
input:
imdb_id --> id of the selected movie

Output: A dataframe containing reviews for the selected movie

Description: 
This function will return a dataframe of reviews for a selected
movie from the database. It will Keep reviews with length less 
than 1000 characters and if filtering results in an empty 
dataset, truncate reviews to 1000 characters.
'''

def get_reviews_for_imdb_id(imdb_id):
    try:
        conn, cur = call_database()
        query = "SELECT * FROM reviews WHERE imdb_id = %s"        
        cur.execute(query, (imdb_id,))       
        rows = cur.fetchall()     
        column_names = [desc[0] for desc in cur.description]     
        df = pd.DataFrame(rows, columns=column_names) 
        df = df.sample(frac=1).reset_index(drop=True) 
        filtered_df = df[df['review'].str.len() < 1000]
        if filtered_df.empty:
            df['review'] = df['review'].str[:1000]
        else:
            df = filtered_df
        
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

##########clean_fullstop##########
'''
Arguments:
input:
text --> string input to cleaned

Output: A cleaned version od the text

Description: 
This function will make sure that the summary is a complete sentence and
will end in '.'
'''

def clean_fullstop(text):
    last_full_stop_index = text.rfind('.')
    if last_full_stop_index != -1:
        cleaned_text = text[:last_full_stop_index + 1]
    else:
        cleaned_text = text
    return cleaned_text

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
    
##########generate_movie_summary##########
'''
input: 
name --> the name of the movie that we are processing

output: summary of user reviews for this movie

Description:
This function will recive a movie name and generate summary
of user review for that movie.
'''
def generate_movie_summary(name):
    imdb_id=find_movie_id(name)
    reviews_df = get_reviews_for_imdb_id(imdb_id)
    reviews_df['review'] = reviews_df['review'].apply(summarize_text)
    full_text=""
    for rev in reviews_df['review'].tolist():
        full_text=full_text + ' '+ rev
    summary = summarize_review(full_text)
    summary=clean_fullstop(summary)
    return summary


# main program
if __name__ == "__main__":
    # get reviews data
    #imdb_id = "tt0113987"
    name="Jarhead"
    summary=generate_movie_summary(name)

    print("Summary:", summary)