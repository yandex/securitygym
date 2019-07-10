import React from 'react';
import ReactMarkdown from 'react-markdown';

function Markdown(props) {
    return <ReactMarkdown source={props.source}/>
}

export default Markdown;