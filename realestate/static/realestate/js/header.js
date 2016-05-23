$( document ).ready(
    $(function() {
    $('#language_select').change(function() {
        this.form.submit();
        });
    })
);
