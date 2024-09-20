from flask import Flask, request, jsonify, render_template
import openai

app = Flask(__name__)

# OpenAI API 키 설정
openai.api_key = 'Insert Your API Key Here!!!!!!!!!!!!!!!!!'

# 루트 경로에 대한 라우트 정의
@app.route('/')
def index():
    return render_template('index.html')

# /analyze 경로: API 요청을 처리하는 라우트
@app.route('/analyze', methods=['POST'])
def analyze_code():
    data = request.get_json()
    code = data.get('code', '')

    if not code:
        return jsonify({'error': 'No code provided'}), 400

    try:
        # OpenAI API의 새로운 방식으로 코드 분석 요청
        sections = ["시큐어 코딩 여부", "악성 코드 여부", "비효율적인 코드 여부", "코드 오류 여부"]
        analysis_results = {}

        for section in sections:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a code analyzer."},
                    {"role": "user", "content": f"다음 코드를 {section}에 대해 분석해줘. 문제를 자세히 설명하고 그에 대한 추천 대응법을 제시해줘:\n\n{code}"}
                ]
            )
            analysis_content = response['choices'][0]['message']['content']

            # 문제와 대응을 분리하여 구체적으로 처리
            problem = analysis_content.split("대응:")[0].strip()
            solution = analysis_content.split("대응:")[1].strip() if "대응:" in analysis_content else "대응책이 제시되지 않았습니다."

            # 결과 저장
            analysis_results[section] = f"{problem}\n대응: {solution}"

        # 수정된 코드 요청
        corrected_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a code analyzer."},
                {"role": "user", "content": f"다음 코드를 시큐어하게 수정하고 비효율성을 개선해줘:\n\n{code}"}
            ]
        )

        corrected_code = corrected_response['choices'][0]['message']['content']

        result = {
            "secureCode": analysis_results["시큐어 코딩 여부"],
            "maliciousCode": analysis_results["악성 코드 여부"],
            "inefficientCode": analysis_results["비효율적인 코드 여부"],
            "codeErrors": analysis_results["코드 오류 여부"],
            "correctedCode": corrected_code.strip()
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
