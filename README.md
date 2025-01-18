<<<<<<< HEAD

# iMessage Analytics Wrapped

An advanced analytics tool that provides deep insights into your iMessage communication patterns, combining sentiment analysis, linguistic patterns, and behavioral metrics to create a comprehensive messaging wrap-up.

## Features

### Core Analytics
* **Message Volume Analysis**
  * Total message counts and sent/received ratios
  * Percentage breakdowns of messaging patterns
  * Historical message distribution

### Sentiment Analysis
* **VADER-powered Sentiment Scoring**
  * Individual message sentiment scoring
  * Conversation-level sentiment aggregation
  * Personal sentiment baseline calculation
* **Contact Rankings**
  * Top 10 most messaged contacts
  * Sentiment-based positivity rankings
  * Message volume statistics per contact

### Linguistic Analysis
* **Vocabulary Metrics**
  * Frequently used words tracking
  * Custom word lookup functionality
  * Average message length calculation
* **Language Pattern Detection**
  * Curse word frequency monitoring
  * Stop word filtering
  * Reaction message filtering

### Communication Style Analysis
* **Politeness Metrics**
  * Detection of courtesy markers
  * Politeness scoring per conversation
* **Conversation Blend Rate**
  * Jaccard similarity calculation
  * Language style matching analysis
  * Communication pattern synchronization

## Technical Requirements

### System Requirements
* macOS (due to iMessage database location)
* Python 3.9+
* Access to iMessage database (`chat.db`)

### Dependencies
```bash
pip install nltk sqlite3-Utils datetime-utils statistics
```

### NLTK Requirements
```python
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('vader_lexicon')
```

## Installation & Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/imessage-analytics.git
cd imessage-analytics
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure database path:
```python
username = "yourusername"  # Update with your system username
DB_PATH = f"/Users/{username}/Library/Messages/chat.db"
```

## Usage

### Basic Analysis
```python
python analyze_messages.py
```

### Features Configuration
* **Sentiment Analysis Settings**
  * Adjust sentiment thresholds in `SentimentIntensityAnalyzer`
  * Modify politeness markers in `POLITENESS_MARKERS`
* **Text Processing**
  * Customize stop words in `STOP_WORDS`
  * Update reaction keywords list as needed

## Output

### Sentiment Analysis
* Personal sentiment score and positivity rating
* Top 10 contacts ranked by:
  * Message count
  * Positivity score
  * Average sentiment

### Communication Metrics
* Politeness ratings for top contacts
* Conversation blend rates
* Language similarity scores

### Word Usage Statistics
* Word frequency distribution
* Custom word lookup results
* Curse word frequency

## Privacy & Security Notes

* This tool analyzes local iMessage data only
* No data is transmitted or stored externally
* Personal message content remains private
* Exercise caution when sharing analysis results

## Known Limitations

* Database access may be restricted by macOS security settings
* Analysis depth depends on local database completeness
* Performance may vary with large message volumes
* Some message types may not be properly categorized
* iMessage database does not store contact names

## Future Enhancements

* Interactive visualization dashboard
* Temporal analysis patterns
* Emoji usage analytics
* Response time analysis
* Topic modeling implementation
* Conversation context analysis
* Relationship dynamics insights

## Contributing

Contributions are welcome! Please feel free to submit pull requests or create issues for bugs and feature requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
=======
# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
>>>>>>> 950334e (Initial Commit)
