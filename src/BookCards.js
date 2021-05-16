/*
 * Code written following TinderCards documentation (https://www.npmjs.com/package/react-tinder-card)
*/

import React, {useEffect, useRef} from 'react'
import TinderCard from "react-tinder-card";
import './BookCards.css';

// enum for the different swipe directions
const directions = {
	LIKE: "right",
	DISLIKE: "left",
    READ_LIKE: "up",
    READ_DISLIKE: "down"
}

function BookCards({books, setBooks, savedBooks, setSavedBooks}) {

    /* JavaScript states aren't updated live, so we must use local variables, or refContainers, to store values that we will need within the same instance of BookCards */
    // refContainer determines whether or not a book is pending to be saved
    const refContainer = useRef({current: false});
    // currBook contains the book information of the book JUST swiped on. Primarily used to remove the book from the stack
    const currBook = useRef({current: null});
    // checkBook contains the book information of the book being displayed currently. Primarily used to send the correct book to the backend along with a sentiment.
    const checkBook = useRef({current: books[0]});

    useEffect(() => {
        // check to see if we add current book to saved list and that it isn't part of the initial tutorial books, and if so, do it
        if (refContainer.current === true && parseInt(currBook.current.init_flag) !== 1) {
            setSavedBooks((prevSavedBooks) => {
                // since we are updating multiple states, useEffect is called twice.
                // to only add an entry once, we check to see if the book is already in the SavedList
                var found = false;
                for (var i = 0; i < prevSavedBooks.length; i++) {
                    if (prevSavedBooks[i].id === currBook.current.id) {
                        found = true;
                        break;
                    }
                }
                if (!found) {
                    prevSavedBooks.push(currBook.current);
                }
                return prevSavedBooks;
            });
            refContainer.current = false;
        }

        // check to see if card stack is empty
        if (books.length === 0) {
            // call fetch to endpoint to get next 5 BEST recommendations; by default, fetch calls get()
            fetch('book/1').then(res => res.json()).then((value) => {
                // add the returned value of books to the stack of cards after unpacking the different books
                setBooks([value['one'],value['two'],value['three'],value['four'],value['five']]);
                // update the book currently being displayed at the top
                checkBook.current = value['five'];
            });
        }
    });

    /**
     * Performs an action when a BookCard is BEING swiped
     * @param {*} direction: the direction the current card is being swiped in
     */
    const onSwipe = (direction) => {
        // if more implementation is desired, code below here
    }

    /**
     * Performs an action when a BookCard LEAVES the screen completely
     * @param {*} direction: the direction the just-swiped card was swiped to
     */
    const onCardLeftScreen = (direction) => {
        // switch statement determines which direction the user swiped in
        switch (direction) {
            case directions.LIKE:
                /**
                 * json information to be passed to the backend, contains:
                 *  - init_flag: should only be 1 if the current book being swiped is part of the initial hard-coded books
                 *  - book_id: the current book's GoodBooks id
                 *  - sentiment: the user's response to the current book; 1 being positive, 0 being negative
                 */
                const data = { init_flag: (checkBook.current.init_flag == null) ? 0 : 1, book_id: checkBook.current.id, sentiment: 1 };
                // check to see if book id is valid (should only be false for information cards)
                if (checkBook.current.id > 0) {
                    fetch('book/1', {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
                        body: JSON.stringify(data)
                        }).then(res => res.json()).then((value) => {
                            if(value['alert'] === 1) {
                                alert("You have been matched! Swipe away!")
                            }
                        })
                }
                // set flag variable to save the current book to the user's SavedList
                refContainer.current = true;

                console.log("Liked");
                break;
            case directions.DISLIKE:
                const data1 = { init_flag: (checkBook.current.init_flag == null) ? 0 : 1, book_id: checkBook.current.id, sentiment: 0 };
                // send the book id and "0" response to backend
                if (checkBook.current.id > 0) {
                    fetch('book/1', {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
                        body: JSON.stringify(data1)
                        }).then(res => res.json()).then((value) => {
                            if(value['alert'] === 1){
                                alert("You have been matched! Swipe away!")
                            }
                        })
                }

                console.log("Disliked");
                break;
            case directions.READ_LIKE:
                const data2 = { init_flag: (checkBook.current.init_flag == null) ? 0 : 1, book_id: checkBook.current.id, sentiment: 1 };
                // send the book id and "1" response to backend
                if (checkBook.current.id > 0) {
                    fetch('book/1', {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
                        body: JSON.stringify(data2)
                        }).then(res => res.json()).then((value) => {
                            if(value['alert'] === 1){
                                alert("You have been matched! Swipe away!")
                            }
                        })
                }
                    
                console.log("Read and liked");
                break;
            case directions.READ_DISLIKE:
                const data3 = { init_flag: (checkBook.current.init_flag == null) ? 0 : 1, book_id: checkBook.current.id, sentiment: 0 };
                // send the book id and "0" response to backend
                if (checkBook.current.id > 0) {
                    console.log('fetching:', checkBook.current.id);
                    fetch('book/1', {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
                        body: JSON.stringify(data3)
                        }).then(res => res.json()).then((value) => {
                            if(value['alert'] === 1){
                                alert("You have been matched! Swipe away!")
                            }
                        })
                }

                console.log("Read and disliked");
                break;
            default:
                console.log('Something went wrong with swiping');
                break;
        }

        // remove currBook from the card stack and set the book that is just about to be displayed
        setBooks((previousBooks) => {
            currBook.current = previousBooks[previousBooks.length-1];
            if (previousBooks.length > 1) {
                checkBook.current = previousBooks[previousBooks.length-2];
            }
            return previousBooks.slice(0, previousBooks.length-1);
        })
    }

    return (
        <div>
            <h1>BookCards</h1>

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