// Track all clicks and form submissions silently
document.addEventListener("click", function(e) {
    let target = e.target;
    let data = {
        event: "click",
        element: target.tagName,
        id: target.id || null,
        classes: target.className || null,
        timestamp: new Date().toISOString()
    };
    sendEvent(data);
});

document.addEventListener("submit", function(e) {
    let form = e.target;
    let formData = {};
    for (let pair of new FormData(form).entries()) {
        formData[pair[0]] = pair[1];
    }
    let data = {
        event: "form_submit",
        form: form.id || form.name || "unknown",
        data: formData,
        timestamp: new Date().toISOString()
    };
    sendEvent(data);
});

function sendEvent(eventData) {
    fetch("/predict", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(eventData)
    }).catch(err => console.log("AI Tracking Error:", err));
}
