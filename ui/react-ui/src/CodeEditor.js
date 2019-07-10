
import React from "react";

import Editor from "react-simple-code-editor";
import { highlight, languages } from "prismjs/components/prism-core";
import "prismjs/components/prism-clike";
import "prismjs/components/prism-javascript";
import "prismjs/components/prism-python";

class CodeEditor extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        code: props.code
      };
    }

    componentWillReceiveProps(nextProps) {
      this.setState({code: nextProps.code});
    }

    render() {
      
        return (
          <div
            style={{
              overflow: "auto",
              maxHeight: "100%",
              height: "100%"
            }}
          >
            <Editor
              value={this.state.code}
              onValueChange={code => { this.props.onChange(code); this.setState({ code })} }
              highlight={code => highlight(code, languages.python)}
              padding={10}
              tabSize={4}
              selectionColor="green"
              style={{
                fontFamily: '"Fira code", "Fira Mono", monospace',
                fontSize: 12
              }}
            />
          </div>
        );
    }
}

export default CodeEditor;