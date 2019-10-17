import React from 'react';
import {  makeStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import InputBase from '@material-ui/core/InputBase';
import Divider from '@material-ui/core/Divider';
import IconButton from '@material-ui/core/IconButton';

import Chip from '@material-ui/core/Chip';
import SearchIcon from '@material-ui/icons/Search';
import LocalFloristIcon from '@material-ui/icons/LocalFlorist';
import ResultsLayout from './ResultsLayout'
import axios from "axios";

const useStyles = makeStyles(theme => ({
    
    root: {
        position: "absolute",
        marginLeft: '2%',
        width: '96%',
        minHeight: '100vh',
        backgroundColor: '#ffecb3',
    },
    
    inputatCenter: {
        position: 'relative',
        top: '30%',
        left: '5%',
        width: '90%',
        [theme.breakpoints.up('md')]: {
            left: '25%',
            width: '50%',
        }
    },
    
    inputatTop: {
        position: 'relative',
        display: 'inline',
        
        [theme.breakpoints.up('md')]: {
            display: 'flex',
        }
    },

    inputbar:{
        display: 'flex',
        flexWrap: 'wrap',
        padding: theme.spacing(1),
        margin: theme.spacing(1,1,0,1),
        alignItems: 'center',
        flex:1,
    },
    input: {
        marginLeft: theme.spacing(1),
        flex: 1,
    },
    iconButton: {

    },
    divider: {
        height: 28,
        margin: theme.spacing(0.5),
    },

    chipboard: {
        display: 'flex',
        justifyContent: 'center',
        flexWrap: 'wrap',
        padding: theme.spacing(1),
        margin: theme.spacing(1,1,0,0),
    },
    chip: {
        margin: theme.spacing(0.5),
    },
}));

function ChipsArray() {
    const classes = useStyles();
    const [chipData, setChipData] = React.useState([
      { key: 0, label: 'this' },
      { key: 1, label: 'for' },
      { key: 2, label: 'display' },
      { key: 3, label: 'only' },
    ]);
  
    const handleDelete = chipToDelete => () => {
        alert('Why would you want to delete me?! :)');
        setChipData(chips => chips.filter(chip => chip.key !== chipToDelete.key));
    };
  
    return (
      <Paper className={classes.chipboard}>
        {
            chipData.map(data => {
            return (
                <Chip
                key={data.key}
                label={data.label}
                onDelete={handleDelete(data)}
                className={classes.chip}
                color= 'primary'
                />
          );
        })}
      </Paper>
    );
  }

function SearchInput(props) {
  const classes = useStyles();

  return (
    <Paper className={classes.inputbar}>
        <IconButton className={classes.iconButton} aria-label="menu" 
               color= 'primary'>
            <LocalFloristIcon />
        </IconButton>
        <InputBase
            className={classes.input}
            placeholder="Search WWS&Coles"
            inputProps={{'aria-label': 'Search WWS&Coles'}}
            onChange={props.inputChange}
        >
            {props.showword}
        </InputBase>
        <IconButton className={classes.iconButton} aria-label="search"
                color= 'primary'
                onClick={props.buttonClick}>
            
            <SearchIcon />
        </IconButton>
        <Divider className={classes.divider} orientation="vertical" />
        <IconButton className={classes.iconButton} aria-label="directions"
                color= 'primary'>
            <LocalFloristIcon />
        </IconButton>
    </Paper >
  );
}
/*
function BeforeSearcher() {
    const classes = useStyles();
    return (
    <Paper className={classes.root}>
        <div className={classes.inputatCenter}>
            <Typography variant="h3"  align="center">
                Search
            </Typography>

            <SearchInput/>
            <ChipsArray/>

            <Typography variant="h7"  align="center">
                (By the way, I'm looking for Job)
            </Typography>
        </div>
    </Paper>
    );
}
*/
export default function Searcher() {
    const classes = useStyles();
    const [keyword,setkeyword] = React.useState('');
    const [Resultlist,setResultlist] = React.useState([]);

    const handleSearchClick = ()=>{
        //alert(keyword);
        //http://127.0.0.1:8000/api/pbsearch/?name=nappies //CLOSE (FILTER TYPE)
        //http://127.0.0.1:8000/api/pbsearch/?search= (SEARCH TYPE)
        if (keyword.length <= 1) {
            alert("Try again with longer keyword!")
            return;
        }
        axios.get("https://pricebeetest-250705.appspot.com/api/pbsearch/?search="+keyword)
            .then(res => setResultlist(res.data))
            .catch(err => console.log(err));
    }

    const handleSearchChange= (event)=>{
        setkeyword(event.target.value);
    }

    return (
    <Paper className={classes.root}>

        <div className={classes.inputatTop}>
            
            <SearchInput showword={keyword} inputChange = {handleSearchChange} buttonClick = {handleSearchClick}/>
            <ChipsArray/>

        </div>
        
        <ResultsLayout fullList = {Resultlist} />
    </Paper>
    );
}