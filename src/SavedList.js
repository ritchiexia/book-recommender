import React from 'react'
import './SavedList.css';

function SavedList({savedBooks, setSavedBooks}) {

    const removeBook = (book) => {
        var array = savedBooks;
        var idx = array.findIndex((element) => element.id === book.id);
        if (idx !== -1) {
            array.splice(idx, 1);
            setSavedBooks(array);
        }
    }

    return (
        <div>
            <h1>Saved Books</h1>

            <div className="SavedList___container">
                {
                    savedBooks.map(book => (
                        <div className="box" key={book.id}>
                            <div className="entry">
                                <div className="info">
                                    <h3>{book.name}</h3>
                                    <h4>{book.author}</h4>
                                </div>
                                <input type="checkbox" onClick={() => removeBook(book)} className="x"/>
                                <img className="cover" src={book.url} alt=""/>
                            </div>
                        </div>
                    ))
                }
                
            </div>
        </div>
    )
}

export default SavedList