function build_box_html(detection_results) {
    if (detection_results.length == 0)
        return '';
    return detection_results.map(result => {
        result.boxes.forEach(box => box.class = result.class);
        return result.boxes;
    })
    .reduce((a, b) => a.concat(b))
    .map(box => ({
        'class': box.class,
        'coord': {
            'top': box.coord[1],
            'left': box.coord[0],
            'width': box.coord[2] - box.coord[0],
            'height': box.coord[3] - box.coord[1]
        },
        'score': box.score
    })).map(box => map_box_html(box));
}

function map_box_html(box) {
    return '<div class="detection-box"  style="top: '+box.coord.top+'px; left: '+box.coord.left+'px; width: '+box.coord.width+'px; height: '+box.coord.height+'px"><div class="detection-class">'+box.class+' ('+Math.round(box.score * 100)+'%)'+'</div></div>';
}

var streamerBox = document.getElementById('streamer_box');
var streamerImage = document.getElementById('streamer_image');

var tick = Date.now();

function toggle_detection() {
    DETECTION_ENABLED = !DETECTION_ENABLED;
    if (!DETECTION_ENABLED)
        $(streamerBox).html('');
}

function run_streamer() {
    toDataURL(STREAM_URL, function(dataUrl) {
        var image  = new Image();

        image.addEventListener("load", function () {
            $(streamerImage).html('');
            streamerImage.appendChild( this );
            run_streamer();
        });
        image.src = dataUrl;

        var now = Date.now();
        if (now - tick < window.DETECTION_DELAY || !DETECTION_ENABLED) {
            return;
        }
        tick = now;
        var base64 = dataUrl.substring('data:image/jpeg;base64,'.length - 1);
        detect_object(base64, function(result) {
            if (!DETECTION_ENABLED)
                return;
            var detection_results = result.msg.detections;
            var boxes = build_box_html(detection_results);
            $(streamerBox).html(boxes);
        }, function(err) {
            console.log(err);
        });
    });
}

function toDataURL(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.onload = function() {
        var reader = new FileReader();
        reader.onloadend = function() {
        callback(reader.result);
        }
        reader.readAsDataURL(xhr.response);
    };
    xhr.open('GET', url);
    xhr.responseType = 'blob';
    xhr.send();
}

function imageChange(e) {
    var file = e.target.files[0];

    elPreview = document.getElementById("preview");
    var reader = new FileReader();
    reader.addEventListener("load", function () {
        var image  = new Image();

        image.addEventListener("load", function () {
            $(elPreview).html('')
            var imageInfo = file.name +' '+
            image.width +'x'+
            image.height +' '+
            file.type +' '+
            Math.round(file.size/1024) +'KB';

            // Show image and info
            elPreview.appendChild( this );
            elPreview.insertAdjacentHTML("beforeend", imageInfo +'<br>');
        });
        image.src = reader.result;

        var base64 = reader.result.substring('data:image/jpeg;base64,'.length - 1);
        detect_object(base64, function(result) {
            var detection_results = result.msg.detections;
            var boxes = build_box_html(detection_results);
            $(elPreview).append(boxes);
        }, function(err) {
            console.log(err);
        });
    });

    reader.readAsDataURL(file);
}