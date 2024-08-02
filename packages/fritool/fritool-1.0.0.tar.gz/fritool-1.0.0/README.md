# frtool
Financial Resilience tool
## Example Usage

```python
from frtool.apiclient import ApiClient

apiclient = ApiClient(api_key="demokey")
questions = apiclient.collect_questions()
answers = apiclient.generate_mock_answers(questions)
scores = apiclient.calculate_score(answers)

if scores['index_score_result'] > 0:
    print(f"Your score is {scores['index_score']} which is {scores['index_score_result']}% higher than the average score {scores['index_score_value_to_compare']}")
else:
    print(f"Your score is {scores['index_score']} which is {abs(scores['index_score_result'])}% lower than the average score {scores['index_score_value_to_compare']}")
