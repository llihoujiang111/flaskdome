
window.onload = function () {
    itqiniu.setUp({
        'domain': 'http://jpg.lihoujiang.online/',
        'browse_btn': 'upload-btn',
        'uptoken_url': '/uptoken/?space=lhjimg',
        'success': function (up, file, info) {
            let image_url = file.name;
            // console.log(image_url);
            let image_input = document.getElementById('image-input');
            image_input.value = image_url;
            let img = document.getElementById('image-show');
            img.setAttribute('src', image_url);
        }
    });
};
