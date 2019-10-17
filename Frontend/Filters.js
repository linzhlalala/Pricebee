import React ,{useEffect}from 'react';
import { makeStyles } from '@material-ui/core/styles';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import Checkbox from '@material-ui/core/Checkbox';
import Paper from '@material-ui/core/Paper';
import Divider from '@material-ui/core/Divider';
import Typography from '@material-ui/core/Typography';
import Slider from '@material-ui/core/Slider';

/*
function createData( brand, nums, selected) {
    return { brand, nums, selected};
  }
  
const filters = [
    createData('Nestle', 4),
    createData('Babylove', 7),
    createData('Huggies', 3),
    createData('Cadbury', 23),
    createData('Pauls', 2),
];
const pricemin = 0;
const pricemax = 200;
*/

const useStyles = makeStyles(theme => ({
  root: {
    padding: theme.spacing(1,0),
    //width: '99%',
    //backgroundColor: theme.palette.background.paper
  },
  checkicon:{
    width: 20,
    height: 20,
    marginRight: theme.spacing(1),
  },
  description:{
    marginLeft: theme.spacing(1),
  },
  slider:{
    width: '80%',
    marginLeft: '10%',
  }
}));


function valuetext(value) {
    return `$ ${value}`;
  }

function RangeSlider(props) {
    const classes = useStyles();
    const [value,setValue] = React.useState([]);
    const handleChange = (event, newValue) => {
        setValue(newValue);
    };

    useEffect(()=>{
      setValue(props.ranges);
    },[props.ranges]);

    return (
        <Slider className={classes.slider}
            min={props.ranges[0]}
            max={props.ranges[1]}
            value={value}
            onChange={handleChange}
            onChangeCommitted={props.valuehandler}
            step = {0.1}
            valueLabelDisplay="auto"
            aria-labelledby="range-slider"
            getAriaValueText={valuetext}
        />
    )
}


export default function Filters(props) {
  const classes = useStyles();

//  const [checked, setChecked] = React.useState([]);
/*
  const handleToggle = value => () => {
    const currentIndex = checked.indexOf(value);
    const newChecked = [...checked];

    if (currentIndex === -1) {
      newChecked.push(value);
    } else {
      newChecked.splice(currentIndex, 1);
    }

    setChecked(newChecked);
  };
*/
  return (
    <Paper className={classes.root} >
        <Typography variant="h6" className={classes.description}>
            Brand:
        </Typography>
        <List dense disablePadding >
        {props.brands.map(el=> {
            const labelId = `checkbox-list-secondary-label-${el.brand}`;
            return (
            <ListItem key={el.brand}>
                <Checkbox className={classes.checkicon} 
                    onChange={props.brandhandler(el.brand)}
                    checked={el.selected}
                    inputProps={{ 'aria-labelledby': labelId }}
                    color='primary'
                />
                <ListItemText id={labelId} primary={el.brand} />
                <ListItemText align='right' id={labelId} primary= {el.nums} />
            </ListItem>
            );
        })}
        </List>
        <Divider/>
        <Typography variant="h6" className={classes.description}>
            Price:
        </Typography>
        <RangeSlider ranges={props.ranges} valuehandler={props.valuehandler}/>
    </Paper>
  );
}
