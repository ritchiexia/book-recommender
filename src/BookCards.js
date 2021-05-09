import React, {useState, useEffect} from 'react'
import TinderCard from "react-tinder-card";
import './BookCards.css';

const directions = {
	LIKE: "right",
	DISLIKE: "left",
    SAVE: "up"
}

function BookCards() {
    const [currBook, setCurrBook] = useState(null);

    const [books, setBooks] = useState([
        {
            id: '1',
            name: 'Test Book Title',
            url: 'https://thewritelife.com/wp-content/uploads/2019/08/How-to-format-a-book.jpg',
            author: 'Test'
        },
        {
            id: '2',
            name: 'Other Test',
            url: 'https://media.wired.com/photos/5be4cd03db23f3775e466767/125:94/w_2375,h_1786,c_limit/books-521812297.jpg',
            author: 'Test2'
        }
    ]);

    useEffect(() => {
        console.log("test", {books});
        // **** FETCH THE FIRST 5 CARDS FROM THE BACKEND ****, make sure to check how fetch is going to work from backend
        // also make sure we fetch from the correct endpoint in the back (the initial 5 random books)
        // fetch('localhost.3001/init_books').then((value) => {
        //     // add the returned value of books to the stack of cards, make sure you CLEAN the data/extract what we need and put it where it needs to be
        //     setBooks(value);
        //     // for following line, set the curr book as the book on top of the card stack
        //     setCurrBook();
        // });
        
        // check to see if card stack is empty
        if (books.length === 0) {
            // call fetch to endpoint to get next 5 BEST recommendations
            // fetch({insert endpoint here});
            console.log("empty!");
        }
    });

    // setBooks([])

    const onSwipe = (direction) => {
        switch (direction) {
            case directions.LIKE:
                // send the currBook and "like" response to backend
                // 
                console.log("Liked");
                break;
            case directions.DISLIKE:
                console.log("Disliked");
                break;
            case directions.SAVE:
                console.log("saved");
                break;
            default:
                console.log('Something went wrong with swiping');
                break;
        }
    }

    const onCardLeftScreen = () => {
        // remove currBook from the card stack
        setBooks((previousBooks) => {
            return previousBooks.slice(0, previousBooks.length-1);
        })
    }

    return (
        <div>
            <h1>Book Cards</h1>

            <div className="bookCards__cardContainer">
                {books.map(book => (
                    <TinderCard className="swipe" key={book.id} onSwipe={onSwipe} onCardLeftScreen={onCardLeftScreen} preventSwipe={['down']}>
                        <div style={{backgroundImage: `url(${book.url})`}} className="card">
                            <h3>{book.name}</h3>
                        </div>
                    </TinderCard>
                ))}
            </div>
        </div>
    )
}

export default BookCards