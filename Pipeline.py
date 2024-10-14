from header import *
from MovieData import call_database,get_movie_info
from Review_Summary import generate_movie_summary
from Content_req_test import recommend_movies as content_req
from User_req import recommend_movies as user_req 

'''
Author: Tina Nosrati
Last Update: 10/14/2024

Description: 
This script will perform as the main pipline of the project
'''



# main program
if __name__ == "__main__":

    #getting movie info
    name="Jarhead"
    df = get_movie_info(name)

    #create dictionary of movie informations
    info_dict = df.iloc[0].to_dict()

    #generate review summary
    summary=generate_movie_summary(name)

    #content based recommendation
    content_model_path = os.path.expanduser('~/content_req_model.pkl')
    with open(content_model_path, 'rb') as f:
        df, cosine_sim, tfidf = pickle.load(f) 
    
    content_req_list = content_req(name, df, cosine_sim)
    
    #user based recommendation system
    user_req_list=user_req(name)

    print("Movie Data:")
    print(info_dict)
    print("Summary of reviews:")
    print(summary)
    print("Content based recommendation:")
    print(content_req_list)
    print("User based recommendation:")
    print(user_req_list)
     

