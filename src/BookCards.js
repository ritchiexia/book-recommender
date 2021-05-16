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
    const refContainer = useRef({current: false});
    const currBook = useRef({current: null});
    const checkBook = useRef({current: books[0]});

    useEffect(() => {
        // console.log("Current book stack:", {books});
        // console.log("Top book on stack:", books[books.length-1]);
        console.log("Saved books:", {savedBooks});

        // check to see if we add current book to saved list, and if so, do it
        if (refContainer.current === true && parseInt(currBook.current.init_flag) !== 1) {
            console.log('made it into if statemetn');
            setSavedBooks((prevSavedBooks) => {
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
           // console.log("let's wait to fetch")
            // call fetch to endpoint to get next 5 BEST recommendations
            //while(init_flag.current === 0 && pause.current === 1){
            //   setTimeout(()=>{console.log(pause.current--)}, 20000)
           // }
            //console.log("I'm done waiting")
            fetch('book/1').then(res => res.json()).then((value) => {
                // add the returned value of books to the stack of cards, make sure you CLEAN the data/extract what we need and put it where it needs to be
                setBooks([value['one'],value['two'],value['three'],value['four'],value['five']]);
                checkBook.current = value['five'];
            });
        }
    });

    const onSwipe = (direction) => {
        
    }

    const onCardLeftScreen = (direction) => {
        switch (direction) {
            case directions.LIKE:
                const data = { init_flag: (checkBook.current.init_flag == null) ? 0 : 1, book_id: checkBook.current.id, sentiment: 1 };
                // send the book id and "1" response to backend
                if (checkBook.current.id > 0) {
                    console.log('fetching:', checkBook.current.id);
                    fetch('book/1', {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
                        body: JSON.stringify(data)
                        }).then(res => res.json()).then((value) => {
                            if(value['alert'] === 1){
                                alert("You have been matched! Swipe away!")
                            }
                    })
                }
                refContainer.current = true;

                console.log("Liked");
                break;
            case directions.DISLIKE:
                const data1 = { init_flag: (checkBook.current.init_flag == null) ? 0 : 1, book_id: checkBook.current.id, sentiment: 0 };
                // send the book id and "0" response to backend
                console.log('CheckBook id:', checkBook.current.id);
                if (checkBook.current.id > 0) {
                    console.log('fetching:', checkBook.current.id);
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
                    console.log('fetching:', checkBook.current.id);
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

        // remove currBook from the card stack
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