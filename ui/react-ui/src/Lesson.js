import React from "react";
import { withStyles } from '@material-ui/core';
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';
import Snackbar from '@material-ui/core/Snackbar';

import CodeEditor from "./CodeEditor";
import Markdown from "./Markdown";

const styles = theme => ({
    lessonPane: {
        height: '100vh',
        overflow: 'auto',
        padding: 10,
        border: 'solid #000',
        borderWidth: '0px 1px 0px 0px'
    },
    codePane: {
      height: '75vh',
      overflow: 'auto',
      padding: 10,
      border: 'solid #000',
      borderWidth: '0px 0px 1px 0px'
    },
    buttonPane: {
        height: '10vh',
        padding: 10
    },
    debugPane: {
      height: '15vh',
      padding: 10,
      overflow: 'auto',
      whiteSpace: 'pre-line'
    },
    button: {
        margin: theme.spacing(1),
      }
  });

class Lesson extends React.Component {
    constructor() {
        super();
        this.state = {
            'initial_code': '',
            'vuln_code': '',
            'description': '',
            'language': '',
            'debug_console': '',
            'prev_slug': '',
            'next_slug': '',
            'show_debug_message': false,
            'show_waiting_message': false,
            'debug_message': ''
        };
    }

    codeUpdate = code => this.setState({vuln_code: code})

    checkCode() {
        this.setState({
            'show_waiting_message': true,
            'debug_console': '',
            'debug_message': ''
        });
        fetch('/api/courses/' + this.props.match.params.courseSlug 
                + '/lessons/' + this.props.match.params.lessonSlug + '/check',{
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-type': 'application/json'
            },
            body: JSON.stringify({
                'code': this.state.vuln_code
            })
        }).then(function(response){
            return response.json();
        }).then(data => {
            this.setState({
                debug_message: data.message, 
                debug_console: data.console,
                show_debug_message: true,
                show_waiting_message: false});
        });
    }

    updateStateFromApi(params) {
        fetch('/api/courses/' + params.courseSlug
                + '/lessons/' + params.lessonSlug).then(function(response){
            return response.json();
        }).then(lessonInfo => {
            this.setState({
                'initial_code': lessonInfo['vulnerable_code'],
                'vuln_code': lessonInfo['vulnerable_code'],
                'description': lessonInfo['description'],
                'language': lessonInfo['language'],
                'prev_slug': lessonInfo['prev_slug'],
                'next_slug': lessonInfo['next_slug'],
                'debug_console': ''
            });
        });
    }

    componentDidMount() {
        this.updateStateFromApi(this.props.match.params);
    }

    componentWillReceiveProps(nextProps) {
        this.updateStateFromApi(nextProps.match.params);
    }

    render () {
        const { classes } = this.props;
        
        return (
        <div>
            <Grid container spacing={12}>
                <Grid item xs={4} className={classes.lessonPane}>
                    <Markdown className={classes.markdown} source={this.state.description}/>
                </Grid>
                <Grid container item xs={8} spacing={12}>
                    <Grid item xs={12} className={classes.codePane}>
                        <CodeEditor code={this.state.vuln_code} language={this.state.language}
                            onChange={this.codeUpdate} />
                    </Grid>
                    <Grid container xs={12} spacing={12} className={classes.buttonPane}>
                        <Grid item xs={6}>
                            <Button variant="outlined" color="primary" className={classes.button}
                                onClick={() => {
                                    this.checkCode();
                                    }}
                                >
                                Check
                            </Button>
                            <Button variant="outlined" color="secondary" className={classes.button}
                                onClick={() => { this.setState({'vuln_code': this.state.initial_code, "debug_console": '' }); }}>
                                Reset
                            </Button>
                        </Grid>
                        <Grid item xs={6}>
                            <Button className={classes.button} disabled={this.state.prev_slug === ''}
                                onClick={() => { this.props.history.push('/courses/' 
                                                + this.props.match.params.courseSlug + '/' + this.state.prev_slug); }}
                            >
                                Prev
                            </Button>
                            <Button className={classes.button} disabled={this.state.next_slug === ''}
                                onClick={() => { this.props.history.push('/courses/'
                                                + this.props.match.params.courseSlug + '/' + this.state.next_slug); }}
                            >
                                Next 
                            </Button>
                            
                        </Grid>
                    </Grid>
                    <Grid item xs={12} className={classes.debugPane}>
                        { this.state.debug_console }
                    </Grid>
                </Grid>

            </Grid>
            <Snackbar
                ref="snackbar"
                anchorOrigin={{
                    vertical: 'top',
                    horizontal: 'right',
                }}
                autoHideDuration={6000}
                message={this.state.debug_message}
                open={this.state.show_debug_message}
                onClose={(event, reason) => {this.setState({'show_debug_message': false})}}
            />
            <Snackbar
                anchorOrigin={{
                    vertical: 'bottom',
                    horizontal: 'right',
                }}
                autoHideDuration={10000}
                message="Run tests. Wait, please..."
                open={this.state.show_waiting_message}
                onClose={(event, reason) => {this.setState({'show_waiting_message': false})}}
            />
        </div>
        );
    }
}

export default withStyles(styles)(Lesson);