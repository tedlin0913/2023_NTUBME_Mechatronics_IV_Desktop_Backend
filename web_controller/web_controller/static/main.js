$(document).ready(function () {
    // Set placeholder text as initial iframe source
    var placeholderUrl = $("#video_url").attr("placeholder");
    $("#videoIframe").attr("src", placeholderUrl);

    // Enable touch and click for all buttons
    enableTouchAndClickForAllButtons();
});

// Update video url
function updateVideo() {
    var newVideoUrl = $("#video_url").val();
    $.ajax({
        type: 'POST',
        url: '/update_video',
        data: { 'video_url': newVideoUrl },
        success: function (response) {
            $("#videoIframe").attr("src", response.updated_url);
            const msg = `Update url: ${response.updated_url}`
            console.log(msg);
        },
        error: function (error) {
            console.log(error);
        }
    });
}

function updateControl(control) {
    $.ajax({
        type: 'POST',
        url: '/control',
        data: { 'control': control },
        success: function (response) {
            const msg = `Control: ${response.control}`
            console.log(msg);
        },
        error: function (error) {
            console.log(error);
        }
    });
}

function enableTouchAndClickForAllButtons() {
    // Handle both click and touchend events for all buttons
    $(document).on('click touchend', 'button', function (event) {
        event.preventDefault();
        // You can check the specific button by its ID, class, or any other attribute
        // For example, if you want to run a specific function for a button with the ID 'updateButton':
        if ($(this).attr('id') === 'update_btn') {
            updateVideo();
        } else if ($(this).attr('id') === 'control_btn') {
            updateControl($(this).val());
        }

    });
}