# Customer Call Transcript Analyzer

A web-based application that uses AI to analyze customer service call transcripts, providing automated summaries and sentiment analysis. Built with Gradio for the interface and powered by Groq's Llama 3.3 model for natural language processing.

## Overview

This tool helps customer service teams and managers quickly analyze call transcripts by:
- Generating concise summaries of customer interactions
- Classifying customer sentiment (Positive, Neutral, Negative)
- Storing analysis results in CSV format for historical tracking
- Providing an intuitive web interface for easy operation

## Technical Architecture

### Core Components

**Frontend Interface**: Gradio-based web application with custom CSS styling
**AI Processing**: Groq API integration using Llama 3.3-70B model
**Data Storage**: Local CSV file system for persistent storage
**File Management**: Pandas for CSV operations and data manipulation

### Dependencies

```
gradio
groq
pandas
os (built-in)
csv (built-in)
datetime (built-in)
```

## How the Code Works

### 1. Initialization and Configuration

The application starts by importing required libraries and initializing the Groq client with an API key from environment variables. A sample transcript is defined for testing purposes.

```python
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
client = Groq(api_key=GROQ_API_KEY)
```

### 2. AI Analysis Function

The `analyze_with_groq()` function performs the core AI processing:

**Summary Generation**:
- Sends the transcript to Groq API with a prompt requesting a 2-3 sentence summary
- Uses temperature of 0.3 for balanced creativity and consistency
- Limits response to 150 tokens for concise output

**Sentiment Analysis**:
- Makes a second API call with a sentiment classification prompt
- Uses lower temperature (0.1) for more deterministic results
- Restricts output to single word classification

### 3. Data Persistence

The `save_to_csv()` function handles data storage:
- Checks if CSV file exists to determine header requirements
- Truncates long transcripts to 500 characters for storage efficiency
- Appends new analysis results with timestamp
- Uses UTF-8 encoding to handle special characters

### 4. Main Processing Pipeline

The `analyze_transcript()` function orchestrates the workflow:
1. Validates input transcript is not empty
2. Calls AI analysis function
3. Saves results to CSV file
4. Updates CSV for download functionality
5. Returns results to the interface

### 5. User Interface Components

**Input Section**:
- Large text area for transcript input
- Sample data loader for testing
- Clear function for resetting fields

**Results Display**:
- Summary output field
- Sentiment classification display
- Status messages for user feedback
- CSV file download component

**Data Management**:
- Historical data viewer
- CSV contents display functionality

### 6. Event Handling

The application uses Gradio's event system:
- Button clicks trigger specific functions
- Input validation prevents empty submissions
- Error handling provides user feedback
- File operations update interface components

### 7. Styling and User Experience

Custom CSS provides professional appearance:
- Gradient headers and modern design elements
- Responsive layout for different screen sizes
- Color-coded sections for better organization
- Hover effects and smooth transitions

## Setup and Installation

### Local Development

1. Clone the repository
2. Install required dependencies:
   ```bash
   pip install gradio groq pandas
   ```
3. Set your Groq API key:
   ```bash
   export GROQ_API_KEY='your_actual_api_key_here'
   ```
4. Run the application:
   ```bash
   python app.py
   ```

### Hugging Face Spaces Deployment

1. Upload the code to a new Hugging Face Space
2. Add your Groq API key as a Space Secret named `GROQ_API_KEY`
3. The application will automatically launch on the platform

## Usage Instructions

### Basic Operation

1. **Input Transcript**: Paste your customer service call transcript into the text area
2. **Analyze**: Click the "Analyze Transcript" button to process the conversation
3. **Review Results**: Check the generated summary and sentiment classification
4. **Download Data**: Use the CSV download link to save results locally
5. **View History**: Click "View Stored Data" to see accumulated analysis results

### Sample Data

Use the "Load Sample" button to populate the input field with example data for testing the application functionality.

## Data Format

### Input Format
Transcripts should include speaker identification and dialogue:
```
Agent: Hello, how can I help you today?
Customer: I'm having trouble with my order...
```

### Output CSV Structure
- **Timestamp**: Analysis date and time
- **Transcript**: First 500 characters of original text
- **Summary**: AI-generated summary
- **Sentiment**: Classification result (Positive/Neutral/Negative)

## API Integration

The application integrates with Groq's API using two distinct approaches:

**Summary Generation**: Uses creative prompting to extract key information and resolution details from the conversation.

**Sentiment Classification**: Employs focused prompting with strict output constraints to ensure consistent sentiment categorization.

Both API calls use error handling to manage network issues and API limitations gracefully.

## File Management

The application automatically manages CSV files:
- Creates new files when none exist
- Appends data to existing files
- Maintains proper CSV formatting
- Handles file encoding for international characters

## Error Handling

Comprehensive error handling covers:
- Missing API keys (warns user but continues operation)
- Network connectivity issues with Groq API
- File system permissions and disk space
- Invalid input data formatting
- CSV parsing and writing errors

## Performance Considerations

The application is optimized for efficiency:
- Truncates long transcripts for storage
- Uses appropriate model temperature settings
- Implements file existence checks before operations
- Manages memory usage with Pandas operations

## Security Notes

- API keys are loaded from environment variables
- No sensitive data is logged or displayed
- CSV files are stored locally (not transmitted)
- Input validation prevents malicious content processing
