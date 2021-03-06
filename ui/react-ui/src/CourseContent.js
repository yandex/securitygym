import React from "react";
import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import Card from '@material-ui/core/Card';
import CardMedia from '@material-ui/core/CardMedia';
import CardContent from '@material-ui/core/CardContent';
import CardActionArea from '@material-ui/core/CardActionArea';
import DoneIcon from '@material-ui/icons/Done';
import LinearProgress from '@material-ui/core/LinearProgress';

const COMMON_TITLE = 'Security Courses';
const COMMON_ABSTRACT = 'Choose your specialization';

class CourseContent extends React.Component {

    constructor() {
        super();
        this.state = {
            'content': [],
            'title': 'Security Courses',
            'abstract': 'Choose your specialization',
        }
    }

    fetchLessons(courseSlug) {
        return fetch('/api/courses/'+courseSlug+'/lessons').then(function(response){
            return response.json();
        })
    }

    fetchCourseInfo(courseSlug) {
        return fetch('/api/courses/'+courseSlug).then(function(response){
            return response.json();
        })
    }


    componentDidMount() {
        if (this.props.match.params.hasOwnProperty('courseSlug')) {
            this.fetchCourseInfo(this.props.match.params.courseSlug).then(
                course => {
                    this.setState({'title': course.title, 'abstract': course.abstract});
            });
            this.fetchLessons(this.props.match.params.courseSlug).then(
                courses => {
                    this.setState({'content': courses});
            });
        } else {
            this.setState({'title': COMMON_TITLE, 'abstract': COMMON_ABSTRACT});
            fetch('/api/courses/').then(function(response){
                return response.json();
            }).then(courses => {
                this.setState({'content': courses});
            });
        }
    }

    componentWillReceiveProps(nextProps) {
        if (nextProps.match.params.hasOwnProperty('courseSlug')) {
            this.fetchCourseInfo(nextProps.match.params.courseSlug).then(
                course => {
                    this.setState({'title': course.title, 'abstract': course.abstract});
            });
            this.fetchLessons(nextProps.match.params.courseSlug).then(
                courses => {
                    this.setState({'content': courses});
            });
        } else {
            this.setState({'title': COMMON_TITLE, 'abstract': COMMON_ABSTRACT});
            fetch('/api/courses/').then(function(response){
                return response.json();
            }).then(courses => {
                this.setState({'content': courses});
            });
        }
    }

    render () {
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
                <Grid container spacing={4}>
                    {this.state.content.map(course => (
                        <Grid item key={course.slug} xs={12} sm={6} md={4}>
                            <Card>
                                <CardActionArea
                                    onClick={() => { 
                                        if (this.props.match.params.hasOwnProperty('courseSlug')) {
                                            this.props.history.push('/courses/' + this.props.match.params.courseSlug 
                                                + '/' + course.slug);
                                        } else {
                                            this.props.history.push('/courses/' + course.slug);
                                        } 
                                    }}
                                >
                                    <CardMedia 
                                        image={"/api/"+course.logo}
                                        title={course.title}
                                        style={{
                                            maxHeight: "256px",
                                            height: "256px"
                                        }}
                                    />
                                    <CardContent
                                        style={{
                                            maxHeight: "120px",
                                            height: "120px"
                                        }}
                                    >
                                        <Typography gutterBottom variant="h5" component="h2">
                                            {course.title} {course.solved && <DoneIcon/>}
                                        </Typography>
                                        <Typography>
                                            {course.abstract}
                                        </Typography>
                                    </CardContent>
                                    <CardContent>
                                        <LinearProgress
                                            variant="determinate" 
                                            value={course.progress} 
                                        />
                                    </CardContent>
                                </CardActionArea>
                            </Card>
                        </Grid>
                    ))}

                </Grid>
            </Container>
        </div>);
    }
}

export default CourseContent;