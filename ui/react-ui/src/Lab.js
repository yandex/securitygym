import React from "react";
import { withStyles } from '@material-ui/core';
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';

import CodeEditor from "./CodeEditor";
import Markdown from "./Markdown";

import labs from "./lessons/labs.js";

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

class Lab extends React.Component {
    constructor() {
        super();
        this.state = {
            'lab': {},
            'vuln_code': '',
            'md_theory': '',
            'debug_output': '',
            'prev': '',
            'next': ''
        };
    }

    codeUpdate = code => this.setState({vuln_code: code})

    checkCode() {
        fetch('/api/check_code',{
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-type': 'application/json'
            },
            body: JSON.stringify({
                'code': this.state.vuln_code,
                'lab': this.props.match.params.exerciseSlug
            })
        }).then(function(response){
            return response.json();
        }).then(data => {
            this.setState({debug_output: data.message});
        })
    }

    componentDidMount() {
        this.setState({
            'lab': labs[this.props.match.params.exerciseSlug],
            'vuln_code': labs[this.props.match.params.exerciseSlug]['code'],
            'md_theory': labs[this.props.match.params.exerciseSlug]['md'],
            'prev': labs[this.props.match.params.exerciseSlug]['prev'],
            'next': labs[this.props.match.params.exerciseSlug]['next'],
        });
    }

    componentWillReceiveProps(nextProps) {
        this.setState({
            'lab': labs[nextProps.match.params.exerciseSlug],
            'vuln_code': labs[nextProps.match.params.exerciseSlug]['code'],
            'md_theory': labs[nextProps.match.params.exerciseSlug]['md'],
            'prev': labs[nextProps.match.params.exerciseSlug]['prev'],
            'next': labs[nextProps.match.params.exerciseSlug]['next'],
        });
    }

    render () {
        const { classes } = this.props;
        
        return (
        <div>
            <Grid container spacing={12}>
                <Grid item xs={4} className={classes.lessonPane}>
                    <Markdown className={classes.markdown} source={this.state.md_theory}/>
                </Grid>
                <Grid container item xs={8} spacing={12}>
                    <Grid item xs={12} className={classes.codePane}>
                        <CodeEditor code={this.state.vuln_code} onChange={this.codeUpdate} />
                    </Grid>
                    <Grid container xs={12} spacing={12} className={classes.buttonPane}>
                        <Grid item xs={6}>
                            <Button variant="outlined" color="primary" className={classes.button}
                                onClick={() => {this.checkCode()}}
                                >
                                Check
                            </Button>
                            <Button variant="outlined" color="secondary" className={classes.button}
                                onClick={() => { this.setState({'vuln_code': this.state.lab.code, "debug_output": '' }); }}>
                                Reset
                            </Button>
                        </Grid>
                        <Grid item xs={6}>
                            <Button className={classes.button} disabled={this.state.prev === ''}
                                onClick={() => { this.props.history.push('/exercise/'+this.state.prev); }}
                            >
                                Prev
                            </Button>
                            <Button className={classes.button} disabled={this.state.next === ''}
                                onClick={() => { this.props.history.push('/exercise/'+this.state.next); }}
                            >
                                Next 
                            </Button>
                            
                        </Grid>
                    </Grid>
                    <Grid item xs={12} className={classes.debugPane}>
                        { this.state.debug_output }
                    </Grid>
                </Grid>

            </Grid>
            
        </div>
        );
    }
}

export default withStyles(styles)(Lab);