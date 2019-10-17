import React from 'react';
import { createMuiTheme } from '@material-ui/core/styles';
import { ThemeProvider } from '@material-ui/styles';
import { amber } from '@material-ui/core/colors';
import { red } from '@material-ui/core/colors';

const theme = createMuiTheme({
  palette: {
    primary: { main: amber[500] }, // Purple and green play nicely together.
    secondary: { main: red[500] }, // This is just green.A700 as hex.
  },
});

export default function Theme(props) {
  return (
    <ThemeProvider theme={theme}>
      {props.children}
    </ThemeProvider>
  );
}