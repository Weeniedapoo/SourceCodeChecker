<<<<<<< HEAD
document.addEventListener("DOMContentLoaded", function() {
    const codeInput = document.getElementById('codeInput');
    const scannedCode = document.getElementById('scannedCode');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const dropArea = document.getElementById('drop-area');

    // 1. Paste event와 input event를 통해 실시간으로 Scanned Code에 반영
    codeInput.addEventListener('input', function() {
        scannedCode.innerText = codeInput.value;
    });

    // 2. Drag & Drop 기능
    dropArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        dropArea.classList.add('dragover');
    });

    dropArea.addEventListener('dragleave', function() {
        dropArea.classList.remove('dragover');
    });

    dropArea.addEventListener('drop', function(e) {
        e.preventDefault();
        dropArea.classList.remove('dragover');
        const file = e.dataTransfer.files[0];
        const reader = new FileReader();

        reader.onload = function(event) {
            codeInput.value = event.target.result;
            scannedCode.innerText = event.target.result; // 파일 내용을 바로 Scanned Code에 반영
        };

        if (file) {
            reader.readAsText(file);
        }
    });

    // 3. Analyze 버튼 클릭 시 OpenAI API 호출
    analyzeBtn.addEventListener('click', function() {
        const code = codeInput.value;

        fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code: code })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error: ' + data.error);
            } else {
                document.getElementById('secureCode').innerText = data.secureCode || 'No secure code found.';
                document.getElementById('maliciousCode').innerText = data.maliciousCode || 'No malicious code found.';
                document.getElementById('inefficientCode').innerText = data.inefficientCode || 'No inefficient code found.';
                document.getElementById('codeErrors').innerText = data.codeErrors || 'No errors found.';
                document.getElementById('correctedCode').innerText = data.correctedCode || 'No corrections made.';
            }
        })
        .catch(error => console.error('Error:', error));
    });
});
=======
document.addEventListener("DOMContentLoaded", function() {
    const codeInput = document.getElementById('codeInput');
    const scannedCode = document.getElementById('scannedCode');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const dropArea = document.getElementById('drop-area');

    // 1. Paste event와 input event를 통해 실시간으로 Scanned Code에 반영
    codeInput.addEventListener('input', function() {
        scannedCode.innerText = codeInput.value;
    });

    // 2. Drag & Drop 기능
    dropArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        dropArea.classList.add('dragover');
    });

    dropArea.addEventListener('dragleave', function() {
        dropArea.classList.remove('dragover');
    });

    dropArea.addEventListener('drop', function(e) {
        e.preventDefault();
        dropArea.classList.remove('dragover');
        const file = e.dataTransfer.files[0];
        const reader = new FileReader();

        reader.onload = function(event) {
            codeInput.value = event.target.result;
            scannedCode.innerText = event.target.result; // 파일 내용을 바로 Scanned Code에 반영
        };

        if (file) {
            reader.readAsText(file);
        }
    });

    // 3. Analyze 버튼 클릭 시 OpenAI API 호출
    analyzeBtn.addEventListener('click', function() {
        const code = codeInput.value;

        fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code: code })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error: ' + data.error);
            } else {
                document.getElementById('secureCode').innerText = data.secureCode || 'No secure code found.';
                document.getElementById('maliciousCode').innerText = data.maliciousCode || 'No malicious code found.';
                document.getElementById('inefficientCode').innerText = data.inefficientCode || 'No inefficient code found.';
                document.getElementById('codeErrors').innerText = data.codeErrors || 'No errors found.';
                document.getElementById('correctedCode').innerText = data.correctedCode || 'No corrections made.';
            }
        })
        .catch(error => console.error('Error:', error));
    });
});
>>>>>>> master
