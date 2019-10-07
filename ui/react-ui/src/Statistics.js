import React from 'react';
import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';
import Table from '@material-ui/core/Table';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import TableCell from '@material-ui/core/TableCell';
import TableBody from '@material-ui/core/TableBody';

const COMMON_TITLE = 'Statistics';
const COMMON_ABSTRACT = 'All courses';

class Statistics extends React.Component {

    constructor() {
        super();
        this.state = {
            'title': 'Security Courses',
            'abstract': 'Choose your specialization',
            'header': [],
            'content': []
        }
    }

    componentDidMount() {
        if (this.props.match.params.hasOwnProperty('courseSlug')) {
        } else {
            this.setState({'title': COMMON_TITLE, 'abstract': COMMON_ABSTRACT});
            fetch('/api/statistics').then(function(response){
                return response.json();
            }).then(statistics => {
                this.setState({
                    'header': statistics['statistics_header'],
                    'content': statistics['statistics_content']
                });
            });
        }
    }

    render() {
        return (
            <div>
                <div>
                    <Container maxWidth="sm">
                        <Typography component="h1" variant="h2" align="center" color="textPrimary" gutterBottom>
                            {this.state.title}
                        </Typography>
                        <Typography variant="h5" align="center" color="textSecondary" paragraph>
                            {this.state.abstract}
                        </Typography>
                    </Container>
                </div>
                <Container maxWidth="md">
                    <Table size="small">
                        <TableHead>
                            <TableRow>
                                <TableCell>Username</TableCell>
                                {
                                    this.state.header.map(course => (
                                    <TableCell align="right">{course['title']}</TableCell>
                                    ))
                                }
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {this.state.content.map(row => (
                                <TableRow key={row.uid}>
                                    <TableCell component="th" scope="row">{row.username}</TableCell>
                                    {
                                        this.state.header.map(course => (
                                        <TableCell align="right">
                                            {row.courses[course['slug']].progress}&nbsp;%
                                        </TableCell>
                                        ))
                                    }
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </Container>
            </div>
        );
    }
}

export default Statistics;