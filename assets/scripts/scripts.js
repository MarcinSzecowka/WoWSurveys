function submitSurveyCreationForm() {
    var form = $("#dungeon_form");
    var checkedBosses = $("#dungeon_form").find(".instance").not(".d-none").find(".boss-checkbox:checked + label");
    var bossesQuery = "";
    for (boss of checkedBosses) {
        bossesQuery = bossesQuery.concat(`&bosses=${encodeURIComponent(boss.innerText.trim())}`)
    }
    $.ajax(
      `/api/surveys?${form.serialize()}${bossesQuery}`,
      {
        type: 'POST',
        success: function(data, status, xhr) {
            window.location.href = `../survey/${data.id}/results/`;
        }
      }
    )
}


function getSurveyIdFromPathname() {
    var path = window.location.pathname.split("/");
    return path[path.length - 1];
}


function submitResultsForm(event) {
    var is_survey_valid = validateForm();
    if (!is_survey_valid) {
        return
    }

    var answers_table = [];
    var filled_form = $("#filled_dungeon_form").serialize();
    for (pair of filled_form.split("&")) {
        split_pair = pair.split("=")
        answers_table.push({
            "question_id": split_pair[0],
            "answer_id": split_pair[1]
        })
    }

    var surveyId = getSurveyIdFromPathname();
    var nickname = $("#nickname").val();
    var dungeon_name = $("#dungeon_name")[0].innerText

    FingerprintJS.load().then(fp => {
      fp.get().then(result => {
        const client_id = result.visitorId;

        $.ajax(
        `/api/surveys/${surveyId}/answers?client_id=${client_id}&nickname=${nickname}`,
        {
            type: 'POST',
            data: JSON.stringify(answers_table),
            success: function(data, status, xhr) {
                window.localStorage.setItem("recent_survey_id", surveyId);
                window.localStorage.setItem("recent_survey_dungeon_name", dungeon_name);
                window.localStorage.setItem(btoa(surveyId), btoa(`${data.score};${data.timestamp}`));
                window.location.href = '/result';
            },
            error: function(data, status, xhr) {
                if (data.status === 429){
                    var error_message_element = $("#error_message")[0];
                    error_message_element.classList.remove("d-none");
                    var button = $("#submit")[0];
                    button.disabled = true;
                }
            }
        }
        )
      });
    });
}

function validateForm() {
    var form = $("#filled_dungeon_form");
    var questions = form.find(".question").toArray();
    var is_valid = true;
    for (question of questions) {
        var question_element = $(question);
        if (!hasSelectedAnswer(question_element)) {
            addInvalidClassToAnswers(question_element);
            showWarning(question_element)
            is_valid = false;
        }
    }
    return is_valid;
}

function hasSelectedAnswer(question) {
    return question.find(".selected").length > 0;
}

function addInvalidClassToAnswers(question_element) {
    var answers = question_element.find(".answer").toArray();
    for (answer of answers) {
        answer.classList.add("is-invalid");
    }
}

function showWarning(question) {
    question.find(".form-warning")[0].classList.remove("d-none");
}

function removeWarning(question) {
    question.find(".form-warning")[0].classList.add("d-none");
}

function onInput(event) {
    var button = $("#submit")[0];
    var nickname = $("#nickname").val();
    if (nickname.length < 3) {
        button.disabled = true;
    } else {
        button.disabled = false;
    }
}

function surveyResultsOnLoad() {
    buildSurveyLink();
    initializeClipboard();
}

function buildSurveyLink() {
    var input_element = $("#share_link")[0];

    var urlPrefix = window.location.href.split("/survey/")[0];
    var survey_short_id = input_element.value;

    input_element.value = `${urlPrefix}/${survey_short_id}`;
}

function initializeClipboard() {
    var button = $("#btn_copy")[0];
    var clipboard = new ClipboardJS(button);
    clipboard.on('success', function(e) {
        e.clearSelection();
        button.innerText = "Copied"
    });
}

function onAnswerSelected(event) {
    var currentAnswersGroup = $(event.currentTarget)[0].parentElement
    $(currentAnswersGroup).find(".answer").toArray().forEach(answer => answer.classList.remove("selected"));
    event.currentTarget.classList.add("selected");
    var inputToCheck = $(event.currentTarget).find("input")[0];
    inputToCheck.checked = true;
    var question = currentAnswersGroup.parentElement;
    currentAnswersGroup.classList.remove("is-invalid");
    removeBordersFromAnswers(currentAnswersGroup);
    removeWarning($(question));
}

function removeBordersFromAnswers(answersGroup) {
    var answers = $(answersGroup).find(".answer").toArray();
    for(answer of answers) {
        answer.classList.remove("is-invalid");
    }
}

function displayInstanceBosses(event) {
    var allInstances = $(".instance");
    for (instance of allInstances) {
        $(instance).addClass("d-none")
    }
    var instanceName = event.target.value.replaceAll(" ","_");
    var instanceToShow = $(`#${instanceName}`);
    if (typeof instanceToShow[0] != "undefined") {
        instanceToShow[0].classList.remove("d-none")
        };
}

function displayCurrentlySelectedInstance() {
    var selected = $("#instance_name").val()
    console.log(selected)
}