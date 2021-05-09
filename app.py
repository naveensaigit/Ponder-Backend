from flask import Flask, request
from get_data import get_df
from question_generation.pipelines import pipeline
from sentence_transformers import SentenceTransformer, util

app = Flask(__name__)
nlp = pipeline("multitask-qa-qg")
model = SentenceTransformer("paraphrase-distilroberta-base-v1")

@app.route("/transformer/generate", methods=["POST"])
def generate_questions():
    text = request.get_json().get('text')
    print('----------TEXT-----------')
    print(text)
    return {"response": nlp(text)}

@app.route("/transformer/answer", methods=["POST"])
def answer_question():
    text = request.get_json().get('text')
    question = request.get_json().get('question')
    return nlp({"question": question, "context": text})

@app.route("/similarity", methods=["POST"])
def sentence_similarity():
    trueAns = request.get_json().get('trueAns')
    userAns = request.get_json().get('userAns')
    similarity = []
    for ta, ua in zip(trueAns, userAns):
        trueEmbeds = model.encode(ta, convert_to_tensor=True)
        userEmbeds = model.encode(ua, convert_to_tensor=True)
        similarity.append(util.pytorch_cos_sim(trueEmbeds, userEmbeds)[0][0].item())
    return {"similarity": similarity}

@app.route("/libgen/getBooks", methods=["POST"])
def get_books():
    topic_id = request.get_json().get("topic_id")
    page_num = request.get_json().get("page_num")

    url = f"http://libgen.rs/search.php?&req=topicid{topic_id}&phrase=0&view=simple&column=topic&sort=def&sortmode=ASC&page={page_num}"
    df = get_df(url)
    print("\n\n\n\n\n", df, "\n\n\n\n\n\n")
    try:
        res = df.to_json(orient="records")
        return res
    except AttributeError:
        return {"response": []}
    
if __name__ == '__main__':
   app.run(debug=True)