/*
 * General format of header and styling follows this tutorial: https://www.youtube.com/watch?v=DQfeB_FKKkc&t=5317s, but slightly adjusted.
 * In general we are just emulating Tinder's layout
*/

import React from 'react'
import './Header.css';
import BookIcon from '@material-ui/icons/Book';
import IconButton from "@material-ui/core/IconButton";

function Header({onViewingSaved}) {
    return (
        <div className="header">
            <IconButton onClick={() => onViewingSaved(false)}>
            <img className="header__logo"
                alt="/centrosaurus.png"
                src="https://image.flaticon.com/icons/png/512/47/47251.png"
            />
            </IconButton>

            <IconButton onClick={() => onViewingSaved(true)}>
            <BookIcon className="header__icon" fontSize="large"/>
            </IconButton>
        </div>
    )
}

export default Header