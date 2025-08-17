from transformers import pipeline

def summarize_text(text):
    summarizer = pipeline("summarization")
    
    chunk_size = 1000  
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    
 
    summary = ""
    for chunk in chunks:
        part_summary = summarizer(chunk, max_length=150, min_length=40, do_sample=False)
        summary += part_summary[0]['summary_text'] + " "
    
    return summary.strip()

