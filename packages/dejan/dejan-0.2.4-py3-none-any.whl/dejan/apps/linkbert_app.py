from dejan import linkbert

def run_linkbert(text, group):
    """CLI tool for LinkBERT Token Prediction"""
    # Initialize the LinkBERTInference model
    model = linkbert.LinkBERTInference()

    # Perform prediction based on selected grouping strategy
    links = model.predict_link_tokens(text, group=group)

    # Display the results in the CLI
    print(f"\nPredicted link tokens ({group}):")
    for link in links:
        print(link)
