import {React, useState} from 'react'
import './App.css';
import Header from './Header';
import BookCards from './BookCards';
import SavedList from './SavedList';

function App() {

  const [viewingSaved, setViewingSaved] = useState(false);

  const onViewingSaved = (isViewing) => {
    setViewingSaved(isViewing);
  }
  
  const [savedBooks, setSavedBooks] = useState([]);

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
    },
    {
        id: '3',
        name: 'Test 3',
        url: 'https://thewritelife.com/wp-content/uploads/2019/08/How-to-format-a-book.jpg',
        author: 'Test 3 Author'
    },
    {
        id: '4',
        name: 'Test 4',
        url: 'https://thewritelife.com/wp-content/uploads/2019/08/How-to-format-a-book.jpg',
        author: 'Test 4 Author'
    },
    {
        id: '5',
        name: 'Test 5',
        url: 'https://thewritelife.com/wp-content/uploads/2019/08/How-to-format-a-book.jpg',
        author: 'Test 5 Author'
    },
  ]);

  return (
    <div className="App">
      {/* {HEADER} */}
      <Header onViewingSaved={onViewingSaved}/>
      {
        viewingSaved ? <SavedList savedBooks={savedBooks} setSavedBooks={setSavedBooks}/> : <BookCards books={books} setBooks={setBooks} savedBooks={savedBooks} setSavedBooks={setSavedBooks}/>
      }
    </div>
  );
}

export default App;
