function submitForm() {
    var dungeon = $("#dungeon option:selected").val();
    $.ajax(
      '/api/surveys?instance_name=' + dungeon,
      {
        type: 'POST',
        success: function(data, status, xhr) {
            window.location.href = `../survey/${data.id}/results/`;
        }
      }
    )
    console.log('/api/surveys?instance_name=' + dungeon);
}