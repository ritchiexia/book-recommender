import {React, useState} from 'react'
import './App.css';
import Header from './Header';
import BookCards from './BookCards';
import SavedList from './SavedList';

function App() {
  
  // boolean to determine which page to display
  const [viewingSaved, setViewingSaved] = useState(false);

  // function to toggle the above boolean and switch between BookCards and SavedList
  /**
   * Sets the boolean state that controls what to display on the web page
   * @param {*} isViewing: true -> view SavedList, false -> view BookCards
   */
  const onViewingSaved = (isViewing) => {
    setViewingSaved(isViewing);
  }
  
  // initialize empty list for user's saved books
  const [savedBooks, setSavedBooks] = useState([]);

  // initialize the BookCards stack with the 18 set starter books
  const [books, setBooks] = useState([ 
    {
      id: -2,
      name: 'Please wait...',
      url: 'https://cdn.discordapp.com/attachments/824063621864095744/843353932356648970/unknown.png',
      author: 'Team Centrosaurus',
      init_flag: '1'
    },
    {
      id : 3,
      name : 'To Kill a Mocking Bird',
      url : 'https://images.gr-assets.com/books/1361975680m/2657.jpg',
      author : 'Harper Lee',
      init_flag: '1'
    },
    {
      id: 15,
      name: "The Girl with the Dragon Tattoo (Millennium, #1)",
      url: "https://images.gr-assets.com/books/1327868566m/2429135.jpg",
      author: "Stieg Larsson, Reg Keeland",
      init_flag: '1'
    },
    {
      id: 18,
      name: "The Fellowship of the Ring (The Lord of the Rings, #1)",
      url: "https://images.gr-assets.com/books/1298411339m/34.jpg",
      author: "J.R.R. Tolkien",
      init_flag: '1'
    },
    {
      id: 815,
      name: "Wolf Hall (Thomas Cromwell, #1)",
      url: "https://images.gr-assets.com/books/1336576165m/6101138.jpg",
      author: "Hilary Mantel",
      init_flag: '1'
    },
    {
      id: 96,
      name: "Dracula",
      url: "https://images.gr-assets.com/books/1387151694m/17245.jpg",
      author: "Bram Stoker, Nina Auerbach, David J. Skal",
      init_flag: '1'
    },
    {
      id: 4,
      name: "The Great Gatsby",
      url: "https://images.gr-assets.com/books/1490528560m/4671.jpg",
      author: "F. Scott Fitzgerald",
      init_flag: '1'
    },
    {
      id: 9,
      name: "Pride and Prejudice",
      url: "https://images.gr-assets.com/books/1320399351m/1885.jpg",
      author: "Jane Austen",
      init_flag: '1'
    },
    {
      id: 127,
      name: "Steve Jobs",
      url: "https://images.gr-assets.com/books/1327861368m/11084145.jpg",
      author: "Walter Isaacson",
      init_flag: '1'
    },
    {
      id: 14,
      name: "The Diary of a Young Girl",
      url: "https://images.gr-assets.com/books/1358276407m/48855.jpg",
      author: "Anne Frank, Eleanor Roosevelt, B.M. Mooyaart-Doubleday",
      init_flag: '1'
    },
    {
      id: 2458,
      name: "Mastering the Art of French Cooking",
      url: "https://images.gr-assets.com/books/1333577773m/129650.jpg",
      author: "Julia Child, Simone Beck, Louisette Bertholle",
      init_flag: '1'
    },
    {
      id: 2738,
      name: "Bad Feminist",
      url: "https://images.gr-assets.com/books/1421292744m/18813642.jpg",
      author: "Roxane Gay",
      init_flag: '1'
    },
    {
      id: 316,
      name: "I Know Why the Caged Bird Sings",
      url: "https://images.gr-assets.com/books/1327957927m/13214.jpg",
      author: "Maya Angelou",
      init_flag: '1'
    },
    {
      id: 60,
      name: "The Girl on the Train",
      url: "https://images.gr-assets.com/books/1490903702m/22557272.jpg",
      author: "Paula Hawkins",
      init_flag: '1'
    },
    {
      id: 5,
      name: "The Fault in Our Stars",
      url: "https://images.gr-assets.com/books/1360206420m/11870085.jpg",
      author: "John Green",
      init_flag: '1'
    },
    {
      id: 2992,
      name: "The Lottery",
      url: "http://2.bp.blogspot.com/_sJq42pXCZlI/TPk56SM9t3I/AAAAAAAAC2U/YDk7007wQrA/s1600/shirley%2Bjackson.JPG",
      author: "Shirley Jackson",
      init_flag: '1'
    },
    {
      id: 259,
      name: "How to Win Friends and Influence People",
      url: "https://images.gr-assets.com/books/1442726934m/4865.jpg",
      author: "Dale Carnegie",
      init_flag: '1'
    },
    {
      id: 617,
      name: "The Hound of the Baskervilles",
      url: "https://images.gr-assets.com/books/1355929358m/8921.jpg",
      author: "Arthur Conan Doyle, Anne Perry",
      init_flag: '1'
    },
    {
      id: 237,
      name: "Augusten Burroughs",
      url: "https://images-na.ssl-images-amazon.com/images/I/51mzqTVGgfL._SX331_BO1,204,203,200_.jpg",
      author: "Running with Scissors",
      init_flag: '1'
    },
    {
      id: -1,
      name: "Introduction to BookCards!",
      url: "https://media.discordapp.net/attachments/707031501392314369/843314088347697152/unknown.png",
      author: "Team Centrosaurus",
      init_flag: '1'
    }
    ]);

  return (
    <div className="App">
      <Header onViewingSaved={onViewingSaved}/>
      {/* Ternary statement to determine which page to render. Designed so that upon clicking on their respective icons, the page switches between BookCards and SavedList */}
      {
        viewingSaved ? <SavedList savedBooks={savedBooks} setSavedBooks={setSavedBooks}/> : <BookCards books={books} setBooks={setBooks} savedBooks={savedBooks} setSavedBooks={setSavedBooks}/>
      }
    </div>
  );
}

export default App;
