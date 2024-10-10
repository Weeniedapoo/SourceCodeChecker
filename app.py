from flask import Flask, request, jsonify, render_template
import openai

app = Flask(__name__)

openai.api_key = ''

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
        # 분석할 항목들
        sections = {
            "시큐어 코딩": "이 코드가 시큐어코딩이 적용되었는지에 대해서만 분석하시오. 시큐어코딩에 대한 문제를 제외한 다른 문제에 대해서는 문제삼지마시오. 해당 사항에 대해서 문제가 있는 코드인지 한줄로 명확히 설명하고 각각 문제점을 번호매겨 간략하게 설명하시오. 대안에서 각 번호의 문제점에 대한 설명과 수정 방안을 제공하시오. 각 대안은 대안이 가리키는 문제의 번호와 동일하게하시오. 문제가 발견된다면 처음에 무조건 !!로 문장을 시작하시오.",
            "악성 코드": "이 코드가 악성 동작(예: 데이터 유출, 시스템 손상)을 수행할 수 있는지, 개인정보 유출 가능성이 있는지에 대해서만 분석하시오. 악성동작에 대한 문제를 제외한 다른 문제에 대해서는 문제삼지마시오.해당 사항에 대해서 문제가 있는 코드인지 한줄로 명확히 설명하고 각각 문제점을 번호매겨 간략하게 설명하시오. 대안에서는 각 번호의 문제점에 대한 설명과 수정 방안을 제공하시오. 각 대안은 대안이 가리키는 문제의 번호와 동일하게하시오. 문제가 발견된다면 처음에 무조건 !!로 문장을 시작하시오.",
            "비효율적인 코드": "이 코드가 성능 면에서 비효율적인 부분이 있는지, 더 효율적으로 수정이가능한지에 대해서만 분석하시오. 효율적코딩에 대한 문제를 제외한 다른 문제에 대해서는 문제삼지마시오. 해당 사항에 대해서 문제가 있는 코드인지 한줄로 명확히 설명하고 각각 문제점을 번호매겨 간략하게 설명하시오. 대안에서 각 번호의 문제점에 대한 설명과 수정 방안을 제공하시오. 각 대안은 대안이 가리키는 문제의 번호와 동일하게하시오. 문제가 발견된다면 처음에 무조건 !!로 문장을 시작하시오.",
            "코드 오류": "이 코드에 구문 오류 또는 논리적 오류가 있는지에 대해서만 분석하시오. 코드 문법오류에 대한 문제를 제외한 다른 문제에 대해서는 문제삼지마시오. 해당 사항에 대해서 문제가 있는 코드인지 한줄로 명확히 설명하고 각각 문제점을 번호매겨 간략하게 설명하시오. 대안에서 각 번호의 문제점에 대한 설명과 수정 방안을 제공하시오. 각 대안은 대안이 가리키는 문제의 번호와 동일하게하시오. 문제가 발견된다면 처음에 무조건 !!로 문장을 시작하시오."
        }

        analysis_results = {}

        for section, description in sections.items():
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "당신은 전문가 수준의 코드 분석기입니다. 각 코드 분석 항목에 대한 문제점을 명확히 식별하고 해당 문제점에 대한 대안을 제공하시오. 대안은 4줄을 띄고 설명하시오."},
                    {"role": "user", "content": f"{description}\n다음 코드를 분석해 주세요:\n\n{code}"}
                ]
            )
            analysis_content = response['choices'][0]['message']['content']

            # 문제와 대안을 추출하는 로직
            problem = ""
            solution = ""

            if "!!" in analysis_content and "대안:" in analysis_content:
                problem = analysis_content.split("!!")[1].split("대안:")[0].strip()
                solution = analysis_content.split("대안:")[1].strip()
            else:
                problem = "문제가 발견되지 않았습니다."
                solution = "대안이 제공되지 않았습니다."

            # 문제가 없으면 "정상적인 코드" 메시지 출력
            if "정상적인 코드" in analysis_content:
                problem = "문제가 없는 정상적인 코드입니다."
                solution = "대안이 제공되지 않았습니다."

            # 결과 저장
            analysis_results[section] = f"**문제:** {problem}\n\n\n\n\n\n**대안:** {solution}"
            

        # 모든 문제를 해결한 수정된 코드 생성
        corrected_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 전문가 수준의 코드 분석기입니다."},
                {"role": "user", "content": f"다음 코드를 시큐어하게 수정하고, 비효율성을 개선하며 모든 오류를 해결해 주세요. 수정된 코드만 반환하세요:\n\n{code}"}
            ]
        )
        corrected_code = corrected_response['choices'][0]['message']['content'].strip()

        # 분석 결과 반환
        result = {
            "secureCode": analysis_results["시큐어 코딩"],
            "maliciousCode": analysis_results["악성 코드"],
            "inefficientCode": analysis_results["비효율적인 코드"],
            "codeErrors": analysis_results["코드 오류"],
            "correctedCode": corrected_code
        }
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
