# Investapp - Financial News Analyzer

A Python-based financial news analysis tool that fetches news from NewsAPI, analyzes sentiment and stock impacts using OpenRouter's free AI models, and stores results in JSON format.

## 🚀 Features

- **News Fetching**: Retrieves financial news from NewsAPI (free tier: 100 requests/day)
- **AI Analysis**: Analyzes sentiment (positive, negative, neutral) using OpenRouter's free AI models
- **Stock Impact Assessment**: Identifies affected stocks and their potential impact
- **Structured Output**: Stores results in organized JSON format
- **Rate Limiting**: Handles API limits and request throttling
- **Error Handling**: Graceful error handling and fallback mechanisms

## 📋 Requirements

- Python 3.7+
- NewsAPI account (free tier available)
- OpenRouter account (free tier available)

## 🛠️ Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API keys**:
   - Create a `.env` file in the project directory
   - Copy the contents from `env_example.txt` to `.env`
   - Replace placeholder values with your actual API keys

## 🔑 API Setup

### NewsAPI Setup
1. Go to [NewsAPI.org](https://newsapi.org/)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Add it to your `.env` file as `NEWS_API_KEY`

### OpenRouter Setup
1. Go to [OpenRouter.ai](https://openrouter.ai/)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Add it to your `.env` file as `OPENROUTER_API_KEY`

## 🎯 Usage

### Basic Usage
```bash
python financial_news_analyzer.py
```

### Custom Analysis
```python
from financial_news_analyzer import FinancialNewsAnalyzer

# Initialize analyzer
analyzer = FinancialNewsAnalyzer()

# Run custom analysis
results = analyzer.run_analysis(
    query="technology stocks earnings",
    max_articles=5
)
```

## 📊 Output Format

The script generates a JSON file (`financial_news_analysis.json`) with the following structure:

```json
{
  "analysis_metadata": {
    "total_articles": 3,
    "analysis_date": "2024-01-15T10:30:00",
    "news_api_requests_used": 1,
    "model_used": "meta-llama/llama-2-70b-chat"
  },
  "articles": [
    {
      "headline": "Apple Reports Record Q4 Earnings",
      "description": "Apple Inc. reported record-breaking quarterly earnings...",
      "url": "https://example.com/article",
      "publishedAt": "2024-01-15T09:00:00Z",
      "source": "Financial Times",
      "sentiment": "positive",
      "affected_stocks": ["AAPL", "TSLA"],
      "impact_description": "Apple's strong earnings could boost tech sector confidence and potentially lift related stocks",
      "confidence": "high",
      "analysis_timestamp": "2024-01-15T10:30:00"
    }
  ]
}
```

## 🤖 AI Model Selection

The script uses **Llama 2 70B Chat** via OpenRouter because:
- ✅ **Free tier available** (no cost for basic usage)
- ✅ **High performance** for financial analysis
- ✅ **Reliable JSON output** for structured data
- ✅ **Good understanding** of financial markets

## 📈 Sample Output

```
🚀 Starting Financial News Analysis...
📊 Query: 'stock market technology companies' | Max Articles: 3
🤖 Using AI Model: meta-llama/llama-2-70b-chat
--------------------------------------------------
✅ API keys validated successfully
📰 Fetching financial news for query: 'stock market technology companies'
✅ Fetched 3 articles
🤖 Analyzing article 1/3: Apple Reports Strong Q4 Earnings...
🤖 Analyzing article 2/3: Tech Stocks Rally on Fed Decision...
🤖 Analyzing article 3/3: Microsoft Cloud Revenue Surges...
✅ Analysis results saved to financial_news_analysis.json
--------------------------------------------------
✅ Analysis complete!
📈 Analyzed 3 articles

📋 Sample Analysis Results:
==================================================

Article 1:
Headline: Apple Reports Strong Q4 Earnings
Sentiment: POSITIVE
Affected Stocks: AAPL, GOOGL, MSFT
Impact: Apple's strong earnings could boost tech sector confidence
Confidence: HIGH
------------------------------
```

## 🔧 Configuration

### Environment Variables
- `NEWS_API_KEY`: Your NewsAPI key
- `OPENROUTER_API_KEY`: Your OpenRouter API key
- `OPENROUTER_MODEL`: AI model to use (default: meta-llama/llama-2-70b-chat)

### Customization Options
- **Query**: Change the news search query in `main()` function
- **Article Count**: Modify `max_articles` parameter
- **Output File**: Change filename in `save_analysis_results()`

## 🚨 Rate Limits & Costs

### NewsAPI (Free Tier)
- ✅ 100 requests per day
- ✅ No cost for basic usage
- ⚠️ Rate limiting enforced

### OpenRouter (Free Tier)
- ✅ Free credits available
- ✅ Llama 2 70B available for free
- ⚠️ Monitor usage in dashboard

## 🛠️ Troubleshooting

### Common Issues

1. **API Key Errors**
   ```
   ❌ NEWS_API_KEY not found in environment variables
   ```
   **Solution**: Check your `.env` file and ensure API keys are correct

2. **Rate Limit Reached**
   ```
   ⚠️ Daily NewsAPI limit reached (100 requests)
   ```
   **Solution**: Wait until tomorrow or upgrade to paid plan

3. **AI Analysis Failures**
   ```
   ❌ AI analysis failed: [error message]
   ```
   **Solution**: Check OpenRouter API key and account status

4. **No News Found**
   ```
   ❌ No news articles found. Exiting.
   ```
   **Solution**: Try different search queries or check internet connection

### Debug Mode
Add debug prints by modifying the script:
```python
# Add to any function for debugging
print(f"DEBUG: {variable_name}")
```

## 🔮 Future Enhancements

### Suggested Improvements
1. **Multiple News Sources**: Add Reuters, Bloomberg, Yahoo Finance
2. **Database Integration**: Store results in PostgreSQL/MongoDB
3. **Real-time Monitoring**: Set up scheduled analysis
4. **Advanced Analytics**: Historical sentiment tracking
5. **Web Interface**: Create a web dashboard
6. **Stock Price Integration**: Combine with real-time price data
7. **Alert System**: Notify on significant news events

### Technical Enhancements
- Add more AI models for comparison
- Implement sentiment confidence scoring
- Add stock sector classification
- Create API endpoints for web integration
- Add data visualization capabilities

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review API documentation
3. Open an issue on GitHub

---

**Note**: This tool is for educational and research purposes. Always verify AI-generated financial analysis with professional sources before making investment decisions. 