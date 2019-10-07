import React, { Component } from 'react';
import { BrowserRouter as Router, Switch, Route, withRouter, Link } from 'react-router-dom';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Button from '@material-ui/core/Button';
import Menu from '@material-ui/core/Menu';
import MenuItem from '@material-ui/core/MenuItem';
import CourseContent from './CourseContent';
import Lesson from './Lesson';
import Login from './Login';
import Register from './Register';
import Statistics from './Statistics';

class Nav extends Component {

    constructor(props) {
        super(props);
        this.state = {
            menuOpen: false,
            mainMenuOpen: false,
        }
    }

    logout() {
        this.setState({
            menuOpen: false,
            mainMenuOpen: false,
        });
        fetch('/api/auth/logout').then(() => {
            this.props.checkLoginStatus();
        })
    }

    render() {
        return (
            <div>
                <AppBar position="relative">
                    <Toolbar>
                        <div>
                            <Menu
                                id="main-menu"
                                open={this.state.mainMenuOpen}
                                onClose={() => {this.setState({mainMenuOpen: false})}}
                                getContentAnchorEl={null}
                                    anchorOrigin={{
                                        vertical: 'top',
                                        horizontal: 'left',
                                    }}
                                    transformOrigin={{
                                        vertical: 'top',
                                        horizontal: 'left',
                                    }}
                            >
                                <MenuItem component={Link} to={'/'} onClick={() => {this.setState({mainMenuOpen: false})}}>
                                    Home
                                </MenuItem>
                                <MenuItem component={Link} to={'/statistics'} onClick={() => {this.setState({mainMenuOpen: false})}}>
                                    Statistics
                                </MenuItem>
                            </Menu>
                            <Button color="inherit" onClick={() => {this.setState({mainMenuOpen: true})}}>Security Gym</Button>
                        </div>
                        
                        <span style={{marginLeft: "auto"}}>
                        {!this.props.isLogged && (
                            <div>
                            <Button color="inherit" component={Link} to={'/login'}>Sign In</Button>
                            <Button color="inherit" variant="outlined" component={Link} to={'/register'}>Sign Up</Button>
                            </div>
                        )}
                        {this.props.isLogged && (
                            <div>
                                <Menu
                                    id="user-menu"
                                    open={this.state.menuOpen}
                                    onClose={() => {this.setState({menuOpen: false})}}
                                    getContentAnchorEl={null}
                                    anchorOrigin={{
                                        vertical: 'top',
                                        horizontal: 'right',
                                    }}
                                    transformOrigin={{
                                        vertical: 'top',
                                        horizontal: 'right',
                                    }}
                                >   
                                    <MenuItem onClick={()=>{this.logout()}}>Logout</MenuItem>
                                </Menu>
                                <Button color="inherit" onClick={() => {this.setState({menuOpen: true})}}>{this.props.username}</Button>
                            </div>
                        )}
                        </span>
                    </Toolbar>
                </AppBar>
            </div>
        )
    }
}

const NavWithRouter = withRouter(Nav);

class App extends Component {

    constructor(props) {
        super(props);
        this.state = {
            isLogged: false,
            username: ''
        }
        this.checkLoginStatus();
    }

    checkLoginStatus = () => {
        fetch('/api/auth/username').then(function(response){
            if (response.status === 200) {
                return response.json();
            } else {
                throw new Error("You are not logged");
            }
        }).then((data) => {
            if(!this.state.isLogged || this.state.username !== data.username) {
                this.setState({
                    isLogged: true,
                    username: data.username
                })
            }
        }).catch((error) => {
            if (this.state.isLogged) {
                this.setState({
                    isLogged: false,
                    username: ''
                })
            }
        });
    }

    render() {
        return (
            <React.Fragment>
                <Router>
                    <div>
                        <NavWithRouter {...this.props} isLogged={this.state.isLogged} username={this.state.username}
                            checkLoginStatus={this.checkLoginStatus}
                        />
                        <Switch>
                            <Route exact path='/' component={CourseContent} />
                            <Route exact path='/courses' component={CourseContent} />
                            <Route exact path='/courses/:courseSlug' component={CourseContent} />
                            <Route exact path='/courses/:courseSlug/:lessonSlug' render={
                                props => <Lesson {...props} isLogged={this.state.isLogged}/>
                            } />
                            <Route exact path='/login' render={
                                props => <Login {...props} checkLoginStatus={this.checkLoginStatus}/>
                            } />
                            <Route exact path='/register' component={Register} />
                            <Route exact path='/statistics' component={Statistics} />
                        </Switch>
                    </div>
                </Router>
            </React.Fragment>
        );
    }
}

export default App;