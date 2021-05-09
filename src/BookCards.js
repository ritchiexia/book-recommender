/*
 * Code written following TinderCards documentation (https://www.npmjs.com/package/react-tinder-card)
*/

import React, {useEffect, useRef} from 'react'
import TinderCard from "react-tinder-card";
import './BookCards.css';

const directions = {
	LIKE: "right",
	DISLIKE: "left",
    READ_LIKE: "up",
    READ_DISLIKE: "down"
}

function BookCards({books, setBooks, savedBooks, setSavedBooks}) {
    const refContainer= useRef({current: false});
    const currBook = useRef({current: null});
    const init_flag = useRef({current: 20});

    useEffect(() => {
        console.log("Current book stack:", {books});
        console.log("Top book on stack:", books[books.length-1]);

        // check to see if we add current book to saved list, and if so, do it
        if (refContainer.current) {
            setSavedBooks((prevSavedBooks) => {
                var found = false;
                for (var i = 0; i < prevSavedBooks.length; i++) {
                    if (prevSavedBooks[i].id === currBook.current.id) {
                        found = true;
                        break;
                    }
                }
                if (!found) {
                    prevSavedBooks.push(currBook.current)
                }
                return prevSavedBooks;
            });
            refContainer.current = false;
        }

        // check to see if card stack is empty
        if (books.length === 0) {
            console.log("Book stack is empty! Fetching more books...");

            // call fetch to endpoint to get next 5 BEST recommendations
            fetch('localhost:5000/books/1').then(res => res.json()).then((value) => {
                // add the returned value of books to the stack of cards, make sure you CLEAN the data/extract what we need and put it where it needs to be
                setBooks(value);
            });

        }
        // FOR TESTING *** REMOVE AFTER DONE
        console.log("Currently saved books:", {savedBooks});
    });

    const onSwipe = (direction) => {
        
    }

    const onCardLeftScreen = (direction) => {
        const requestOptions = {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title: 'Sending positive sentiment...' })
        };
        switch (direction) {
            case directions.LIKE:
                // send the book id and "1" response to backend
                fetch('localhost:5000/books/1', requestOptions)
                    .then(response => response.json())
                    .then(data => this.setState({ init_flag: (init_flag.current > 0) ? 1 : 0, book_id: books[books.length-1].id, sentiment: 1 }));
                init_flag.current--;
                refContainer.current = true;

                console.log("Liked");
                break;
            case directions.DISLIKE:
                // send the book id and "0" response to backend
                fetch('localhost:5000/books/1', requestOptions)
                    .then(response => response.json())
                    .then(data => this.setState({ init_flag: (init_flag.current > 0) ? 1 : 0, book_id: books[books.length-1].id, sentiment: 0 }));
                init_flag.current--;

                console.log("Disliked");
                break;
            case directions.READ_LIKE:
                // send the book id and "1" response to backend
                fetch('localhost:5000/books/1', requestOptions)
                    .then(response => response.json())
                    .then(data => this.setState({ init_flag: (init_flag.current > 0) ? 1 : 0, bookid: books[books.length-1].id, sentiment: 1 }));
                init_flag.current--;
                    
                console.log("Read and liked");
                break;
            case directions.READ_DISLIKE:
                // send the book id and "0" response to backend
                fetch('localhost:5000/books/1', requestOptions)
                    .then(response => response.json())
                    .then(data => this.setState({ init_flag: (init_flag.current > 0) ? 1 : 0, book_id: books[books.length-1].id, sentiment: 0 }));
                init_flag.current--;

                console.log("Read and disliked");
                break;
            default:
                console.log('Something went wrong with swiping');
                break;
        }

        // remove currBook from the card stack
        setBooks((previousBooks) => {
            currBook.current = previousBooks[previousBooks.length-1];
            return previousBooks.slice(0, previousBooks.length-1);
        })
    }

    return (
        <div>
            <h1>Book Cards</h1>

            <div className="bookCards__cardContainer">
                {books.map(book => (
                    <TinderCard className="swipe" key={book.id} onSwipe={onSwipe} onCardLeftScreen={onCardLeftScreen}>
                        <div style={{backgroundImage: `url(${book.url})`}} className="card">
                            <h3>{book.name}</h3>
                            <h4>{book.author}</h4>
                        </div>
                    </TinderCard>
                ))}
            </div>
        </div>
    )
}

export default BookCards