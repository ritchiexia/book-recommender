import React, {useState} from 'react'
import TinderCard from "react-tinder-card";
import './BookCards.css';

function BookCards() {
    const [books, setBooks] = useState([
        {
            name: 'Test Book Title',
            url: 'https://thewritelife.com/wp-content/uploads/2019/08/How-to-format-a-book.jpg'
        },
        {
            name: 'Other Test',
            url: 'https://media.wired.com/photos/5be4cd03db23f3775e466767/125:94/w_2375,h_1786,c_limit/books-521812297.jpg'
        }
    ]);

    // setBooks([])

    return (
        <div>
            <h1>Book Cards</h1>

            <div className="bookCards__cardContainer">
                {books.map(book => (
                    <TinderCard className="swipe" key={book.id} preventSwipe={['down']}>
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