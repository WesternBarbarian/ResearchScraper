"""Paper analyzer module that uses GPT-4o to identify relevant papers."""

import json
import os
from datetime import datetime
from typing import Dict, List

from openai import OpenAI

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai = OpenAI(api_key=OPENAI_API_KEY)

def analyze_paper(paper: Dict) -> Dict:
    """Analyze a single paper using GPT-4o."""
    prompt = f"""Analyze this research paper summary and determine its relevance for practical AI applications and thought leadership.
Focus on papers that:
1. Discuss practical applications of AI
2. Present insights valuable for thought leadership
3. Offer implementable methodologies or frameworks

Paper Title: {paper['title']}
Summary: {paper['summary']}

Respond with JSON in this format:
{{
    "is_relevant": boolean,
    "relevance_score": float (0-1),
    "practical_applications": string,
    "thought_leadership_value": string,
    "key_insights": list of strings
}}
"""
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        analysis = json.loads(response.choices[0].message.content)
        return {**paper, "analysis": analysis}
    except Exception as e:
        print(f"Error analyzing paper '{paper['title']}': {str(e)}")
        return None

def filter_papers(papers: List[Dict], min_relevance_score: float = 0.7) -> List[Dict]:
    """Filter papers based on relevance score."""
    return [
        paper for paper in papers 
        if paper and paper.get('analysis', {}).get('is_relevant', False) 
        and paper.get('analysis', {}).get('relevance_score', 0) >= min_relevance_score
    ]

def analyze_papers(input_file: str, output_file: str, min_relevance_score: float = 0.7) -> None:
    """Analyze papers from input JSON file and save relevant ones to output file."""
    try:
        with open(input_file, 'r') as f:
            data = json.load(f)
        
        analyzed_papers = []
        for paper in data['papers']:
            analyzed_paper = analyze_paper(paper)
            if analyzed_paper:
                analyzed_papers.append(analyzed_paper)
        
        filtered_papers = filter_papers(analyzed_papers, min_relevance_score)
        
        output_data = {
            "metadata": {
                "exported_at": datetime.now().isoformat(),
                "paper_count": len(filtered_papers),
                "min_relevance_score": min_relevance_score,
                "export_format_version": "1.0"
            },
            "papers": filtered_papers
        }
        
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)
            
        print(f"Analysis complete. Found {len(filtered_papers)} relevant papers out of {len(data['papers'])} total papers.")
        
    except Exception as e:
        print(f"Error processing papers: {str(e)}")
        raise
