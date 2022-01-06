# BOOKCARDS 📘🃏

## Table Of Contents

* [Project Description](#project-description)
* [Setup](#setup)
* [Web App Walkthrough/How to Use BookCards](#walkthrough)
* [Technologies](#technologies)
* [Video Link](#video-link)

## Project Description
Our project makes book recommendations powered by machine learning. Our web app uses a user's reactions towards 18 representative books to match them with a reader in our existing dataset. The user is then presented with books that the machine learning model recommends, using data from the paired user, then prompting the user as to whether they like this book or not. This is done through an interface evocative of modern dating apps like Tinder or Bumble. As the user swipes, they begin to cultivate a list of books they’ve liked, and the underlying machine learning model adapts based on their swipe activity. Thus, as the app is used, the model learns more about the user’s book tastes, improving its future recommendations.

## Setup



## Web App Walkthrough/How to Use BookCards
When you open the BookCards app you are greeted by a tutorial card explaining the function of each swipe direction. 

<br />
Photo here
<br />

Swiping past this, you are then presented with 18 books, chosen to represent a range of genres, which are used to determine which user from the dataset you most resemble. As you swipe your responses are communicated to the backend, which interprets a positive swipe as 5 stars and negative swipe as 0 stars. The set of 18 book-rating pairs are then used to find the user with whom you are most similar to. 

<br />
Photo here
<br />

This process takes time, so when you swipe on the last book in the representative set, you are presented with a waiting message. The message informs you to wait until the app alerts you that it has completed the pairing process. When the backend has selected a similar user, your browser will alert you. You can now swipe through the highest ranked books for this user.

<br />
Photo here
<br />

As you swipe, the reinforcement learning model trains itself to improve the books that it will recommend to you. The books you swipe right on get added to a saved books list available through a button at the top right corner. By clicking the check box on the top right of each card and switching back to the home page, by clicking the centrosaurus icon on the top left, the user is able to delete that book from the saved list.

<br />
Photo here
<br />

That’s it! Using BookCards is a simple and easy way to get personalized book recommendations, where your next read may only be a swipe away!

## Technologies

## Video Link
https://youtu.be/B6URcxePV0s