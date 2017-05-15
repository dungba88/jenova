var ALLOW_TYPING = true;
var current_idx = -1;
var command_histories = [];

var command_helps = {
    bot_commands: {
        talk: 'Send a text to the bot server. Usage: talk {sentence}',
        audio: 'Start dictation',
        say: 'Make the robot say a sentence. Usage: say {sentence}',
        go: 'Make the robot go',
        switch: 'Switch the bot. Usage: switch {bot_name}',
        teach: 'Teach the robot. Usage: teach {sentence},{intent}',
        train: 'Train the bot server',
        test: 'Test the model against cross validation data',
        raw: 'Send a raw command to the bot server',
        reload: 'Reload bot configurations'
    },
    interface_commands: {
        clear: 'Clear the console interface',
        info: 'Get client information',
        servinfo: 'Get server information',
        eval: 'Execute javascript code. Usage: eval {statement}'
    },
    misc: {
        help: 'Print help',
        man: 'Alias for help'
    }
}

function startDictation() {
    $('#audio').prop('disabled', true);
    $('#audio').html('Speak now...');
    var recognition = new webkitSpeechRecognition();

    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.lang = LANG;
    recognition.start();

    recognition.onresult = function(e) {
        $('#audio').prop('disabled', false);
        $('#audio').html('Speak');
        transcript = e.results[0][0].transcript;
        recognition.stop();
        add_command('talk ' + transcript);
        run_command('talk ' + transcript);
    };

    recognition.onerror = function(e) {
        $('#audio').prop('disabled', false);
        $('#audio').html('Speak');
        recognition.stop();
        add_error('Audio failed: ' + e.error);
    }                
}

function call_service(text) {
    call_raw(JSON.stringify({
        "name": "predict",
        "args": {
            "data_name": DATA_NANE,
            "text": text
        }
    }));
}

function speak(text) {
    sentences = text.split(/[.!?]/).forEach(speak_sentence);
}

function speak_sentence(sentence) {
    utter = new SpeechSynthesisUtterance(sentence);
    // utter.voice = window.speechSynthesis.getVoices()[4];
    window.speechSynthesis.speak(utter);
}

function call_raw(text) {
    ALLOW_TYPING = false;
    $.post(SERVER_URL, text, function(res) {
        ALLOW_TYPING = true;
        if (res.status == 1) {
            add_error(res.msg);
        } else {
            if (typeof res.msg == 'string' || res.msg == undefined) {
                add_response(res.msg);
            } else {
                add_response("Bot says: <i>" + res.msg.bot_response + "</i><br />" + res.msg.raw + "<br />");

                if (window.ENABLE_TTS) {
                    speak(res.msg.bot_response.replace(/(?:https?|ftp):\/\/[\n\S]+/g, ''));
                }
            }
        }
    }).fail(function(xhr, status, err) {
        ALLOW_TYPING = true;
        if (xhr.readyState == 0) {
            add_error('Cannot connect to server');
        } else {
            add_error('Error from server: ' + err);
        }
    });
}

function add_command(text) {
    $('#response').append('<li class="command">' + text + '</li>');
    $('#response').scrollTop($('#response')[0].scrollHeight);
}

function add_response(text, skip_next_command) {
    $('#response').append('<li class="resp">' + text + '</li>');
    if (!skip_next_command) {
        add_command('');
    }
    $('#response').scrollTop($('#response')[0].scrollHeight);
}

function add_error(err) {
    $('#response').append('<li class="error resp">' + err + '</li>');
    add_command('');
}

function run_command(text) {
    if (text == undefined || text.trim() == '') {
        add_command('');
        return;
    }
    command_histories.push(text);
    current_idx = command_histories.length;

    commands = text.split(' ');
    command = commands[0];
    if (bot_commands[command] == undefined) {
        add_error(command + ': command not found. Type help for available commands.')
        return;
    }
    commands.splice(0, 1);
    try {
        bot_commands[command](commands.join(' '));
    } catch(ex) {
        add_error(ex);
    }
}

bot_commands = {

    clear: function() {
        $('#response').text('');
        add_command('');
        command_histories = [];
        current_idx = -1;
    },

    talk: function(text) {
        if (!text) {
            throw new Error('Sentence is empty');
        }
        call_service(text);
    },

    test: function(text) {
        call_raw(JSON.stringify({
            "name": "test",
            "args": {
                "data_name": DATA_NANE
            }
        }));
    },

    raw: function(text) {
        call_raw(text);
    },

    man: function(text) {
        this.help(text);
    },

    help: function(text) {
        if (text != undefined && text != '') {
            helpText = findCommandHelp(text);
            if (helpText == undefined) {
                add_error('No help found for command: ' + text);
                return;
            }
            add_response(helpText);
            return;
        }
        for(var category in command_helps) {
            add_response('<a><b>' + category + '</b></a>', true);
            for(var command in command_helps[category]) {
                add_response(' - <div class="helpitem">' + command + '</div>' + command_helps[category][command], true);
            }
        }
        add_command('');
    },

    audio: function(text) {
        startDictation();
    },

    teach: function(text) {
        call_raw(JSON.stringify({
            "name": "teach",
            "args": {
                "text": text,
                "data_name": DATA_NANE
            }
        }));
    },

    train: function(text) {
        call_raw(JSON.stringify({
            "name": "train",
            "args": {
                "data_name": DATA_NANE
            }
        }));
    },

    reload: function(text) {
        call_raw(JSON.stringify({
            "name": "reload",
            "args": {
            }
        }));
    },

    say: function(text) {
        if (!text) {
            throw new Error('Sentence is empty');
        }
        call_raw(JSON.stringify({
            "name": "pass",
            "args": {
                "command": {
                    "name": "say",
                    "args": {
                        "text": text
                    }
                }
            }
        }));
    },

    go: function(text) {
        if (!text) {
            throw new Error('Direction is empty');
        }
        frags = text.split(' ')
        call_raw(JSON.stringify({
            "name": "pass",
            "args": {
                "command": {
                    "name": "go",
                    "args": {
                        "behavior": frags[0],
                        "power": parseInt(frags[1])
                    }
                }
            }
        }));
    },

    switch: function(text) {
        if (!text) {
            throw new Error('Bot name is empty');
        }
        call_raw(JSON.stringify({
            "name": "pass",
            "args": {
                "command": {
                    "name": "switch",
                    "args": {
                        "bot": text
                    }
                }
            }
        }));
    },

    servinfo: function(text) {
        add_response('Server configured at: <a target="_blank" href="' + SERVER_URL + '">'+SERVER_URL+'</a>');
    },

    info: function(text) {
        for(key in navigator) {
            if (typeof navigator[key] == 'string')
                add_response('<b>' + key + '</b>: ' + navigator[key], true);
        }
        add_command('');
    },

    eval: function(text) {
        if (!text) {
            throw new Error('Statement is empty');
        }
        result = eval(text);
        add_response(result);
    }
}

function findCommandHelp(command) {
    for(var category in command_helps) {
        if (command_helps[category][command] != undefined) {
            return command_helps[category][command];
        }
    }
}

function autosuggest(element) {
    text = element.text();
    for(command in bot_commands) {
        if (command.startsWith(text)) {
            element.text(command);
            return;
        }
    }
}

document.addEventListener('keydown', function(e) {
    if (!ALLOW_TYPING)
        return;
    element = $('#response li:last');
    if (e.keyCode == 13) {
        if (element.length == 0 || !element.hasClass('command'))
            return;
        text = element.text();
        run_command(text);
        return;
    }
    if (e.keyCode == 8) {
        if (element.length == 0 || !element.hasClass('command'))
            return;
        text = element.text();
        element.text(text.substr(0, text.length - 1))
        return;
    }
    if (e.keyCode == 9) {
        if (element.length == 0 || !element.hasClass('command'))
            return;
        autosuggest(element);
        e.preventDefault();
        return;
    }
    if (e.keyCode >= 112 && e.keyCode <= 123)
        return;
    if (e.keyCode == 38) {
        if (element.length == 0 || !element.hasClass('command'))
            return;
        if (current_idx < 0) {
            current_idx = command_histories.length - 1;
        }
        if (current_idx > 0)
            current_idx--;
        if (current_idx >= 0 && current_idx <= command_histories.length - 1) {
            element.text(command_histories[current_idx]);
        }
        e.preventDefault();
        return;
    }
    if (e.keyCode == 40) {
        if (element.length == 0 || !element.hasClass('command'))
            return;
        if (current_idx < 0) {
            current_idx = command_histories.length - 1;
        }
        if (current_idx < command_histories.length)
            current_idx++;
        if (current_idx >= 0 && current_idx <= command_histories.length - 1) {
            element.text(command_histories[current_idx]);
        } else {
            element.text('');
        }
        e.preventDefault();
        return;
    }
    if ((e.keyCode != 32 && e.keyCode <= 40) || e.keyCode == 91)
        return;
    if (e.ctrlKey && e.key == 'c') {
        add_command('');
        return;
    }
    if (e.ctrlKey || e.altKey || e.metaKey)
        return;
    if (e.ctrlKey == "5")
    if (element.length == 0 || !element.hasClass('command')) {
        add_command("");
        element = $('#response li:last');
    }
    element.append(e.key);
});

for(var command in bot_commands) {
    if (window[command] == undefined)
        window[command] = bot_commands[command];
}