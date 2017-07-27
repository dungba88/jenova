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

var NMS_THRESH = 0.9;

function toggle_detection() {
    DETECTION_ENABLED = !DETECTION_ENABLED;
    if (!DETECTION_ENABLED)
        $(streamerBox).html('');
}

var lastBoxes = []

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
            var detectionResults = result.msg.detections;
            detectionResults = compareAndSuppress(detectionResults, lastBoxes);
            lastBoxes = detectionResults;
            var boxes = build_box_html(detectionResults);
            $(streamerBox).html(boxes);
        }, function(err) {
            console.log(err);
        });
    });
}

function compareAndSuppress(curBoxes, lastBoxes) {
    if (lastBoxes.length == 0)
        return curBoxes;
    for(var i in curBoxes) {
        var curBox = curBoxes[i];
        var lastBoxesWithSameClass = lastBoxes.filter(b => b.class == curBox.class);
        var classBoxes = lastBoxesWithSameClass.length > 0 ? lastBoxesWithSameClass[0].boxes : [];
        if (classBoxes.length == 0)
            continue;
        curBox.boxes = curBox.boxes.map(box => getOverlap(box, classBoxes));
    }
    return curBoxes;
}

function getOverlap(box, classBoxes) {
    var overlaps = classBoxes.filter(classBox => isOverlap(box.coord, classBox.coord));
    if (overlaps.length == 0) {
        return box;
    }
    return overlaps[0];
}

function isOverlap(box, classBox) {
    var leftMax = Math.max(box[0], classBox[0]);
    var topMax = Math.max(box[1], classBox[1]);
    var rightMin = Math.min(box[2], classBox[2]);
    var bottomMin = Math.max(box[3], classBox[3]);

    if (rightMin < leftMax || bottomMin < topMax)   // not overlap at all
        return false;
    var overlapArea = (rightMin - leftMax) * (bottomMin - topMax);
    var boxArea = (box[2] - box[0]) * (box[3] - box[1]);
    return overlapArea / boxArea >= NMS_THRESH;
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