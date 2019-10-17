import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import useScrollTrigger from '@material-ui/core/useScrollTrigger';
import Fab from '@material-ui/core/Fab';
import KeyboardArrowUpIcon from '@material-ui/icons/KeyboardArrowUp';
import Zoom from '@material-ui/core/Zoom';
import Toolbar from '@material-ui/core/Toolbar';

import NavBar from './NavBar'
import Searcher from './Searcher'


const useStyles = makeStyles(theme => ({
  root: {
    //display: 'inline',
  },
  
  content: {
    //textAlign: 'center',
  },

  buttonScroll: {
    position: 'fixed',
    bottom: theme.spacing(2),
    right: theme.spacing(2),
  },

}));

function ScrollTop(props) {
  const classes = useStyles();
  const trigger = useScrollTrigger();

  const handleClick = event => {
    const anchor = (event.target.ownerDocument || document).querySelector('#back-to-top-anchor');

    if (anchor) {
      anchor.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  };

  return (
    <Zoom in={trigger}>
      <div onClick={handleClick} role="presentation" className={classes.buttonScroll}>
        {props.children}
      </div>
    </Zoom>
  );
}

export default function BaseLayout() {
  const classes = useStyles();
  
  return (
    <div className={classes.root}>
      <NavBar  />
      <main className={classes.content}>
        <Toolbar id="back-to-top-anchor" />
        <Searcher />
        <ScrollTop>
          <Fab color="secondary" size="small" aria-label="scroll back to top">
            <KeyboardArrowUpIcon />
          </Fab>
        </ScrollTop>
      </main>
    </div>
  );
}

