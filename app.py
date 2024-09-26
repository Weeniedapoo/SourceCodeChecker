from flask import Flask, request, jsonify, render_template
import openai

app = Flask(__name__)

openai.api_key = 'api key here'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_code():
    data = request.get_json()  
    code = data.get('code', '')  

    if not code:
        return jsonify({'error': '코드가 제공되지 않았습니다.'}), 400  

    try:

        sections = ["시큐어 코딩", "악성 코드", "비효율적인 코드", "코드 오류"]
        analysis_results = {}

        for section in sections:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "당신은 코드 분석기입니다."},
                    {"role": "user", "content": f"다음 코드를 {section} 기준으로 분석해주세요. 문제와 대응 방안을 제시해 주세요:\n\n{code}"}
                ]
            )
            analysis_content = response['choices'][0]['message']['content']

            problem = analysis_content.split("대응:")[0].strip()
            solution = analysis_content.split("대응:")[1].strip() if "대응:" in analysis_content else "대응책이 제공되지 않았습니다."


            analysis_results[section] = f"{problem}\n대응: {solution}"

        corrected_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 코드 분석기입니다."},
                {"role": "user", "content": f"다음 코드를 시큐어하게 수정하고 비효율성을 개선해 주세요:\n\n{code}"}
            ]
        )
        corrected_code = corrected_response['choices'][0]['message']['content']

        result = {
            "secureCode": analysis_results["시큐어 코딩"],
            "maliciousCode": analysis_results["악성 코드"],
            "inefficientCode": analysis_results["비효율적인 코드"],
            "codeErrors": analysis_results["코드 오류"],
            "correctedCode": corrected_code.strip()
        }
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
