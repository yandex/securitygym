import React from 'react';
import Container from '@material-ui/core/Container';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import Snackbar from '@material-ui/core/Snackbar';
import { withRouter } from "react-router-dom";

class Register extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            username: '',
            password: '',
            error_message: '',
            show_error_message: false
        }
    }

    handleSignUp(event) {
        fetch('/api/auth/register', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-type': 'application/json'
            },
            body: JSON.stringify({
                'username': this.state.username,
                'password': this.state.password
            })
        }).then((response) => {
            if (response.status === 400) {
                return response.json().then(json => {
                    throw new Error(json.error);
                });
            } else if (response.status === 200) {
                this.props.history.push("/login");
            }
        }).catch((error) => {
            this.setState({
                error_message: error.message,
                show_error_message: true
            });
        });
    }

    render() {
        return (
            <div>
            <Container maxWidth="xs">
                <Typography component="h1" variant="h2">
                    Sign Up
                </Typography>
                <TextField
                    variant="outlined"
                    margin="normal"
                    required
                    fullWidth
                    name="username"
                    id="username"
                    label="Username"
                    autocomplete="username"
                    autofocus
                    onChange = {(event) => this.setState({username: event.target.value})}
                />
                <TextField
                    variant="outlined"
                    margin="normal"
                    required
                    fullWidth
                    name="password"
                    id="password"
                    label="Password"
                    type="password"
                    onChange = {(event) => this.setState({password: event.target.value})}
                />
                <Button
                    type="sumbit"
                    fullWidth
                    variant="contained"
                    color="primary"
                    onClick={(event) => this.handleSignUp(event)}
                >
                    Sign Up
                </Button>
            </Container>
            <Snackbar
                ref="snackbar"
                anchorOrigin={{
                    vertical: 'top',
                    horizontal: 'center',
                }}
                autoHideDuration={6000}
                message={this.state.error_message}
                open={this.state.show_error_message}
                onClose={(event, reason) => {this.setState({'show_error_message': false})}}
            />
            </div>
        );
    }
}

export default withRouter(Register);