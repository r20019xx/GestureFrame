/// function to go from lightmode to dark mode and vice versa
function toggleDarkMode() {
    // Toggle the dark mode class on both the html and body elements
    document.documentElement.classList.toggle("dark-mode");
    document.body.classList.toggle("dark-mode");

    // Save the user's preference to localStorage so that darkmode persists if changing to diff webpage
    if (document.body.classList.contains("dark-mode")) {
        localStorage.setItem("theme", "dark");
    } else {
        localStorage.setItem("theme", "light");
    }
}

// changes
function toggleDarkModeAndUpdateText(event) {
    event.preventDefault();         // prevents defaulting to light mode
    toggleDarkMode();               // change from light to dark mode
    updateThemeToggleLinkText();    // update text in the settings dropdown
}

// changes text in the dropdown based on the mode that website is currently in
function updateThemeToggleLinkText() {
    var link = document.getElementById("theme-toggle-link");
    if (document.body.classList.contains("dark-mode")) {
        link.textContent = "Change to Light Mode";
    } else {
        link.textContent = "Change to Dark Mode";
    }
}

// DOM = Document object Model
document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript loaded");

    addComment();

    // Apply stored theme preference if it exists
    const storedTheme = localStorage.getItem("theme");
    if (storedTheme === "dark") {
        document.documentElement.classList.add("dark-mode");
        document.body.classList.add("dark-mode");
    }
    updateThemeToggleLinkText(); // Set initial dropdown link text based on the theme

    const upload_image_button = document.getElementById("upload_image_button");
    const file_input = document.getElementById("ASL_image");
    const capture_image_button = document.getElementById("capture_image_button");
    const video = document.getElementById("camera");
    const canvas = document.getElementById("snapshot");
    const camera_results = document.getElementById("camera_results");
    const upload_results = document.getElementById("upload_results");
    const methodSelector = document.getElementById("methodSelector");
    const cameraSection = document.getElementById("camera-section");
    const uploadSection = document.getElementById("upload-section");

    // Covers functionality to take and upload photos to guess ASL sign located on the "Upload" page of website
    // Force default display
    cameraSection.style.display = "block";
    uploadSection.style.display = "none";

    // Upload Options dropdown
    methodSelector.addEventListener("change", function () {
        console.log("User selected:", methodSelector.value);

        if (methodSelector.value === "camera") {
            cameraSection.style.display = "block";
            uploadSection.style.display = "none";
        } else if (methodSelector.value === "upload") {
            cameraSection.style.display = "none";
            uploadSection.style.display = "block";
        }
    });

    // Check if user allowed access to device's camera, and start the webcam
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices
            // ask user for permission to access device's camera
            .getUserMedia({video: true})
            .then((stream) => {
                video.srcObject = stream;
                video.play(); // user allowed access to camera stream camera feed
            })
            .catch((err) => {
                // if user does not allow access to camera display message
                console.error("Camera access denied:", err);
                camera_results.textContent = "Unable to access camera.";
            });
    }

    // Send image to backend to get prediction
    function sendToBackend(blob, filename = "image.jpg", resultsTarget) {
        const formData = new FormData();
        formData.append("file", blob, filename); // append imagefile to formData which is sent to backend api/views

        fetch("/api/predict/", {
            method: "POST",
            body: formData,
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.predictions && data.predictions.length > 0) {
                    const formatted = data.predictions
                        .map((p) => `${p.label} @ (${p.x1}, ${p.y1}) → (${p.x2}, ${p.y2})`)
                        .join("\n");
                    resultsTarget.textContent = formatted;
                } else {
                    resultsTarget.textContent = "No predictions.";
                }
            })
            .catch((error) => {
                console.error("Prediction error:", error);
                resultsTarget.textContent = "Error connecting to backend.";
            });
    }

    // Button to upload an image file
    upload_image_button.addEventListener("click", function () {
        if (!file_input.files.length) {
            alert("Please select an image.");
            return;
        }

        const file = file_input.files[0];
        sendToBackend(file, file.name, upload_results);
    });

    // Webcam Snapshot
    capture_image_button.addEventListener("click", function () {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext("2d");
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        canvas.toBlob((image) => {
            sendToBackend(image, "capture.jpg", camera_results);
        }, "image/jpeg");
    });
});