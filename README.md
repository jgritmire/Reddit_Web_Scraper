# Project 3: Reddit and Webscraping

## Contents
##### - Problem Statement
##### - Data Description
##### - Data Cleaning/Feature Engineering
##### - Modeling
##### - Final Model/Conclusion

## Problem Statement

You're fresh out of your Data Science bootcamp and looking to break through in the world of freelance data journalism. Nate Silver and co. at FiveThirtyEight have agreed to hear your pitch for a story in two weeks!

Your piece is going to be on how to create a Reddit post that will get the most engagement from Reddit users. Because this is FiveThirtyEight, you're going to have to get data and analyze it in order to make a compelling narrative.

You have been tasked with determining how we can optimize our chances at having a successful reddit post. A successful post is defined as having more than the median number of comments. In the case of our dataset, the median number of comments is 185. 

## Data Description

The cleaned dataset contains 14,226 observations and 17 variables (post title, number of comments, the subreddit, how long ago it was posted, the number of upvotes, when the data was scraped, whether the post contains text, image, or video, the length of the title, whether the title contains an emoji, and the unique ID for the post. 

## Cleaning and Feature Engineering

The part of this dataset that required the most cleaning was unsurprisingly the title. I first transformed the titles to lowercase and removed the emojis. I next stemmed the words in the titles and performed TFIDF analysis to identify important words that helped differentiate between successful and unsuccessful posts. 

I engineered a variety of terms that related to when a post was posted, noting the hour in which it was posted, and the day of the week that it was posted. I reverse engineered the time that each post was posted by taking the difference from "scraped_time" and "hours_ago".

## Modeling

I created two distinct groups of models: Random Forest models and Logistic Regression models. For these models I dummified the pertinent categorical variables, and initially modeled on all variables. After these models initially output relatively high scores (0.75+) I realized that including the number of upvotes that a post received did not make sense as that is not a factor that you can control while creating your post. Removing this variable decreased the performance of my models significantly, as they were now returning scores slightly under 0.6 with larger confidence intervals. 

I wanted to analyze the titles and see if there were any buzz words that helped posts succeed, but ultimately when I included the variables generated from my TFIDF analysis, they did not improve the performance of the model and so I elected to exclude them. I believe that these terms would have more impact if we either expanded the scope of the data set to include posts from a larger time span, because around the winter holidays there are a lot of posts about christmas, new years, etc that wouldn't exist around, for example, halloween. I also believe that if we narrowed the scope of our analysis to individual subreddits, the TFIDF analysis might become more relevant.

## Final Model and Conclusions

My final model is a logistic regression model that does not include the TFIDF terms that I created. This model has a score of 0.59 with a 95% confidence interval of between 0.56 and 0.63. This model predicts on post content, title length, and when the post was posted. I standard scaled the data so that I would be able to look at the relative contributions of the variables to a post's chances of succes. 

The model indicates that in order to give your post the highest chance of success, you should post a text only post on thursday between 10 and 11 am. Given the number of successful posts and the rate of post success in the various subreddits that I collected data from, I would recommend posting in either r/teenagers, or r/antiwork. A post with the worst chance at succeeding would be an image posted on a friday between 11:00pm and midnight, to a subreddit that does not generally reward images such as r/askreddit. 

It should be noted that our final model does not have a lot of predictive power, but ultimately what we are trying to predict is human behaviour. We are trying to predict what people like, and how they will interact with a post. When the scope of our analysis is the front page, it is very difficult to determine what will succeed. This project would likely be much more successful if we took a deep dive into a single subreddit, and tried to determine what attributes helped a post become successful within the boundaries of that subreddit. In that situation, we would likely be able to include more TFIDF analysis because each subreddit is dedicated to a specific topic, which would likely have more recurring/distinguishing words. For example, in the anti-work subreddit, I would imagine that posts with much more negative titles would tend to do better, as the people that are members of that subreddit love to see people talking trash about their bosses and explaining their unpleasant working conditions.

