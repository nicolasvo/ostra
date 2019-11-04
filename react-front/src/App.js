import React, { Component } from 'react';

const API = 'http://localhost:5000';


class FetchApproach extends Component {
  constructor(props) {
    super(props);

    this.state = {
      words: [],
      isLoading: false,
      error: null,
    };
  }

  componentDidMount() {
    this.setState({ isLoading: true });

    fetch(API)
      .then(response => {
        if (response.ok) {
          console.log(response);
          return response.json();
        } else {
          throw new Error('Something went wrong...');
        }
      })
      .then(data => this.setState({ words: data, isLoading: false }))
      .catch(error => this.setState({ error, isLoading: false }));

  }

  render() {
    const { words, isLoading, error } = this.state;
    const columns = ["en", "ru", "es"];
    const data = words.map(word =>
      columns.map(language =>
        word[language]
      )
    );

    if (error) {
      return <p>{error.message}</p>;
    }

    if (isLoading) {
      return <p style={{textAlignVertical: "center",textAlign: "center",}}>Warte...</p>;
    }

    // console.log(Object.keys(words));

    return (
      <table border="1">
        <tr>
        {columns.map(language =>
          <th>{language}</th>
        )}
        </tr>
        {words.map((word, index) =>
          <tr id={index+1}>
          {columns.map(language =>
            <td>{word[language].toLowerCase()}</td>
          )}
          </tr>
        )}
      </table>
    );
  }
}

export default FetchApproach;
