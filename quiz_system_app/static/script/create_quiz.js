let questionCount = 0;

function addQuestion() {
    questionCount++;
    const container = document.getElementById("questions-container");
    const div = document.createElement("div");
    div.classList.add("mb-4", "border", "p-3", "rounded");
    div.setAttribute("id", `question${questionCount}`);

    div.innerHTML = `
        <label class="form-label fw-bold">Question ${questionCount}</label>
        <textarea name="q${questionCount}_text" class="form-control mb-2" placeholder="Enter question text" required></textarea>

        <label>Type</label>
        <select name="q${questionCount}_type" class="form-select mb-2" onchange="toggleOptions(this, ${questionCount})">
            <option value="mcq">MCQ</option>
            <option value="tf">True/False</option>
        </select>

        <div id="q${questionCount}_options_container" style="display:block;">
            <!-- MCQ Options -->
            <div id="q${questionCount}_mcq" class="mt-2">
                ${[1,2,3,4].map(i => `
                    <div class="mb-1">
                        <input type="radio" name="q${questionCount}_correct" value="${i}" required>
                        <input type="text" name="q${questionCount}_option${i}" class="form-control d-inline w-75" placeholder="Option ${i}" required>
                    </div>
                `).join('')}
            </div>

            <!-- True/False Options -->
            <div id="q${questionCount}_tf" class="mt-2" style="display:none;">
                <div class="mb-1">
                    <input type="radio" name="q${questionCount}_correct" value="True" required> True
                </div>
                <div class="mb-1">
                    <input type="radio" name="q${questionCount}_correct" value="False"> False
                </div>
            </div>
        </div>

        <button type="button" class="btn btn-danger btn-sm mt-2" onclick="removeQuestion(${questionCount})">Remove Question</button>
    `;

    container.appendChild(div);
}

function toggleOptions(select, qNum) {
    const mcqDiv = document.getElementById(`q${qNum}_mcq`);
    const tfDiv = document.getElementById(`q${qNum}_tf`);

    if (select.value === "mcq") {
        mcqDiv.style.display = "block";
        tfDiv.style.display = "none";
        mcqDiv.querySelectorAll("input[type='text'], input[type='radio']").forEach(inp => inp.required = true);
        tfDiv.querySelectorAll("input").forEach(inp => inp.required = false);
    } else if (select.value === "tf") {
        mcqDiv.style.display = "none";
        tfDiv.style.display = "block";
        mcqDiv.querySelectorAll("input").forEach(inp => inp.required = false);
        tfDiv.querySelectorAll("input").forEach(inp => inp.required = true);
    }
}
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('input[type="text"][name^="q"]').forEach(input => {
        input.addEventListener('input', () => {
            const radio = input.parentElement.querySelector('input[type="radio"]');
            if(radio) {
                radio.value = input.value;
            }
        });
    });
});
function removeQuestion(qNum) {
    const div = document.getElementById(`question${qNum}`);
    if (div) div.remove();
}

// AJAX 
document.getElementById("quizForm").addEventListener("submit", function(e) {
    e.preventDefault(); 
    const formData = new FormData(this);

    fetch(createQuizURL, {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": formData.get("csrfmiddlewaretoken")
        }
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            alert("Quiz created successfully!");
            window.location.href = homeURL;
        } else {
            alert("Error: " + JSON.stringify(data.errors));
        }
    })
    .catch(err => console.error(err));
});
