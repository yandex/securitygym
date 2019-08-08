import React from 'react';
import Container from '@material-ui/core/Container';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import Link from '@material-ui/core/Link';

class Login extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            username: '',
            password: ''
        }
    }

    handleSignIn(event) {
        fetch('/api/auth/login', {
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
            if (response.status === 403) {
                return response.json().then(json => {
                    throw new Error(json.error);
                });
            } else if (response.status === 200) {
                this.props.checkLoginStatus();
                this.props.history.push("/");
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
            <Container maxWidth="xs">
                <Typography component="h1" variant="h2">
                    Sign In
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
                    onClick={(event) => this.handleSignIn(event)}
                >
                    Sign In
                </Button>
                <Grid container>
                    <Grid item>
                        <Link href="/register">
                            {"Don't have an account? Sign Up"}
                        </Link>
                    </Grid>
                </Grid>
            </Container>
        );
    }
}

export default Login;