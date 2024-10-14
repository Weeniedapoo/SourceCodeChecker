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
            "시큐어 코딩": "이 코드가 시큐어코딩이 적용되었는지에 대해서만 분석하시오. 시큐어코딩의 예로는 버퍼 오버플로우, XSS 공격 방지 여부, 인증 및 권한 체크가 제대로 이루어졌는지, 안전한 데이터 전송을 위해 암호화가 되었는지, 에러 처리 시 민감한 정보가 노출되지 않도록 처리했는지가 있으며 취약점을 방지하기 위한 '방어적인 코딩' 관점에서 분석한다. 시큐어코딩에 대한 문제를 제외한 다른 문제에 대해서는 문제삼지마시오. 해당 사항에 대해서 문제가 있는 코드인지 한줄로 명확히 설명하고 각각 문제점을 번호매겨 간략하게 설명하시오. 대안에서 각 번호의 문제점에 대한 설명과 수정 방안을 제공하시오. 각 대안은 대안이 가리키는 문제의 번호와 동일하게하시오. 문제가 발견된다면 처음에 무조건 !!로 문장을 시작하시오.",
            "악성 코드": "이 코드에 악성 동작(예: 데이터 유출, 시스템 손상) 수행을 목적으로하는 코드가 있는지에서만 분석하시오. 악성동작의 예로는 민감한 정보를 외부로 전송하는 코드가 있는지, 권한 없이 파일 삭제 또는 시스템 변경을 시도하는 코드가 있는지, 원격 명령 실행, 루트 권한을 탈취하려는 시도가 있는지가 있으며 공격적인 동작이나 의도를 분석한다. 악성동작에 대한 문제를 제외한 다른 문제에 대해서는 문제삼지마시오.해당 사항에 대해서 문제가 있는 코드인지 한줄로 명확히 설명하고 각각 문제점을 번호매겨 간략하게 설명하시오. 대안에서는 각 번호의 문제점에 대한 설명과 수정 방안을 제공하시오. 각 대안은 대안이 가리키는 문제의 번호와 동일하게하시오. 문제가 발견된다면 처음에 무조건 !!로 문장을 시작하시오.",
            "비효율적인 코드": "이 코드가 코드의 길이나 성능 면에서 비효율적인 부분이 있는지, 성능개선이 가능한 코드인지에 대해서만 분석하시오. 호율적코딩의 초점은 불필요하게 길거나 중복된 코드를 제거할 수 있는지, 더 효율적인 알고리즘이나 데이터 구조로 대체할 수 있는지, 메모리 사용량과 CPU 처리 시간을 줄일 수 있는지에 대해 분석한다. 효율적코딩에 대한 문제를 제외한 다른 문제에 대해서는 문제삼지마시오. 해당 사항에 대해서 문제가 있는 코드인지 한줄로 명확히 설명하고 각각 문제점을 번호매겨 간략하게 설명하시오. 대안에서 각 번호의 문제점에 대한 설명과 수정 방안을 제공하시오. 각 대안은 대안이 가리키는 문제의 번호와 동일하게하시오. 문제가 발견된다면 처음에 무조건 !!로 문장을 시작하시오.",
            "코드 오류": "이 코드에 컴파일오류가 발생하는지 여부만을 분석하시오. 코드가 컴파일되고 실행 가능하면 그 외의 문제는 분석에서 제외하시오. 해당 사항에 대해서 문제가 있는 코드인지 한줄로 명확히 설명하고 각각 문제점을 번호매겨 간략하게 설명하시오. 대안에서 각 번호의 문제점에 대한 설명과 수정 방안을 제공하시오. 각 대안은 대안이 가리키는 문제의 번호와 동일하게하시오. 문제가 발견된다면 처음에 무조건 !!로 문장을 시작하시오."
        }

        analysis_results = {}

        for section, description in sections.items():
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "당신은 전문가 수준의 코드 분석기입니다.  요청된 조건에 맞추어 코드 분석을 정확하게 수행하고, 조건에 맞지 않는 내용은 절대 지적하거나 언급하지 마십시오. 대안은 4줄을 띄고 설명하시오."},
                    {"role": "user", "content": f"{description}\n다음 코드를 분석해 주세요:\n\n{code}"}
                ],
                temperature=0.1
            )
            analysis_content = response['choices'][0]['message']['content']

            problem = ""
            solution = ""

            if "!!" in analysis_content and "대안:" in analysis_content:
                problem = analysis_content.split("!!")[1].split("대안:")[0].strip()
                solution = analysis_content.split("대안:")[1].strip()
            else:
                problem = "문제가 발견되지 않았습니다."
                solution = "대안이 제공되지 않았습니다."

            if "정상적인 코드" in analysis_content:
                problem = "문제가 없는 정상적인 코드입니다."
                solution = "대안이 제공되지 않았습니다."

            analysis_results[section] = f"**문제:** {problem}\n\n\n\n\n\n**대안:** {solution}"
            
        corrected_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 전문가 수준의 코드 분석기입니다."},
                {"role": "user", "content": f"다음 코드를 시큐어하게 수정하고, 비효율성을 개선하며 모든 오류를 해결해 주세요. 수정된 코드만 반환하세요:\n\n{code}"}
            ],
            temperature=0.1  
        )
        corrected_code = corrected_response['choices'][0]['message']['content'].strip()

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
