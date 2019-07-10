import React, { Component } from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import CourseContent from './CourseContent';
import Lab from './Lab';

class App extends Component {
    render() {
        return (
            <React.Fragment>
                <AppBar position="relative">
                    <Toolbar>
                        <Button color="inherit" href="/">Security Gym</Button>
                    </Toolbar>
                </AppBar>
                <Router>
                    <Switch>
                        <Route exact path='/' component={CourseContent} />
                        <Route path='/courses/:courseSlug' component={CourseContent} />
                        <Route path='/courses/:courseSlug/:exerciseSlug' component={Lab} />
                    </Switch>
                </Router>
            </React.Fragment>
        );
    }
}

export default App;