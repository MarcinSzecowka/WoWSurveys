function submitSurveyCreationForm() {
    var form = $("#dungeon_form");
    $.ajax(
      `/api/surveys?${form.serialize()}`,
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

    $.ajax(
      `/api/surveys/${surveyId}/answers?nickname=${nickname}`,
      {
        type: 'POST',
        data: JSON.stringify(answers_table),
        success: function(data, status, xhr) {
            window.localStorage.setItem("recent_survey_id", surveyId);
            window.localStorage.setItem("recent_survey_dungeon_name", dungeon_name);
            window.localStorage.setItem(surveyId, data.score);
        }
      }
    )
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