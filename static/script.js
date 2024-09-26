document.addEventListener("DOMContentLoaded", function() {
    const codeInput = document.getElementById('codeInput');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('fileInput');
    const loadingBar = document.getElementById('loadingBar'); 
    const progressBar = document.getElementById('progress');

    let loadingInterval;

    codeInput.addEventListener('input', function() {
        document.getElementById('scanned_Code').innerText = codeInput.value;
    });

    dropArea.addEventListener('click', function() {
        fileInput.click();
    });

    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            handleFile(file);
        }
    });

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
        if (file) {
            handleFile(file);
        }
    });

    function handleFile(file) {
        const reader = new FileReader();
        if (file.type === "text/plain" || file.name.endsWith(".c") || file.name.endsWith(".cpp") || file.name.endsWith(".py") || file.name.endsWith(".js")) {
            reader.onload = function(event) {
                codeInput.value = event.target.result;
                document.getElementById('scanned_Code').innerText = event.target.result;
            };
            reader.readAsText(file);
        } else {
            alert("Only text or code files are allowed.");
        }
    }

    analyzeBtn.addEventListener('click', function() {
        const code = codeInput.value;

        progressBar.style.width = '0%';
        loadingBar.style.display = 'block';

        let progress = 0;
        loadingInterval = setInterval(() => {
            if (progress < 90) {
                progress += 1;
                progressBar.style.width = progress + '%';
            }
        }, 300);

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
                document.getElementById('secureCodeText').innerText = data.secureCode || 'No secure code found.';
                document.getElementById('maliciousCodeText').innerText = data.maliciousCode || 'No malicious code found.';
                document.getElementById('inefficientCodeText').innerText = data.inefficientCode || 'No inefficient code found.';
                document.getElementById('codeErrorsText').innerText = data.codeErrors || 'No errors found.';
                document.getElementById('correctedCode').innerText = data.correctedCode || 'No corrections made.';
                progressBar.style.width = '100%';
            }
        })
        .catch(error => console.error('Error:', error))
        .finally(() => {

            clearInterval(loadingInterval); 
            setTimeout(() => {
                loadingBar.style.display = 'none'; 
            }, 530);
        }); 
    });

    window.handleButtonClick = function(buttonText) {

        document.getElementById('subheadingText').innerText = 'Analysed Results For: "' + buttonText + '"';

        document.querySelectorAll('.toggle-box').forEach(box => {
            box.style.display = 'none';
        });

        switch(buttonText) {
            case 'Secure Code':
                document.getElementById('secureCodeBox').style.display = 'block';
                break;
            case 'Malicious Code':
                document.getElementById('maliciousCodeBox').style.display = 'block';
                break;
            case 'Inefficient Code':
                document.getElementById('inefficientCodeBox').style.display = 'block';
                break;
            case 'Code Errors':
                document.getElementById('codeErrorsBox').style.display = 'block';
                break;
        }
    };

    window.onload = function() {
        document.querySelectorAll('.toggle-box').forEach(box => {
            box.style.display = 'none';
        });
    };
});
