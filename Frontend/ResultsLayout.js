import React,{useEffect} from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Filters from './Filters';
import EnhancedTable from './Table';


const useStyles = makeStyles(theme => ({
  
  mainGrid: {
    padding: theme.spacing(1),
    // paddingRight: theme.spacing(1),
    // paddingLeft: theme.spacing(1),
  },
  sideGrid: {
    padding: theme.spacing(1,1,1,0),
    [theme.breakpoints.down('sm')]: {
      paddingLeft: theme.spacing(1),
    },
    // paddingRight: theme.spacing(1),
    // paddingLeft: theme.spacing(1),
  },
}));

function countBrands(itemlist)
{
  var brandlist = [];
  for(var i=0;i<itemlist.length;i++){
    //is it in
    var thisbrand = itemlist[i].item_brand;
    var found = false;
    for(var j=0;j<brandlist.length;j++){
      if (brandlist[j].brand === thisbrand){
        brandlist[j].nums += 1;
        found = true;
        break;
      }
    }
    if (found === false){
      brandlist.push({
        'brand': thisbrand,
        'nums': 1,
        'selected': true,
      });
    }
  }
  //sort by nums
  //to be done
  return brandlist;
}

function getRanges(itemlist)
{
  if(itemlist.length === 0){
    return [0,200];
  }
  var min = itemlist[0].item_discount_price;
  var max = min;
  for(var i=1;i<itemlist.length;i++){
    //is it in
    var thisprice = itemlist[i].item_discount_price;
    if (thisprice < min){
      min = thisprice;
    }
    if (thisprice > max){
      max = thisprice;
    }
  }
  return [min,max];
}

export default function ResultsLayout(props) {
  const classes = useStyles();
  //control filter in this component
  const [brandFilters,setbrandFilters] = React.useState([]);
  const [priceRange,setpriceRange] = React.useState([0,10.0]);
  const [priceFilters,setpriceFilters] = React.useState([]);

  const [showList,setshowList] = React.useState([]);

  const brandsfilter = brand=>()=>{
    const newbrands = [...brandFilters];
    const currentIndex = newbrands.findIndex(el=>el.brand === brand);
    if (currentIndex === -1) return;

    const currentState = newbrands[currentIndex].selected

    newbrands[currentIndex].selected = !currentState;
    setbrandFilters(newbrands);
  };

  const valuefilter = (event,newValue)=> {
    setpriceFilters(newValue);
  };

  useEffect(()=>{
    //only when full list change(new search)
    setshowList([])
    
    const ranges = getRanges(props.fullList)
    setbrandFilters(countBrands(props.fullList));
    setpriceRange(ranges);
    setpriceFilters(ranges);
    setshowList(props.fullList);
    //alert("USE effect1s");
  },[props.fullList]);

  useEffect(function applyFilters(){
    //when any filters change
    const [min,max] = priceFilters;
    var toshow = [];
    var brandshow = [];
    brandFilters.forEach(element=>{
      if (element.selected) {
        brandshow.push(element.brand);
      }
    });
    props.fullList.forEach(element => {
      if (element.item_discount_price <= max 
        && element.item_discount_price >= min
        && brandshow.indexOf(element.item_brand)!==-1){
          toshow.push(element);
      }
    });
    setshowList(toshow);
    //alert("USE effect2s");
  },[priceFilters,brandFilters]);
  
  return (
  <React.Fragment>
      <Grid container spacing={0} >
        <Grid item xs={12} md={9} className={classes.mainGrid}>
          
          <EnhancedTable itemList = {showList} /> 

        </Grid>
        <Grid item xs={12} md={3} className={classes.sideGrid}>

          <Filters brands={brandFilters} brandhandler={brandsfilter}
            ranges={priceRange} valuehandler={valuefilter}/>
            
        </Grid> 
      </Grid>
    </React.Fragment>
  );
}