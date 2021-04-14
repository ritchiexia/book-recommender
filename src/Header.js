import React from 'react'
import './Header.css';
import PersonIcon from '@material-ui/icons/Person';
import BookIcon from '@material-ui/icons/Book';
import IconButton from "@material-ui/core/IconButton";

function Header() {
    return (
        <div className="header">
            <IconButton>
            <PersonIcon className="header__icon" fontSize="large"/>
            </IconButton>

            <IconButton>
            <img className="header__logo"
                src="https://e7.pngegg.com/pngimages/932/58/png-clipart-centrosaurus-tyrannosaurus-lambeosaurus-pterodactyls-spinosaurus-dinosaur-carnivoran-dog-like-mammal-thumbnail.png"
                alt="Centrosaurus logo"/>
            </IconButton>

            <IconButton>
            <BookIcon className="header__icon" fontSize="large"/>
            </IconButton>
        </div>
    )
}

export default Header