import openai
import anthropic
import google.generativeai as genai
from dotenv import load_dotenv
import os
import logging
import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import login
import torch
from pdme.generate_bootstrap_prompts import create_bootstrap_prompts
from pdme.evaluate import pdme_llm

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set logging level for external libraries to WARNING to suppress low-level logs
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("anthropic").setLevel(logging.WARNING)
logging.getLogger("google.generativeai").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)  # Suppress HTTP request logs if using requests library

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')

def generate_bootstrap_prompts(seeds, template, num):
    logging.info('Generating bootstrap prompts...')
    return create_bootstrap_prompts(template=template, seeds=seeds, num=num)

def generate_question_prompts(bootstrap_prompts, model_name, api_key):
    logging.info('Generating question prompts using model %s...', model_name)
    client = openai.OpenAI(api_key=api_key)
    question_prompts = []

    for item in bootstrap_prompts:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": item},
            ]
        )
        question_prompts.append(response.choices[0].message.content)
    
    return question_prompts

def generate_responses(model_name, question_prompts):
    logging.info('Generating responses using model %s...', model_name)
    responses = []

    if model_name.startswith("gpt"):
        client = openai.OpenAI(api_key=openai_api_key)
        for item in question_prompts:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": item},
                ]
            )
            responses.append(response.choices[0].message.content)

    elif model_name.startswith("claude"):
        anthropic_client = anthropic.Client(api_key=anthropic_api_key)
        for item in question_prompts:
            response = anthropic_client.messages.create(
                model=model_name,
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": item}
                ]
            )
            text_response = response.content[0].text
            responses.append(text_response)

    else:
        huggingface_api_key = os.getenv('HUGGINGFACE_API_KEY')
        if not huggingface_api_key:
              raise ValueError("HuggingFace API key not found in environment variables.")
        login(huggingface_api_key)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        for item in question_prompts:
            inputs = tokenizer.encode(item, return_tensors="pt")
            outputs = model.generate(inputs, max_length=100)
            response = tokenizer.decode(outputs[0], skip_special_tokens=True)
            responses.append(response)

    return responses

def score_responses(evaluation_prompt_template, question_prompts, responses_model_1, responses_model_2, client, eval_model):
    logging.info('Scoring responses...')
    llm = pdme_llm(client, eval_model)
    model_1_scores = []
    model_2_scores = []
    sum_model_1_scores = 0
    sum_model_2_scores = 0

    for i, question in enumerate(question_prompts):
        prompt_1 = evaluation_prompt_template.replace("<question_full>", question).replace("<response1>", responses_model_2[i]).replace("<response2>", responses_model_1[i])
        score_1 = llm.evaluate(prompt_1, ["1", "2"])

        prompt_2 = evaluation_prompt_template.replace("<question_full>", question).replace("<response1>", responses_model_1[i]).replace("<response2>", responses_model_2[i])
        score_2 = llm.evaluate(prompt_2, ["1", "2"])

        avg_score = [(score_1[j] + score_2[j]) / 2 for j in range(len(score_1))]

        model_1_scores.append(avg_score[1])
        model_2_scores.append(avg_score[0])
        sum_model_1_scores += avg_score[1]
        sum_model_2_scores += avg_score[0]

    winner = "Model 1" if sum_model_1_scores > sum_model_2_scores else "Model 2"

    scores_dict = {
        "Model 1 Scores": model_1_scores,
        "Model 2 Scores": model_2_scores,
        "Model 1 Total Scores": sum_model_1_scores,
        "Model 2 Total Scores": sum_model_2_scores,
        "Winner": winner
    }

    return scores_dict

def rank_models(results, models):
    logging.info('Ranking models...')
    scores = {model: 0 for model in models}

    for model1, model2, winner in results:
        if winner == "Model 1":
            scores[model1] += 1
        elif winner == "Model 2":
            scores[model2] += 1

    leaderboard = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    leaderboard_df = pd.DataFrame(leaderboard, columns=["Model Name", "Wins"])
    leaderboard_df["Rank"] = leaderboard_df["Wins"].rank(ascending=False, method='dense').astype(int)

    return leaderboard_df

def main(models):
    logging.info('Starting the main process with models %s...', models)

    seeds = { 
        "<language>": ["python", "c++"],
        "<seed>": ["tic-tac-toe", "array", "sorting", "dictionary"],
    }

    bootstrap_prompt_template = """Write a question asking to make a programming challenge meant to evaluate programming abilities.
    The problem should be possible to solve in less than 100 lines of code for a very skilled programmer.
    The problem should use the <language> language, and be realted to these seeds: <seed>, <seed>."""

    bootstrap_prompts = generate_bootstrap_prompts(seeds, bootstrap_prompt_template, num=3)

    for item in bootstrap_prompts:
        logging.info('Bootstrap prompt: %s', item)

    question_prompts = generate_question_prompts(bootstrap_prompts, model_name="gpt-3.5-turbo", api_key=openai_api_key)
    
    for item in question_prompts:
        logging.info('Question prompt: %s', item)

    results = []

    for i in range(len(models)):
        for j in range(i + 1, len(models)):
            model_1 = models[i]
            model_2 = models[j]
            
            logging.info('Running competition between %s and %s', model_1, model_2)

            try:
                responses_model_1 = generate_responses(model_1, question_prompts)
                responses_model_2 = generate_responses(model_2, question_prompts)

                eval_model = "gpt-3.5-turbo-instruct"
                client = openai.OpenAI(api_key=openai_api_key)

                evaluation_prompt_template = """<prefix><user_start>Here is a prompt:
                {
                    "instruction": \"""<question_full>\""",
                }

                Here are the outputs of the models:
                [
                    {
                        "model": 1,
                        "answer": \"""<response1>\"""
                    },
                    {
                        "model": 2,
                        "answer": \"""<response2>\"""
                    }
                ]

                Please create a dict containting the highest quality answer, i.e., produce the following output:

                {
                'best_model': <model-name>
                }

                Please provide the response that the majority of humans would consider better.

                <assistant_start>{
                'best_model': """

                scores = score_responses(evaluation_prompt_template, question_prompts, responses_model_1, responses_model_2, client, eval_model)
                
                logging.info('Scores: %s', scores)
                winner = scores["Winner"]
                results.append((model_1, model_2, winner))

                # Save partial results to CSV
                results_df = pd.DataFrame(results, columns=["Model 1", "Model 2", "Winner"])
                results_df.to_csv('pdme_competitions.csv', index=False)
                logging.info('Partial competition results saved to pdme_competitions.csv')

            except Exception as e:
                logging.error('An error occurred during the competition between %s and %s: %s', model_1, model_2, e)
                continue

    # Rank models and save leaderboard
    leaderboard_df = rank_models(results, models)
    logging.info('Leaderboard:\n%s', leaderboard_df)
    leaderboard_df.to_csv('pdme_leaderboard.csv', index=False)
    logging.info('Leaderboard saved to pdme_leaderboard.csv')

if __name__ == "__main__":
    model_list = ['claude-3-opus-20240229', 'claude-3-5-sonnet-20240620', 'gpt-4o', 'gpt-4-turbo', 'gpt-4', 'gemini-1.0-pro']
    main(model_list)
