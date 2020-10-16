function submitForm() {
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
    console.log('/api/surveys?' + form.serialize());
}

function getSurveyResultsBySurveyId(survey_id) {
    $.ajax(
      `/api/surveys/${survey_id}/results`,
      {
        type: 'GET',
        success: function(data, status, xhr) {
            var element = $("#results");
            var results_table = document.createElement("TABLE");
            for(var i; data.length(); i++){
                results_table +=
            }
        }
      }
    )
}