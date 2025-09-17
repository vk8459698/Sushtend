import os
import csv
import pandas as pd
from datetime import datetime
import gradio as gr
from groq import Groq

# Initialize Groq client
# For Hugging Face deployment, set this as a Space Secret
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
client = Groq(api_key=GROQ_API_KEY)

# Sample transcript for testing
SAMPLE_TRANSCRIPT = """Agent: Hello, thank you for calling TechSupport Inc. How can I help you today?
Customer: Hi, I've been trying to book a time slot for a technician visit since yesterday, but every time I try to pay, the payment fails. It's really frustrating because I need this fixed urgently.
Agent: I'm sorry to hear about the payment issues you're experiencing. Let me check your account and see what might be causing this problem.
Customer: I've tried three different credit cards and none of them work. This is ridiculous! I'm a premium customer and I shouldn't have to deal with this.
Agent: I completely understand your frustration, and I apologize for the inconvenience. I can see there was a temporary issue with our payment gateway yesterday. Let me process your booking manually and waive the booking fee as an apology.
Customer: Oh, that would be great! Thank you so much. When can the technician come?
Agent: I can schedule you for tomorrow between 2-4 PM. Does that work for you?
Customer: Perfect! Thank you for resolving this so quickly."""

def analyze_with_groq(transcript):
    """
    Use Groq API to summarize the conversation and extract sentiment
    """
    try:
        if not transcript.strip():
            return "Please provide a transcript to analyze.", "No sentiment available"
            
        # Summarize the conversation
        summary_prompt = f"""
        Please summarize the following customer service call transcript in 2-3 clear, concise sentences:
        
        {transcript}
        
        Focus on the main issue, how it was resolved, and the outcome.
        """
        
        summary_response = client.chat.completions.create(
            messages=[{"role": "user", "content": summary_prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=150
        )
        
        summary = summary_response.choices[0].message.content.strip()
        
        # Extract sentiment
        sentiment_prompt = f"""
        Analyze the sentiment of the customer in this call transcript and classify it as one of: Positive, Neutral, or Negative.
        
        {transcript}
        
        Consider the overall tone, satisfaction level, and emotional state of the customer throughout the conversation.
        Respond with just one word: Positive, Neutral, or Negative.
        """
        
        sentiment_response = client.chat.completions.create(
            messages=[{"role": "user", "content": sentiment_prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.1,
            max_tokens=10
        )
        
        sentiment = sentiment_response.choices[0].message.content.strip()
        
        return summary, sentiment
        
    except Exception as e:
        error_msg = f"Error calling Groq API: {str(e)}"
        return error_msg, "Error"

def save_to_csv(transcript, summary, sentiment, filename='call_analysis.csv'):
    """
    Save the analysis results to a CSV file
    """
    try:
        # Check if file exists to determine if we need headers
        file_exists = os.path.isfile(filename)
        
        # Prepare data
        data = {
            'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Transcript': transcript.replace('\n', ' ').replace('\r', ' ')[:500] + ('...' if len(transcript) > 500 else ''),
            'Summary': summary,
            'Sentiment': sentiment
        }
        
        # Write to CSV
        with open(filename, 'a', newline='', encoding='utf-8') as file:
            fieldnames = ['Timestamp', 'Transcript', 'Summary', 'Sentiment']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            # Write header if file is new
            if not file_exists:
                writer.writeheader()
            
            writer.writerow(data)
        
        return True, f"Results saved to {filename}"
        
    except Exception as e:
        return False, f"Error saving to CSV: {str(e)}"

def analyze_transcript(transcript):
    """
    Main function to analyze transcript and save results
    """
    if not transcript.strip():
        return "", "", "Please enter a transcript to analyze.", None
    
    # Analyze with Groq
    summary, sentiment = analyze_with_groq(transcript)
    
    # Save to CSV
    save_success, save_message = save_to_csv(transcript, summary, sentiment)
    
    # Create/update CSV file for download
    try:
        df = pd.read_csv('call_analysis.csv')
        csv_content = df.to_csv(index=False)
        
        # Save updated CSV
        with open('call_analysis.csv', 'w', encoding='utf-8') as f:
            f.write(csv_content)
            
    except Exception as e:
        save_message += f"\nWarning: Could not update CSV display: {str(e)}"
    
    return summary, sentiment, save_message, 'call_analysis.csv'

def load_sample():
    """
    Load sample transcript
    """
    return SAMPLE_TRANSCRIPT

def view_csv_contents():
    """
    View current CSV file contents
    """
    try:
        if os.path.exists('call_analysis.csv'):
            df = pd.read_csv('call_analysis.csv')
            return df.to_string(index=False, max_colwidth=50)
        else:
            return "No CSV file found. Analyze some transcripts first!"
    except Exception as e:
        return f"Error reading CSV: {str(e)}"

# Custom CSS for professional styling
custom_css = """
.gradio-container {
    max-width: 1200px !important;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 12px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.main-header h1 {
    font-size: 2.2rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    letter-spacing: -0.5px;
}

.main-header p {
    font-size: 1.1rem;
    opacity: 0.9;
    margin-bottom: 0.3rem;
}

.info-card {
    background: #0000;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.info-card h3 {
    color: #1e293b;
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 0.8rem;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 0.5rem;
}

.info-card ul {
    list-style: none;
    padding: 0;
}

.info-card li {
    padding: 0.4rem 0;
    position: relative;
    padding-left: 1.5rem;
}

.info-card li:before {
    content: "•";
    color: #667eea;
    font-weight: bold;
    position: absolute;
    left: 0;
}

.results-section {
    background: #000000;
    border: 1px solid #333333;
    border-radius: 10px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.results-section h3 {
    color: #ffffff;
    font-size: 1.3rem;
    font-weight: 600;
    margin-bottom: 1rem;
    text-align: center;
    border-bottom: 2px solid #333333;
    padding-bottom: 0.5rem;
}

.csv-section {
    background: #000000;
    border-radius: 10px;
    padding: 1.5rem;
    margin-top: 2rem;
    border: 1px solid #333333;
}

.csv-section h3 {
    color: #ffffff;
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 1rem;
    text-align: center;
}

.footer-info {
    background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
    padding: 2rem;
    border-radius: 12px;
    margin-top: 2rem;
    text-align: center;
    border: 1px solid #cbd5e1;
}

.footer-info h4 {
    color: #1e293b;
    font-size: 1.3rem;
    font-weight: 600;
    margin-bottom: 0.8rem;
}

.footer-info p {
    color: #475569;
    font-size: 1rem;
    margin-bottom: 0.5rem;
}

/* Button styling */
.gr-button {
    border-radius: 8px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}

.gr-button-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border: none !important;
}

.gr-button-primary:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4) !important;
}

.gr-button-secondary {
    background: #f8fafc !important;
    border: 1px solid #e2e8f0 !important;
    color: #475569 !important;
}

.gr-button-secondary:hover {
    background: #f1f5f9 !important;
    transform: translateY(-1px) !important;
}

/* Input styling */
.gr-textbox textarea {
    border-radius: 8px !important;
    border: 1px solid #d1d5db !important;
    font-size: 14px !important;
}

.gr-textbox textarea:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
}

/* File component styling */
.gr-file {
    border-radius: 8px !important;
    border: 1px solid #d1d5db !important;
}
"""

# Create Gradio interface
with gr.Blocks(
    title="Customer Call Transcript Analyzer",
    theme=gr.themes.Soft(),
    css=custom_css
) as demo:
    
    gr.HTML("""
    <div class="main-header">
        <h1>Customer Call Transcript Analyzer</h1>
        <p>Advanced AI-powered analysis for customer service conversations</p>
        <p>Powered by Groq API & Llama 3.3</p>
    </div>
    """)
    
    with gr.Row():
        with gr.Column(scale=3):
            gr.HTML("""
            <div class="info-card">
                <h3>How to Use This Tool</h3>
                <ul>
                    <li>Paste your customer service call transcript in the text area</li>
                    <li>Click "Analyze Transcript" to generate insights</li>
                    <li>Review the AI-generated summary and sentiment analysis</li>
                    <li>Download your results as a CSV file for record keeping</li>
                    <li>View accumulated analysis data in the CSV viewer</li>
                </ul>
            </div>
            """)
            
            transcript_input = gr.Textbox(
                label="Customer Call Transcript",
                placeholder="Enter the complete customer service call transcript here. Include both agent and customer dialogue for best results...",
                lines=12,
                max_lines=20
            )
            
            with gr.Row():
                analyze_btn = gr.Button("Analyze Transcript", variant="primary", size="lg", scale=3)
                sample_btn = gr.Button("Load Sample", variant="secondary", scale=1)
                clear_btn = gr.Button("Clear All", variant="secondary", scale=1)
        
        with gr.Column(scale=2):
            gr.HTML('<div class="results-section"><h3>Analysis Results</h3>')
            
            summary_output = gr.Textbox(
                label="Executive Summary",
                lines=5,
                interactive=False,
                placeholder="Summary will appear here after analysis..."
            )
            
            sentiment_output = gr.Textbox(
                label="Customer Sentiment Classification",
                lines=2,
                interactive=False,
                placeholder="Sentiment analysis will appear here..."
            )
            
            status_output = gr.Textbox(
                label="Processing Status",
                lines=2,
                interactive=False,
                placeholder="Status updates will appear here..."
            )
            
            download_file = gr.File(
                label="Download Analysis Results (CSV)",
                visible=True
            )
            
            gr.HTML('</div>')
    
    with gr.Row():
        with gr.Column():
            gr.HTML("""
            <div class="csv-section">
                <h3>Historical Analysis Data</h3>
            """)
            
            view_csv_btn = gr.Button("View Stored Data", variant="secondary", size="sm")
            
            csv_contents = gr.Textbox(
                label="Analysis History",
                lines=10,
                interactive=False,
                show_copy_button=True,
                placeholder="Click 'View Stored Data' to see your analysis history..."
            )
            
            gr.HTML('</div>')
    
    # Event handlers
    analyze_btn.click(
        fn=analyze_transcript,
        inputs=[transcript_input],
        outputs=[summary_output, sentiment_output, status_output, download_file]
    )
    
    sample_btn.click(
        fn=load_sample,
        outputs=[transcript_input]
    )
    
    clear_btn.click(
        fn=lambda: ("", "", "", None),
        outputs=[transcript_input, summary_output, sentiment_output, status_output]
    )
    
    view_csv_btn.click(
        fn=view_csv_contents,
        outputs=[csv_contents]
    )
    
   

# For local testing
if __name__ == "__main__":
    print("Starting Customer Call Transcript Analyzer...")
    print("="*60)
    
    # Check for Groq API key
    if not GROQ_API_KEY :
        print("WARNING: Using default/no API key")
        print("   Local development: export GROQ_API_KEY='your_actual_api_key'")
        print("   Hugging Face Spaces: Add as a Space Secret")
        print()
    else:
        print("API key detected successfully")
        print()
    
    # Launch the app
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,  # Set to True for public sharing during development
        show_error=True
    )
