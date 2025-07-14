#!/usr/bin/env python3
"""
Financial News Analyzer for Investapp

This script fetches financial news from NewsAPI, analyzes sentiment and stock impacts
using OpenRouter's free AI models, and stores results in JSON format.

Features:
- Fetches financial news from NewsAPI (free tier: 100 requests/day)
- Analyzes sentiment (positive, negative, neutral) using OpenRouter AI
- Identifies affected stocks and their potential impact
- Stores results in structured JSON format
- Handles API rate limits and errors gracefully

Author: Investapp Team
Date: 2024
"""

import os
import json
import requests
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

class FinancialNewsAnalyzer:
    """
    Main class for analyzing financial news and determining stock impacts.
    """
    
    def __init__(self):
        """Initialize the analyzer with API configurations."""
        # API Keys from environment variables
        self.news_api_key = os.getenv('NEWS_API_KEY')
        self.openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
        
        # OpenRouter configuration - Using Llama 2 70B as it's free and powerful
        self.openrouter_model = os.getenv('OPENROUTER_MODEL', 'meta-llama/llama-2-70b-chat')
        
        # API endpoints
        self.news_api_url = "https://newsapi.org/v2/everything"
        self.openrouter_url = "https://openrouter.ai/api/v1/chat/completions"
        
        # Rate limiting and request tracking
        self.news_requests_today = 0
        self.max_news_requests = 100  # NewsAPI free tier limit
        self.last_request_time = 0
        self.min_request_interval = 1  # Minimum seconds between requests
        
        # Validate API keys
        self._validate_api_keys()
        
        # Initialize OpenAI client for OpenRouter
        self.openai_client = openai.OpenAI(
            api_key=self.openrouter_api_key,
            base_url="https://openrouter.ai/api/v1"
        )
    
    def _validate_api_keys(self) -> None:
        """Validate that required API keys are present."""
        if not self.news_api_key:
            raise ValueError("NEWS_API_KEY not found in environment variables")
        if not self.openrouter_api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")
        print("✅ API keys validated successfully")
    
    def _check_rate_limits(self) -> bool:
        """Check if we can make another request without hitting rate limits."""
        current_time = time.time()
        
        # Check if enough time has passed since last request
        if current_time - self.last_request_time < self.min_request_interval:
            time.sleep(self.min_request_interval)
        
        # Check NewsAPI daily limit
        if self.news_requests_today >= self.max_news_requests:
            print("⚠️  Daily NewsAPI limit reached (100 requests)")
            return False
        
        return True
    
    def fetch_financial_news(self, query: str = "finance investment stock market", 
                           max_articles: int = 10) -> List[Dict]:
        """
        Fetch financial news from NewsAPI.
        
        Args:
            query: Search query for financial news
            max_articles: Maximum number of articles to fetch
            
        Returns:
            List of news articles with title, description, and content
        """
        if not self._check_rate_limits():
            return []
        
        try:
            # Calculate date range (last 7 days for fresh news)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)
            
            params = {
                'q': query,
                'apiKey': self.news_api_key,
                'language': 'en',
                'sortBy': 'publishedAt',
                'pageSize': max_articles,
                'from': start_date.strftime('%Y-%m-%d'),
                'to': end_date.strftime('%Y-%m-%d')
            }
            
            print(f"📰 Fetching financial news for query: '{query}'")
            response = requests.get(self.news_api_url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                
                # Update request tracking
                self.news_requests_today += 1
                self.last_request_time = time.time()
                
                print(f"✅ Fetched {len(articles)} articles")
                
                # Extract relevant information from articles
                processed_articles = []
                for article in articles:
                    processed_article = {
                        'title': article.get('title', ''),
                        'description': article.get('description', ''),
                        'content': article.get('content', ''),
                        'url': article.get('url', ''),
                        'publishedAt': article.get('publishedAt', ''),
                        'source': article.get('source', {}).get('name', '')
                    }
                    processed_articles.append(processed_article)
                
                return processed_articles
            else:
                print(f"❌ NewsAPI request failed: {response.status_code}")
                return []
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching news: {e}")
            return []
    
    def analyze_news_sentiment_and_impact(self, news_articles: List[Dict]) -> List[Dict]:
        """
        Analyze news articles for sentiment and stock impact using OpenRouter AI.
        
        Args:
            news_articles: List of news articles to analyze
            
        Returns:
            List of analyzed articles with sentiment and stock impact
        """
        analyzed_articles = []
        
        for i, article in enumerate(news_articles, 1):
            print(f"🤖 Analyzing article {i}/{len(news_articles)}: {article['title'][:50]}...")
            
            try:
                # Prepare the analysis prompt
                analysis_prompt = self._create_analysis_prompt(article)
                
                # Get AI analysis
                analysis_result = self._get_ai_analysis(analysis_prompt)
                
                # Parse the AI response
                parsed_analysis = self._parse_ai_response(analysis_result)
                
                # Combine original article with analysis
                analyzed_article = {
                    'headline': article['title'],
                    'description': article['description'],
                    'url': article['url'],
                    'publishedAt': article['publishedAt'],
                    'source': article['source'],
                    'sentiment': parsed_analysis.get('sentiment', 'neutral'),
                    'affected_stocks': parsed_analysis.get('affected_stocks', []),
                    'impact_description': parsed_analysis.get('impact_description', ''),
                    'confidence': parsed_analysis.get('confidence', 'medium'),
                    'analysis_timestamp': datetime.now().isoformat()
                }
                
                analyzed_articles.append(analyzed_article)
                
                # Rate limiting between AI requests
                time.sleep(2)
                
            except Exception as e:
                print(f"❌ Error analyzing article {i}: {e}")
                # Add article with default neutral analysis
                analyzed_article = {
                    'headline': article['title'],
                    'description': article['description'],
                    'url': article['url'],
                    'publishedAt': article['publishedAt'],
                    'source': article['source'],
                    'sentiment': 'neutral',
                    'affected_stocks': [],
                    'impact_description': 'Analysis failed',
                    'confidence': 'low',
                    'analysis_timestamp': datetime.now().isoformat()
                }
                analyzed_articles.append(analyzed_article)
        
        return analyzed_articles
    
    def _create_analysis_prompt(self, article: Dict) -> str:
        """Create a detailed prompt for AI analysis."""
        prompt = f"""
You are a financial analyst specializing in news sentiment analysis and stock market impact assessment.

Please analyze the following financial news article and provide a structured response in JSON format:

HEADLINE: {article['title']}
DESCRIPTION: {article['description']}
CONTENT: {article['content'][:500]}...

Analyze this news for:
1. SENTIMENT: Determine if the news is positive, negative, or neutral for the financial markets
2. AFFECTED STOCKS: Identify specific stocks, companies, or sectors that might be affected
3. IMPACT: Describe the potential impact on stock prices (increase, decrease, volatility, etc.)

Respond in this exact JSON format:
{{
    "sentiment": "positive|negative|neutral",
    "affected_stocks": ["AAPL", "GOOGL", "TSLA"],
    "impact_description": "Detailed description of expected impact",
    "confidence": "high|medium|low"
}}

Guidelines:
- Be specific about stock tickers when possible
- Consider both direct and indirect impacts
- Assess market sentiment realistically
- Focus on actionable insights for investors
"""
        return prompt
    
    def _get_ai_analysis(self, prompt: str) -> str:
        """Get analysis from OpenRouter AI model."""
        try:
            response = self.openai_client.chat.completions.create(
                model=self.openrouter_model,
                messages=[
                    {"role": "system", "content": "You are a financial analyst expert. Provide accurate, well-reasoned analysis in JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,  # Lower temperature for more consistent analysis
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"❌ AI analysis failed: {e}")
            return ""
    
    def _parse_ai_response(self, ai_response: str) -> Dict:
        """Parse the AI response and extract structured data."""
        try:
            # Try to extract JSON from the response
            if '{' in ai_response and '}' in ai_response:
                start = ai_response.find('{')
                end = ai_response.rfind('}') + 1
                json_str = ai_response[start:end]
                
                parsed = json.loads(json_str)
                
                # Validate and clean the parsed data
                return {
                    'sentiment': parsed.get('sentiment', 'neutral').lower(),
                    'affected_stocks': parsed.get('affected_stocks', []),
                    'impact_description': parsed.get('impact_description', ''),
                    'confidence': parsed.get('confidence', 'medium').lower()
                }
            else:
                raise ValueError("No JSON found in AI response")
                
        except Exception as e:
            print(f"❌ Failed to parse AI response: {e}")
            return {
                'sentiment': 'neutral',
                'affected_stocks': [],
                'impact_description': 'Analysis parsing failed',
                'confidence': 'low'
            }
    
    def save_analysis_results(self, analyzed_articles: List[Dict], 
                            filename: str = "financial_news_analysis.json") -> None:
        """
        Save analysis results to a JSON file.
        
        Args:
            analyzed_articles: List of analyzed articles
            filename: Output filename
        """
        output_data = {
            'analysis_metadata': {
                'total_articles': len(analyzed_articles),
                'analysis_date': datetime.now().isoformat(),
                'news_api_requests_used': self.news_requests_today,
                'model_used': self.openrouter_model
            },
            'articles': analyzed_articles
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Analysis results saved to {filename}")
            
        except Exception as e:
            print(f"❌ Error saving results: {e}")
    
    def run_analysis(self, query: str = "finance investment", 
                    max_articles: int = 5) -> List[Dict]:
        """
        Run the complete news analysis pipeline.
        
        Args:
            query: News search query
            max_articles: Maximum articles to analyze
            
        Returns:
            List of analyzed articles
        """
        print("🚀 Starting Financial News Analysis...")
        print(f"📊 Query: '{query}' | Max Articles: {max_articles}")
        print(f"🤖 Using AI Model: {self.openrouter_model}")
        print("-" * 50)
        
        # Step 1: Fetch news
        news_articles = self.fetch_financial_news(query, max_articles)
        
        if not news_articles:
            print("❌ No news articles found. Exiting.")
            return []
        
        # Step 2: Analyze sentiment and impact
        analyzed_articles = self.analyze_news_sentiment_and_impact(news_articles)
        
        # Step 3: Save results
        self.save_analysis_results(analyzed_articles)
        
        print("-" * 50)
        print("✅ Analysis complete!")
        print(f"📈 Analyzed {len(analyzed_articles)} articles")
        
        return analyzed_articles


def main():
    """Main function to run the financial news analyzer."""
    try:
        # Initialize the analyzer
        analyzer = FinancialNewsAnalyzer()
        
        # Run analysis with sample query
        results = analyzer.run_analysis(
            query="stock market technology companies",
            max_articles=3  # Start with small number for testing
        )
        
        # Display sample results
        if results:
            print("\n📋 Sample Analysis Results:")
            print("=" * 50)
            
            for i, article in enumerate(results[:2], 1):  # Show first 2 results
                print(f"\nArticle {i}:")
                print(f"Headline: {article['headline']}")
                print(f"Sentiment: {article['sentiment'].upper()}")
                print(f"Affected Stocks: {', '.join(article['affected_stocks']) if article['affected_stocks'] else 'None identified'}")
                print(f"Impact: {article['impact_description']}")
                print(f"Confidence: {article['confidence'].upper()}")
                print("-" * 30)
        
    except Exception as e:
        print(f"❌ Application error: {e}")
        print("\n💡 Troubleshooting tips:")
        print("1. Check your API keys in .env file")
        print("2. Ensure you have internet connection")
        print("3. Verify NewsAPI and OpenRouter accounts are active")


if __name__ == "__main__":
    main() 