import spacy
from nltk.corpus import wordnet
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer

# Download NLTK resources if not already present
import nltk
# nltk.download('punkt')
# nltk.download('wordnet')

def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return list(synonyms)

def lemmatize(text):
    lemmatizer = WordNetLemmatizer()
    lemmas = [lemmatizer.lemmatize(token) for token in word_tokenize(text)]
    return ' '.join(lemmas)

def extract_action_and_target(sentence):
    # Load the spaCy language model
    nlp = spacy.load("en_core_web_sm")

    # Process the sentence with spaCy
    doc = nlp(sentence)

    # Define keywords for actions
    action_keywords = {
        'click': ['click', 'select', 'press', 'press on', 'mouse click']
    }

 #   if action == 'select':
 #       action = 'click'
    
    # Initialize action and target
    action = None
    target = None

    # Convert the sentence to lowercase for case-insensitive matching
    sentence_lower = sentence.lower()

    # Check for each action keyword, including synonyms
    for key, keywords in action_keywords.items():
        for kw in keywords:
            # Get synonyms for the keyword using WordNet
            synonyms = set(get_synonyms(kw))
            synonyms.add(kw)
            # print (synonyms)
            # print (kw)
            # Lemmatize the sentence and check for synonyms
            lemmatized_sentence = lemmatize(sentence_lower)
            if any(synonym in lemmatized_sentence for synonym in synonyms):
                action = key
                break

    # Extract target for click action using spaCy's part-of-speech tagging
    if action == 'click':
        # Identify the verb 'click' in the sentence
        click_token = next((token for token in doc if token.text.lower() in action_keywords['click']), None)

        # Identify the next noun or pronoun after the 'click' verb
        if click_token:
            # Get the document tokens starting from the token after the 'click' verb
            tokens_after_click = click_token.doc[click_token.i + 1:]
            # Filter tokens based on part-of-speech tags (NOUN, PROPN, PRON)
            filtered_tokens = [token for token in tokens_after_click if token.pos_ in ['NOUN', 'PROPN', 'PRON']]
            # Use the first token that meets the criteria as the target candidate
            target_candidate = next((token for token in filtered_tokens), None)

            if target_candidate:
                target = target_candidate.text

    return action, target

# Example usage
sentence1 = "Could you umm maybe select on sign up please?"
sentence2 = "Hey please can you click the home button?."
sentence3 = "Click on um search please."

action1, target1 = extract_action_and_target(sentence1)
action2, target2 = extract_action_and_target(sentence2)
action3, target3 = extract_action_and_target(sentence3)

print(f"Action 1: {action1}, Target 1: {target1}")
print(f"Action 2: {action2}, Target 2: {target2}")
print(f"Action 3: {action3}, Target 3: {target3}")

# print(type(action1))
# print(type(action2))
# print(type(action3))
