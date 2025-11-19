# n8n arXiv Workflow

An intelligent n8n workflow that automatically retrieves the latest research papers from arXiv, uses a local LLM to generate comprehensive summaries, and delivers digestible insights directly to your Slack channel.

## 🌟 Why This Workflow is Useful

Staying up-to-date with the latest research papers can be overwhelming. With thousands of papers published daily on arXiv, manually reading and understanding each relevant paper is time-consuming and impractical. This workflow solves that problem by:

- **Automated Discovery**: Automatically fetches the latest papers from multiple arXiv categories (AI, Machine Learning, Computer Vision, NLP, etc.)
- **Intelligent Summarization**: Uses a local LLM to generate detailed, structured summaries that capture:
  - Key technical contributions and innovations
  - Experimental results and benchmarks
  - Strengths, limitations, and reproducibility considerations
  - Practical applications and future directions
- **Time-Saving**: Get digestible insights without reading entire papers
- **Privacy-First**: Uses a local LLM, keeping your data private
- **Seamless Integration**: Delivers summaries directly to Slack for easy team sharing

## ✨ Features

- **Multi-Category Support**: Monitors multiple arXiv categories simultaneously (configurable)
- **Smart Text Cleaning**: Removes references, acknowledgments, and other non-essential content before summarization
- **Comprehensive Summaries**: Generates structured summaries including:
  - TL;DR and elevator pitch
  - Technical overview and methodology
  - Experimental results with specific metrics
  - Advantages, limitations, and reproducibility checklist
  - Future work suggestions
- **Batch Processing**: Efficiently processes multiple papers in sequence
- **Error Handling**: Robust workflow design with proper error handling

## 📋 Prerequisites

Before getting started, ensure you have:

1. **n8n installed and running** (self-hosted or cloud)
   - [Installation Guide](https://docs.n8n.io/hosting/installation/)

2. **Local LLM Server** running on `http://127.0.0.1:1234`
   - Compatible with OpenAI-compatible API (e.g., LM Studio, Ollama with OpenAI compatibility)
   - Model: Default `qwen/qwen3-vl-8b` (or any openai compatibile language model)
   - The workflow uses the `/v1/responses` endpoint

3. **Slack Workspace** with:
   - A Slack app created
   - Bot token with permissions to post messages
   - A channel ID where summaries will be posted

## 🚀 Getting Started

### Step 1: Import the Workflow

1. Open your n8n instance
2. Click **"Import from File"** or **"Import from URL"**
3. Select the `src/n8n-arxiv.json` file from this repository
4. The workflow will be imported with all nodes configured

### Step 2: Configure Categories

The workflow is pre-configured to monitor these arXiv categories:
- `cs.AI` (Artificial Intelligence)
- `cs.LG` (Machine Learning)
- `cs.CV` (Computer Vision)
- `cs.CL` (Computation and Language)

To modify categories, edit the **"CS Categories"** node:
```json
{
  "categories": [
    "cat:cs.AI",
    "cat:cs.LG",
    "cat:cs.CV",
    "cat:cs.CL"
  ]
}
```

You can add or remove categories as needed. See [arXiv category taxonomy](https://arxiv.org/category_taxonomy) for available categories.

### Step 3: Configure Slack Integration

1. In the **"Send a message"** node, click on the credentials field
2. Add or select your Slack credentials:
   - **Bot Token**: Your Slack bot's OAuth token (starts with `xoxb-`)
   - **Channel ID**: The Slack channel ID where summaries will be posted
     - You can find this in the channel settings or by right-clicking the channel in Slack

### Step 4: Verify Local LLM Configuration

1. Ensure your local LLM server is running on `http://127.0.0.1:1234`
2. Verify the model name matches (default: `qwen/qwen3-vl-8b`)
3. Test the endpoint by running the workflow manually

### Step 5: Test the Workflow

1. Click **"Execute Workflow"** to run it manually
2. Check your Slack channel for the generated summaries
3. Review the execution logs in n8n for any errors

### Step 6: Schedule the Workflow (Optional)

To run automatically:

1. Replace the **"When clicking 'Execute workflow'"** trigger with a **Schedule Trigger** node
2. Configure your desired schedule (e.g., daily at 9 AM)
3. Save and activate the workflow

## 📊 Workflow Overview

The workflow follows this process:

1. **Category Setup** → Defines which arXiv categories to monitor
2. **Category Loop** → Iterates through each category
3. **Query arXiv API** → Fetches latest 10 papers per category
4. **Parse Results** → Converts XML to JSON and splits into individual papers
5. **Paper Processing Loop** → For each paper:
   - Extracts PDF link
   - Downloads the PDF
   - Extracts text content
   - Cleans the text (removes references, acknowledgments, etc.)
   - Generates comprehensive summary using local LLM
   - Sends formatted summary to Slack

## 🎨 Screenshots

Workflow visualizations are available in the `assets/` folder:
- `daily-arxiv-en.jpg` - English version
- `daily-arxiv-zh.jpg` - Chinese version

## ⚙️ Customization

### Adjust Number of Papers

In the **"Query arXiv API"** node, modify the `max_results` parameter:
```
max_results=10  // Change to desired number
```

### Modify Summary Format

Edit the prompts in the **"Init Prompts"** node:
- `summarize_prompt`: Controls the summary structure and content
- `clean_prompt`: Controls text cleaning behavior

### Change LLM Model

In the **"Summarize Paper"** node, update the `model` field:
```json
"model": "your-model-name"
```

### Adjust Timeout

The LLM request has a 1-hour timeout (3600000ms). Modify in the **"Summarize Paper"** node if needed.

## 🔧 Troubleshooting

### LLM Server Not Responding
- Verify the server is running: `curl http://127.0.0.1:1234/v1/models`
- Check the port number matches (default: 1234)
- Ensure the model is loaded and ready

### Slack Messages Not Sending
- Verify Slack credentials are correct
- Check channel ID is valid
- Ensure bot has permission to post in the channel

### PDF Extraction Failing
- Some papers may not have PDF links available
- Check arXiv API response for paper metadata
- Verify network connectivity

### Timeout Errors
- Increase timeout in **"Summarize Paper"** node
- Consider using a faster model or reducing paper length

## 📝 Notes

- The workflow processes papers sequentially to avoid overwhelming the LLM server
- Text cleaning removes references and non-essential content to improve summary quality
- Summaries are generated in Chinese by default (modify prompts for other languages)
- The workflow is designed to handle errors gracefully and continue processing

## 🤝 Contributing

Feel free to submit issues or pull requests to improve this workflow!

## 📄 License

This workflow is provided as-is for personal and educational use.

