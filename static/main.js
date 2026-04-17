document.addEventListener("DOMContentLoaded", function () {
    const jdTextarea = document.getElementById("job_description");
    const warningEl = document.getElementById("jd-warning");
    const form = document.querySelector("form");
    const resumeInput = document.getElementById("resume");
    const uploadFilename = document.getElementById("upload-filename");

    function countWords(text) {
        return text.trim().split(/\s+/).filter(Boolean).length;
    }

    function showWarning() {
        warningEl.classList.add("visible");
    }

    function hideWarning() {
        warningEl.classList.remove("visible");
    }

    function validateJDInput(event) {
        if (!jdTextarea) {
            return;
        }
        const wordCount = countWords(jdTextarea.value);
        if (wordCount < 10) {
            event.preventDefault();
            showWarning();
            jdTextarea.focus();
        } else {
            hideWarning();
        }
    }

    if (jdTextarea) {
        jdTextarea.addEventListener("input", function () {
            if (countWords(jdTextarea.value) >= 10) {
                hideWarning();
            }
        });
    }

    if (resumeInput) {
        resumeInput.addEventListener("change", function () {
            if (resumeInput.files && resumeInput.files.length > 0) {
                uploadFilename.textContent = resumeInput.files[0].name;
            } else {
                uploadFilename.textContent = "No file selected";
            }
        });
    }

    if (form) {
        form.addEventListener("submit", validateJDInput);
    }
});
