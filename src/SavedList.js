import React, {useState, useEffect, useRef, Component} from 'react'
import './SavedList.css';

function SavedList({savedBooks, setSavedBooks}) {

    return (
        <div>
            <h1>Saved List</h1>

            <div className="SavedList___container">
                {
                    savedBooks.map(book => (
                        <div className="box" key={book.id}>
                            <div className="entry">
                                <h3>{book.name}</h3>
                                <h4>{book.author}</h4>
                            </div>
                        </div>
                    ))
                }
                
            </div>
        </div>
    )
}

export default SavedList